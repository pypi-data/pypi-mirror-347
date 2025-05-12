# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.signal import spectrogram
from matplotlib.ticker import LinearLocator, FormatStrFormatter, FuncFormatter
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import signal, stats, ndimage, interpolate
from scipy.signal.windows import hann
import nnresample
from copy import deepcopy
from autoeq.frequency_response import FrequencyResponse
from utils import magnitude_response, get_ylim, running_mean
from constants import COLORS


class ImpulseResponse:
    def __init__(self, data, fs, recording=None):
        self.fs = fs
        self.data = data
        self.recording = recording

    def copy(self):
        return deepcopy(self)

    def __len__(self):
        """Impulse response length in samples."""
        return len(self.data)

    def duration(self):
        """Impulse response duration in seconds."""
        return len(self) / self.fs

    def peak_index(self, start=0, end=None, peak_height=0.12589):
        """Finds the first high (negative or positive) peak in the impulse response wave form.

        Args:
            start: Index for start of search range
            end: Index for end of search range
            peak_height: Minimum peak height. Default is -18 dBFS

        Returns:
            Peak index to impulse response data
        """
        if end is None:
            end = len(self.data)
        # Peak height threshold, relative to the data maximum value
        # Copy to avoid manipulating the original data here
        data = self.data.copy()
        # Limit search to given range
        data = data[start:end]
        # Normalize to 1.0
        data /= np.max(np.abs(data))
        # Find positive peaks
        peaks_pos, properties = signal.find_peaks(data, height=peak_height)
        # Find negative peaks that are at least
        peaks_neg, _ = signal.find_peaks(data * -1.0, height=peak_height)
        # Combine positive and negative peaks
        peaks = np.concatenate([peaks_pos, peaks_neg])
        # Add start delta to peak indices
        peaks += start
        # Return the first one
        return np.min(peaks)

    def decay_params(self):
        """Determines decay parameters with Lundeby method

        https://www.ingentaconnect.com/content/dav/aaua/1995/00000081/00000004/art00009
        http://users.spa.aalto.fi/mak/PUB/AES_Modal9992.pdf

        Returns:
            - peak_ind: Fundamental starting index
            - knee_point_ind: Index where decay reaches noise floor
            - noise_floor: Noise floor in dBFS, also peak to noise ratio
            - window_size: Averaging window size as determined by Lundeby method
        """
        peak_index = self.peak_index()

        # 1. The squared impulse response is averaged into localtime intervals in the range of 10–50 ms,
        # to yield a smooth curve without losing short decays.
        data = self.data.copy()
        # From peak to 2 seconds after the peak
        data = data[peak_index:min(peak_index + 2 * self.fs, len(self))]
        data /= np.max(np.abs(data))  # Normalize
        squared = data ** 2  # Squared impulse response starting from the peak
        t_squared = np.linspace(0, len(squared) / self.fs, len(squared))  # Time stamps starting from peak
        wd = 0.03  # Window duration, let's start with 30 ms
        n = int(len(squared) / self.fs / wd)  # Number of time windows
        w = int(len(squared) / n)  # Width of a single time window
        t_windows = np.arange(n) * wd + wd / 2  # Timestamps for the window centers
        windows = squared.copy()  # Copy to avoid modifying the original
        windows = np.reshape(windows[:n * w], (n, w))  # Split into time windows, one window per row
        windows = np.mean(windows, axis=1)  # Average each time window
        windows = 10 * np.log10(windows)  # dB

        # 2. A first estimate for the background noise level is determined  from a time segment containing the last
        # 10 % of the impulse response. This gives a reasonable statistical selection without a large systematic error,
        # if the decay continues to the end of the response.
        tail = squared[int(-0.1 * len(squared)):]  # Last 10 %
        noise_floor = 10 * np.log10(np.mean(tail))  # Mean as dBs, not mean of dB values

        # 3. The decay slope is estimated using linear regression between the time interval containing the response
        # 0 dB peak, and  the  first interval 5–10 dB above the background noise level.
        slope_end = np.argwhere(windows <= noise_floor + 10)[0, 0] - 1  # Index previous to the first below 10 dB
        slope, intercept, _, _, _ = stats.linregress(t_windows[:slope_end], windows[:slope_end])

        # 4. A preliminary knee point is determined at the intersection of the decay slope and the background noise
        # level.
        # Everything falls apart if this is not in the decay range but in the tail
        # This can happen when there is a long tail which has plateau first but then starts to decay again
        # in that case the noise floor estimated from the end of the impulse response is far below the knee point.
        # Should be preventable by truncating the impulse response to N seconds after the peak
        knee_point_time = (noise_floor - intercept) / slope

        # 5. A new time interval length is calculated according to the calculated slope, so that there are 3–10
        # intervals per 10 dB of decay.
        n_windows_per_10dB = 3
        wd = 10 / (abs(slope) * n_windows_per_10dB)
        n = int(len(squared) / self.fs / wd)  # Number of time windows
        w = int(len(squared) / n)  # Width of a single time window
        t_windows = np.arange(n) * wd + wd / 2  # Time window center time stamps

        # 6. The squared impulse is averaged into the new local time intervals.
        windows = squared.copy()
        windows = np.reshape(windows[:n * w], (n, w))  # Split into time windows
        windows = np.mean(windows, axis=1)  # Average each time window
        windows = 10 * np.log10(windows)  # dB

        try:
            knee_point_index = np.argwhere(t_windows >= knee_point_time)[0, 0]
            knee_point_value = windows[knee_point_index]
        except IndexError as err:
            # Probably tail has already been cropped
            return peak_index, len(self), noise_floor, w
        # print(f'    Knee point: {knee_point_value:.2f} dB @ {knee_point_time * 1000:.0f} ms')

        # Steps 7–9 are iterated until the knee_point is found to converge(max. 5 iterations).
        for i in range(5):
            # print(f'    iter {i}')
            # 7. The background noise level is determined again. The evaluated noise segment should start from a
            # point corresponding to 5–10 dB of decay after the knee_point, or a minimum of 10 % of the total
            # response length.
            try:
                noise_floor_start_index = np.argwhere(windows <= knee_point_value - 5)[0, 0]
            except IndexError:
                break
            noise_floor_start_time = max(t_windows[noise_floor_start_index], 0.1 * self.duration())
            # Protection against over shooting the impulse response end, in case the IR has been truncated already
            # In that case the noise floor will be calculated from the last half of the last window
            noise_floor_start_time = min(noise_floor_start_time, t_windows[-1])

            # noise_floor_end_time = noise_floor_start_time + 0.1 * len(squared) / ir.fs  # TODO: Until the very end?
            # Noise floor estimation range ends one full decay time after the start, truncated to the IR length
            noise_floor_end_time = min(noise_floor_start_time + knee_point_time, self.duration())
            noise_floor = np.mean(squared[np.logical_and(
                t_squared >= noise_floor_start_time,
                t_squared <= noise_floor_end_time
            )])
            noise_floor = 10 * np.log10(noise_floor)  # dB
            # print(f'      Noise floor '
            #       f'({(noise_floor_start_time + peak_index / self.fs) * 1000:.0f} ms -> '
            #       f'{(noise_floor_end_time + peak_index / self.fs) * 1000:.0f} ms): '
            #       f'{noise_floor}')

            # 8. The late decay slope is estimated for a dynamic range of 10–20 dB, starting from a point 5–10 dB above
            # the noise level.
            slope_end_headroom = 8
            slope_dynamic_range = 20
            try:
                slope_end = np.argwhere(windows <= noise_floor + slope_end_headroom)[0, 0] - 1  # 8 dB above noise level
                slope_start = np.argwhere(windows <= noise_floor + (slope_end_headroom + slope_dynamic_range))[0, 0] - 1
                late_slope, late_intercept, _, _, _ = stats.linregress(
                    t_windows[slope_start:slope_end],
                    windows[slope_start:slope_end]
                )
            except (IndexError, ValueError):
                # Problems with already cropped IR tail
                break
            # print(f'      Late slope {t_windows[slope_start] * 1000:.0f} ms -> {t_windows[slope_end] * 1000:.0f} ms: {late_slope:.1f}t + {late_intercept:.2f}')

            # 9. A new knee_point is found.
            knee_point_time = (noise_floor - late_intercept) / late_slope
            if knee_point_time > t_windows[-1]:
                knee_point_time = t_windows[-1]
                break
            knee_point_index = np.argwhere(t_windows >= knee_point_time)[0, 0]
            knee_point_value = windows[knee_point_index]
            # print(f'      Knee point: {knee_point_value:.2f} dB @ {knee_point_time * 1000:.0f} ms')
            # Index of first window which comes after slope end time
            new_knee_point_index = np.argwhere(t_windows >= knee_point_time)[0, 0]
            if new_knee_point_index == knee_point_index:
                # Converged
                knee_point_index = new_knee_point_index
                break
            else:
                knee_point_index = new_knee_point_index

        # Until this point knee_point_index has been an index to windows,
        # find the index to impulse response data
        knee_point_time = t_windows[knee_point_index]
        knee_point_index = np.argwhere(t_squared >= knee_point_time)[0, 0]

        return peak_index, peak_index + knee_point_index, noise_floor, w

    def decay_times(self, peak_ind=None, knee_point_ind=None, noise_floor=None, window_size=None):
        """Calculates decay times EDT, RT20, RT30, RT60

        Args:
            peak_ind: Peak index as returned by `decay_params()`. Optional.
            knee_point_ind: Knee point index as returned by `decay_params()`. Optional.
            noise_floor: Noise floor as returned by `decay_params()`. Optional.
            window_size: Moving average window size as returned by `decay_params()`. Optional.

        Returns:
            - EDT, None if SNR < 10 dB
            - RT20, None if SNR < 35 dB
            - RT30, None if SNR < 45 dB
            - RT60, None if SNR < 75 dB

        """
        if peak_ind is None or knee_point_ind is None or noise_floor is None:
            peak_ind, knee_point_ind, noise_floor, window_size = self.decay_params()

        t = np.linspace(0, self.duration(), len(self))

        knee_point_ind -= (peak_ind + 0)
        data = self.data.copy()
        data = data[peak_ind - 0 * self.fs // 1000:]
        data /= np.max(np.abs(data))
        # analytical = np.abs(signal.hilbert(data))  # Hilbert doesn't work will with broadband signa
        analytical = np.abs(data)

        schroeder = np.cumsum(analytical[knee_point_ind::-1] ** 2 / np.sum(analytical[:knee_point_ind] ** 2))[:0:-1]
        schroeder = 10 * np.log10(schroeder)

        # Moving average of the squared impulse response
        avg = self.data.copy()
        # Truncate data to avoid unnecessary computations
        # Ideally avg_head is the half window size but this might not be possible if the IR has been truncated already
        # and the peak is closer to the start than half window
        avg_head = min((window_size // 2), peak_ind)
        avg_tail = min((window_size // 2), len(avg) - (peak_ind + knee_point_ind))
        # We need an index offset for average curve if the avg_head is not half window
        avg_offset = window_size // 2 - avg_head
        avg = avg[peak_ind - avg_head:peak_ind + knee_point_ind + avg_tail]  # Truncate
        avg /= np.max(np.abs(avg))  # Normalize
        avg = avg ** 2
        avg = running_mean(avg, window_size)
        avg = 10 * np.log10(avg + 1e-18)
        # Find offset which minimizes difference between Schroeder backward integral and the moving average
        # ie. offset which moves Schroeder curve to same vertical position as the decay power curve
        # Limit the range 10% -> 90% of Schroeder and avg start and end
        fit_start = max(int(len(schroeder) * 0.1), avg_offset)  # avg could start after 10% of Schroeder
        fit_end = min(int(len(schroeder) * 0.9), avg_offset + (len(avg)))  # avg could end before 90% of Schroeder
        offset = np.mean(
            schroeder[fit_start:fit_end] -
            avg[fit_start - avg_offset:fit_end - avg_offset]  # Shift avg indexes by the offset length
        )

        decay_times = dict()
        limits = [(-1, -10, -10, 'EDT'), (-5, -25, -20, 'RT20'), (-5, -35, -30, 'RT30'), (-5, -65, -60, 'RT60')]
        for start_target, end_target, decay_target, name in limits:
            decay_times[name] = None
            if end_target < noise_floor + offset + 10:
                # There has to be at least 10 dB of headroom between the end target point and noise floor,
                # in this case there is not. Current decay time shall remain undefined.
                continue
            try:
                start = np.argwhere(schroeder <= start_target)[0, 0]
                end = np.argwhere(schroeder <= end_target)[0, 0]
            except IndexError as err:
                # Targets not found on the Schroeder curve
                continue
            slope, intercept, _, _, _ = stats.linregress(t[start:end], schroeder[start:end])
            decay_times[name] = decay_target / slope

        return decay_times['EDT'], decay_times['RT20'], decay_times['RT30'], decay_times['RT60']

    def crop_head(self, head_ms=1):
        """Crops away head."""
        self.data = self.data[self.peak_index() - int(self.fs * head_ms / 1000):]

    def equalize(self, fir):
        """Equalizes this impulse response with give FIR filter.

        Args:
            fir: FIR filter as an single dimensional array

        Returns:
            None
        """
        self.data = signal.convolve(self.data, fir, mode='full')

    def resample(self, fs):
        """Resamples this impulse response to the given sampling rate."""
        self.data = nnresample.resample(self.data, fs, self.fs)
        self.fs = fs

    def convolve(self, x):
        """Convolves input data with this impulse response

        Args:
            x: Input data to be convolved

        Returns:
            Convolved data
        """
        return signal.convolve(x, self.data, mode='full')

    def adjust_decay(self, target):
        """Adjusts decay time in place.

        Args:
            target: Target 60 dB decay time in seconds

        Returns:
            None
        """
        peak_index, knee_point_index, _, _ = self.decay_params()
        edt, rt20, rt30, rt60 = self.decay_times()
        rt_slope = None
        # Finds largest available decay time parameter
        for rt_time, rt_level in [(edt, -10), (rt20, -20), (rt30, -30), (rt60, -60)]:
            if not rt_time:
                break
            rt_slope = rt_level / rt_time

        target_slope = -60 / target  # Target dB/s
        if target_slope > rt_slope:
            # We're not going to adjust decay and noise floor up
            return
        knee_point_time = knee_point_index / self.fs
        knee_point_level = rt_slope * knee_point_time  # Extrapolated level at knee point
        target_level = target_slope * knee_point_time  # Target level at knee point
        window_level = target_level - knee_point_level  # Adjustment level at knee point
        window_start = peak_index + 2 * (self.fs // 1000)
        half_window = knee_point_index - window_start  # Half Hanning window length, from peak to knee
        window = np.concatenate([  # Adjustment window
            np.ones(window_start),  # Start with ones until peak
            hann(half_window * 2)[half_window:],  # Slope down to knee point
            np.zeros(len(self) - knee_point_index)  # Fill with zeros to full length
        ]) - 1.0  # Slopes down from 0.0 to -1.0
        window *= -window_level  # Scale with adjustment level at knee point
        window = 10 ** (window / 20)  # Linear scale
        self.data *= window  # Scale impulse response data wit the window

    def magnitude_response(self):
        """Calculates magnitude response for the data."""
        return magnitude_response(self.data, self.fs)

    def frequency_response(self):
        """Creates FrequencyResponse instance."""
        f, m = self.magnitude_response()
        n = self.fs / 2 / 4  # 4 Hz resolution
        step = int(len(f) / n)
        # 0Hz 제외 (첫 번째 요소가 0인 경우)
        start_idx = 1 if f[0] == 0 else 0
        fr = FrequencyResponse(name='Frequency response', frequency=f[start_idx::step], raw=m[start_idx::step])
        fr.interpolate(f_step=1.01, f_min=10, f_max=self.fs / 2)
        return fr

    def plot(self,
             fig=None,
             ax=None,
             plot_file_path=None,
             plot_recording=True,
             plot_spectrogram=True,
             plot_ir=True,
             plot_fr=True,
             plot_decay=True,
             plot_waterfall=True):
        """Plots all plots into the same figure

        Args:
            fig: Figure instance
            ax: Axes instance, must have 2 rows and 3 columns
            plot_file_path: Path to a file for saving the plot
            plot_recording: Plot recording waveform?
            plot_spectrogram: Plot recording spectrogram?
            plot_ir: Plot impulse response?
            plot_fr: Plot frequency response?
            plot_decay: Plot decay curve?
            plot_waterfall: Plot waterfall graph?

        Returns:
            Figure
        """
        if fig is None:
            # Create figure and axises for the plots
            fig = plt.figure()
            fig.set_size_inches(22, 10)
            ax = []
            for i in range(5):
                ax.append(fig.add_subplot(2, 3, i + 1))
            ax.append(fig.add_subplot(2, 3, 6, projection='3d'))
            ax = np.vstack([ax[:3], ax[3:]])
        if plot_recording:
            self.plot_recording(fig=fig, ax=ax[0, 0])
        if plot_spectrogram:
            self.plot_spectrogram(fig=fig, ax=ax[1, 0])
        if plot_ir:
            self.plot_ir(fig=fig, ax=ax[0, 1])
        if plot_fr:
            self.plot_fr(fig=fig, ax=ax[1, 1])
        if plot_decay:
            self.plot_decay(fig=fig, ax=ax[0, 2])
        if plot_waterfall:
            self.plot_waterfall(fig=fig, ax=ax[1, 2])
        if plot_file_path:
            fig.savefig(plot_file_path)
        return fig

    def plot_recording(self, fig=None, ax=None, plot_file_path=None):
        """Plots recording wave form

        Args:
            fig: Figure instance
            ax: Axes instance
            plot_file_path: Path to a file for saving the plot

        Returns:
            - Figure
            - Axes
        """
        if self.recording is None or len(np.nonzero(self.recording)[0]) == 0:
            return
        if fig is None:
            fig, ax = plt.subplots()

        t = np.linspace(0, len(self.recording) / self.fs, len(self.recording))
        ax.plot(t, self.recording, color=COLORS['blue'], linewidth=0.5)

        ax.grid(True)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Sine Sweep')

        # Save image
        if plot_file_path:
            fig.savefig(plot_file_path)

        return fig, ax

    def plot_spectrogram(self, fig=None, ax=None, plot_file_path=None, f_res=10, n_segments=200):
        """Plots spectrogram of the recorded sweep.

        Args:
            fig: Matplotlib figure. If None, a new figure will be created
            ax: Matplotlib axis. If None, a new axis will be created
            plot_file_path: Path to save the plot to
            f_res: Frequency resolution in Hz
            n_segments: Number of spectrogram segments

        Returns:
            None
        """
        if self.recording is None:
            return
        if fig is None or ax is None:
            fig, ax = plt.subplots(figsize=(16/2.54, 9/2.54))

        # Spectrogram parameters
        nfft = round(self.fs / f_res)
        noverlap = int(nfft - (len(self.recording) - nfft) / n_segments)
        # Get spectrogram data
        spectrum, freqs, t = spectrogram(
            self.recording, 
            fs=self.fs, 
            nperseg=nfft, 
            noverlap=noverlap, 
            mode='psd'
        )

        # Remove zero frequency
        f = freqs[1:]
        z = spectrum[1:, :]
        # Logarithmic power
        z = 10 * np.log10(z)

        # Create spectrogram image
        t, f = np.meshgrid(t, f)
        cs = ax.pcolormesh(t, f, z, cmap='gnuplot2', vmin=-150, shading='auto')

        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(cs, cax=cax)

        ax.semilogy()
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_title('Spectrogram')

        # Save image
        if plot_file_path:
            fig.savefig(plot_file_path)

        return fig, ax

    def plot_ir(self, fig=None, ax=None, start=0.0, end=None, plot_file_path=None):
        """Plots impulse response wave form.

        Args:
            fig: Figure instance
            ax: Axis instance
            start: Start of the plot in seconds
            end: End of the plot in seconds
            plot_file_path: Path to a file for saving the plot

        Returns:
            None
        """
        if end is None:
            end = len(self.data) / self.fs
        ir = self.data[int(start * self.fs):int(end * self.fs)]

        if fig is None:
            fig, ax = plt.subplots()
        t = np.arange(start * 1000, start * 1000 + 1000 / self.fs * len(ir), 1000 / self.fs)
        ax.plot(t, ir, color=COLORS['blue'], linewidth=0.5)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Amplitude')
        ax.grid(True)
        ax.set_title('Impulse response'.format(ms=int(end * 1000)))

        if plot_file_path:
            fig.savefig(plot_file_path)

        return fig, ax

    def plot_fr(self,
                fr=None,
                fig=None,
                ax=None,
                plot_file_path=None,
                plot_raw=True,
                raw_color='#7db4db',
                plot_smoothed=True,
                smoothed_color='#1f77b4',
                plot_error=True,
                error_color='#dd8081',
                plot_error_smoothed=True,
                error_smoothed_color='#d62728',
                plot_target=True,
                target_color='#ecdef9',
                plot_equalization=True,
                equalization_color='#2ca02c',
                plot_equalized=True,
                equalized_color='#680fb9',
                fix_ylim=False):
        """Plots frequency response

        Args:
            fr: FrequencyResponse instance. Useful for passing instance with taget, error, equalization etc...
            fig: Figure instance
            ax: Axes instance
            plot_file_path: Path to a file for saving the plot
            plot_raw: Include raw curve?
            raw_color: Color of raw curve
            plot_smoothed: Include smoothed curve?
            smoothed_color: Color of smoothed curve
            plot_error: Include unsmoothed error curve?
            error_color: Color of error curve
            plot_error_smoothed: Include smoothed error curve?
            error_smoothed_color: Color of smoothed error curve
            plot_target: Include target curve?
            target_color: Color of target curve
            plot_equalization: Include equalization curve?
            equalization_color: Color of equalization curve
            plot_equalized: Include equalized curve?
            equalized_color: Color of equalized curve
            fix_ylim: Fix Y-axis limits calculation?

        Returns:
            - Figure
            - Axes
        """
        if fr is None:
            fr = self.frequency_response()
            fr.smoothen_fractional_octave(window_size=1/3, treble_f_lower=20000, treble_f_upper=23999)
        if fig is None:
            fig, ax = plt.subplots()
        ax.set_xlabel('Frequency (Hz)')
        ax.semilogx()
        ax.set_xlim([20, 20e3])
        ax.set_ylabel('Amplitude (dB)')
        ax.set_title(fr.name)
        ax.grid(True, which='major')
        ax.grid(True, which='minor')
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
        legend = []
        v = []
        sl = np.logical_and(fr.frequency >= 20, fr.frequency <= 20000)

        if plot_target and len(fr.target):
            ax.plot(fr.frequency, fr.target, linewidth=5, color=target_color)
            legend.append('Target')
            v.append(fr.target[sl])
        if plot_raw and len(fr.raw):
            ax.plot(fr.frequency, fr.raw, linewidth=0.5, color=raw_color)
            legend.append('Raw')
            v.append(fr.raw[sl])
        if plot_error and len(fr.error):
            ax.plot(fr.frequency, fr.error, linewidth=0.5, color=error_color)
            legend.append('Error')
            v.append(fr.error[sl])
        if plot_smoothed and len(fr.smoothed):
            ax.plot(fr.frequency, fr.smoothed, linewidth=1, color=smoothed_color)
            legend.append('Raw Smoothed')
            v.append(fr.smoothed[sl])
        if plot_error_smoothed and len(fr.error_smoothed):
            ax.plot(fr.frequency, fr.error_smoothed, linewidth=1, color=error_smoothed_color)
            legend.append('Error Smoothed')
            v.append(fr.error_smoothed[sl])
        if plot_equalization and len(fr.equalization):
            ax.plot(fr.frequency, fr.equalization, linewidth=1, color=equalization_color)
            legend.append('Equalization')
            v.append(fr.equalization[sl])
        if plot_equalized and len(fr.equalized_raw) and not len(fr.equalized_smoothed):
            ax.plot(fr.frequency, fr.equalized_raw, linewidth=1, color=equalized_color)
            legend.append('Equalized raw')
            v.append(fr.equalized_raw[sl])
        if plot_equalized and len(fr.equalized_smoothed):
            ax.plot(fr.frequency, fr.equalized_smoothed, linewidth=1, color=equalized_color)
            legend.append('Equalized smoothed')
            v.append(fr.equalized_smoothed[sl])

        if fix_ylim:
            # Y axis limits
            lower, upper = get_ylim(v)
            ax.set_ylim([lower, upper])

        ax.legend(legend, fontsize=8)

        if plot_file_path:
            fig.savefig(plot_file_path)

        return fig, ax

    def plot_decay(self, fig=None, ax=None, plot_file_path=None):
        """Plots decay graph.

        Args:
            fig: Figure instance. New will be created if None is passed.
            ax: Axis instance. New will be created if None is passed to fig.
            plot_file_path: Save plot figure to a file.

        Returns:
            - Figure
            - Axes
        """
        if fig is None:
            fig, ax = plt.subplots()

        peak_ind, knee_point_ind, noise_floor, window_size = self.decay_params()

        start = max(0, (peak_ind - 2 * (knee_point_ind - peak_ind)))
        end = min(len(self), (peak_ind + 2 * (knee_point_ind - peak_ind)))
        t = np.arange(start, end) / self.fs

        squared = self.data.copy()
        squared /= np.max(np.abs(squared))
        squared = squared[start:end] ** 2
        avg = running_mean(squared, window_size)
        squared = 10 * np.log10(squared + 1e-24)
        avg = 10 * np.log10(avg + 1e-24)

        ax.plot(t * 1000, squared, color=COLORS['lightblue'], label='Squared impulse response')
        ax.plot(
            t[window_size // 2:window_size // 2 + len(avg)] * 1000, avg, color=COLORS['blue'],
            label=f'{window_size / self.fs *1000:.0f} ms moving average'
        )

        ax.set_ylim([np.min(avg) * 1.2, 0])
        ax.set_xlim([
            start / self.fs * 1000,
            end / self.fs * 1000
        ])
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Amplitude (dBr)')
        ax.grid(True, which='major')
        ax.set_title('Decay')
        ax.legend(loc='upper right')

        if plot_file_path:
            fig.savefig(plot_file_path)

        return fig, ax

    def plot_waterfall(self, fig=None, ax=None):
        """Plots decay waterfall.

        Args:
            fig: Figure instance
            ax: Axis instance

        Returns:
            - Figure
            - Axis
        """
        if fig is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

        # Logarithmic sine sweep is the input signal
        window_length = 512
        window = hann(window_length)
        # 50% overlap means hop length = window length / 2
        hop_length = int(window_length / 2)
        # Copy and pad with zeros to include a few extra frames after the impulse response
        data = np.copy(self.data)
        s = np.zeros(hop_length * 5 + window_length)
        s[0:len(data)] = data
        data = s
        # Minimum number of frames
        n_min = 40
        # 50% overlap means hop length = window length / 2
        n_segments = max(int(len(data) / hop_length) - 1, n_min)
        nfft = window_length
        noverlap = nfft - hop_length

        # Get spectrogram data
        # Fs 대신 fs 사용, NFFT 대신 nperseg 사용, window 매개변수 업데이트
        spectrum, freqs, t = spectrogram(
            data, 
            fs=self.fs, 
            nperseg=nfft, 
            noverlap=noverlap, 
            mode='magnitude', 
            window=window
        )

        # Remove 0 Hz component
        spectrum = spectrum[1:, :]
        freqs = freqs[1:]

        # Interpolate to logaritmic frequency scale
        f_max = self.fs / 2
        f_min = 10
        step = 1.03
        f = np.array([f_min * step ** i for i in range(int(np.log(f_max / f_min) / np.log(step)))])
        log_f_spec = np.ones((len(f), spectrum.shape[1]))
        for i in range(spectrum.shape[1]):
            interpolator = interpolate.InterpolatedUnivariateSpline(np.log10(freqs), spectrum[:, i], k=1)
            log_f_spec[:, i] = interpolator(np.log10(f))
        z = log_f_spec
        f = np.log10(f)

        # Normalize and turn to dB scale
        z /= np.max(z)
        z = np.clip(z, 10**(-100/20), np.max(z))
        z = 20 * np.log10(z)

        # Smoothen
        z = ndimage.uniform_filter(z, size=3, mode='constant')
        t, f = np.meshgrid(t, f)

        # Smoothing creates "walls", remove them
        t = t[1:-1, :-1] * 1000  # Milliseconds
        f = f[1:-1, :-1]
        z = z[1:-1, :-1]

        # Surface plot
        ax.plot_surface(t, f, z, rcount=len(t), ccount=len(f), cmap='magma', antialiased=True, vmin=-100, vmax=0)

        # Z axis
        ax.set_zlim([-100, 0])
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # X axis
        ax.set_xlim([0, None])
        ax.set_xlabel('Time (ms)')

        # Y axis
        ax.set_ylim(np.log10([20, 20000]))
        ax.set_ylabel('Frequency (Hz)')
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{10 ** x:.0f}'))

        # Orient
        ax.view_init(30, 30)

        return fig, ax
