import os
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive 'Agg' backend

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from decoder import decoder

# Set the output folder
output_folder = 'specs'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

audio_data, sample_rate = decoder("Dreams.mp3")

# Define the window length and overlap
window_length = 1024  # Adjust as needed
overlap = window_length // 2  # 50% overlap

# Compute the STFT
f, t, Zxx = signal.stft(audio_data, sample_rate, window='hann', nperseg=window_length, noverlap=overlap, nfft=None, detrend=False, return_onesided=True, boundary='zeros', padded=True)

# Convert to decibel scale
Zxx_db = 20 * np.log10(np.abs(Zxx) + 1e-10)

# Create a custom colormap
import matplotlib.colors as mcolors
cmap = mcolors.LinearSegmentedColormap.from_list('custom', ['green', 'yellow', 'red'])

# Define the frame size and overlap for splitting the spectrogram
frame_size = 8129  # Adjust as needed
frame_overlap = frame_size // 2  # 50% overlap

# Split the spectrogram into frames
frames = []
start = 0
end = frame_size
while end <= Zxx_db.shape[1]:
    frames.append(Zxx_db[:, start:end])
    start += frame_size - frame_overlap
    end = start + frame_size

# Save each frame as a separate image file
for i, frame in enumerate(frames):
    output_file = os.path.join(output_folder, f'spectrogram_frame_{i}.png')
    plt.figure(figsize=(6, 4))
    plt.pcolormesh(t[:frame.shape[1]], f, frame, cmap=cmap)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.title(f'Spectrogram Frame {i}')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Spectrogram frame {i} saved as '{output_file}'")
