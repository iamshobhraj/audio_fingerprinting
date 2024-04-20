import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from scipy.signal import ShortTimeFFT
from scipy.signal.windows import hann
from preprocessing import preprocessing
from scipy.signal import butter, filtfilt
from scipy.ndimage import maximum_filter
from get2Dpeaks import get_2D_peaks
from genhashes import generate_hashes

def fingerprint(input_file, plot: bool = False):
    # Load the audio data
    audio_data, fs = preprocessing(input_file)
    # Define filter parameters
    highpass_cutoff_frequency = 300  # Cutoff frequency for the high-pass filter (in Hz)
    lowpass_cutoff_frequency = 2600   # Cutoff frequency for the low-pass filter (in Hz)
    filter_order = 6                  # Order of the filter
    # Design high-pass filter
    highpass_b, highpass_a = butter(filter_order, highpass_cutoff_frequency, btype='high', fs=fs)
    # Design low-pass filter
    lowpass_b, lowpass_a = butter(filter_order, lowpass_cutoff_frequency, btype='low', fs=fs)
    # Apply high-pass filter
    haudio_data = filtfilt(highpass_b, highpass_a, audio_data)
    # Apply low-pass filter
    audio_data = filtfilt(lowpass_b, lowpass_a, haudio_data)


    audio_length_seconds = len(audio_data) / fs
    T_x, N = 1/fs, len(audio_data)
    t_x = np.arange(N) * T_x  # time indexes for signal

    f_i = 5e-3*(t_x - t_x[N // 3])**2 + 1  # varying frequency
    # Window parameters
    window_length = 1024
    hop_size = 32

    # window fn
    w = hann(window_length, sym=True)

    # Calculate the STFT
    SFT = ShortTimeFFT(w, hop=hop_size, fs=fs, scale_to='psd')
    Sx = SFT.spectrogram(audio_data)


    # Divide frequency bins into logarithmic bands
    log_bands = 6
    log_band_indices = np.logspace(0, np.log2(Sx.shape[0]), num=log_bands, base=2, dtype=int)
    band_maximums = np.maximum.reduceat(Sx, log_band_indices, axis=0)

    # Apply max filter to the spectrogram
    filtered_Sx = maximum_filter(Sx, size=(26, 26))  # Adjust the size of the filter as needed

    # Find peaks by comparing filtered image with original image
    peak_mask = (filtered_Sx == Sx)
    peak_locations = np.argwhere(peak_mask)


    # Calculate the total number of peaks
    total_peaks = peak_locations.shape[0]

    print("Total number of peaks:", total_peaks)

    # Calculate time axis in seconds
    time_axis = np.arange(Sx.shape[1]) * hop_size / fs
    # Calculate frequency axis in Hz
    freq_resolution = fs / window_length
    frequencies = np.arange(window_length // 2 + 1) * freq_resolution

    # Extract peak frequencies and times from the spectrogram matrix
    peak_frequencies = frequencies[peak_locations[:, 0]]
    peak_times = time_axis[peak_locations[:, 1]]

    # Combine peak frequencies and times into tuples
    peaks = list(zip(peak_frequencies, peak_times))

    hashes = generate_hashes(peaks=peaks)
    return hashes

    if plot:
        # Plot the spectrogram
        plt.figure(figsize=(10, 6))
        plt.imshow(10 * np.log10(Sx + (1e-10)), aspect='auto', origin='lower', cmap='magma', extent=[time_axis[0], time_axis[-1], frequencies[0], frequencies[-1]])
        plt.colorbar(label='Intensity (dB)')
        plt.ylabel('Frequency Bin')
        plt.xlabel('Time Frame')
        plt.title('Spectrogram')
        plt.ylim(0, 4000)
        plt.savefig('fuckersizzz', dpi=300, bbox_inches='tight')

        # Plot only the peaks as red dots
        plt.figure(figsize=(10, 6))
        plt.scatter(time_axis[peak_locations[:, 1]], frequencies[peak_locations[:, 0]], color='red', s=1, marker='.')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Peaks Detected in Spectrogram')
        plt.xlim(time_axis[0], time_axis[-1])
        plt.ylim(0, 2500)
        plt.savefig('peaks_onlyzzz.png', dpi=300, bbox_inches='tight')

    


