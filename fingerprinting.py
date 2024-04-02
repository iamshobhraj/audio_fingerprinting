import os
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive 'Agg' backend

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from decoder import decoder


audio_data, sample_rate = decoder("Dreams.mp3")
# Calculate the time array
time = np.arange(len(audio_data)) / sample_rate
plt.figure(figsize=(12, 4))
plt.plot(time, audio_data)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Audio Data')
# Save the plot as an image file
plt.savefig('audio_data2.png', dpi=300, bbox_inches='tight')

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

# Save the spectrogram plot as a PNG file
plt.figure(figsize=(12, 6))
plt.pcolormesh(t, f, Zxx_db, cmap=cmap)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.colorbar()
plt.title('Spectrogram')
plt.savefig('spectrogram2.png', dpi=300, bbox_inches='tight')
print(len(time))
print("Spectrogram saved as 'spectrogram2.png'")

# Define the frame size and overlap for splitting the spectrogram
frame_size = 8192  # Adjust as needed
frame_overlap = frame_size // 2  # 50% overlap

# Split the spectrogram into frames
frames = []
start = 0
end = frame_size
while end <= Zxx_db.shape[2]:
    frames.append(Zxx_db[:, start:end])
    start += frame_size - frame_overlap
    end = start + frame_size

# Set the output folder
output_folder = 'spectrogrum'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Save each frame as a separate image file
for i, frame in enumerate(frames):
    output_file = os.path.join(output_folder, f'spectrogram_frame_{i}.png')
    print("Frame dimensions:", frame.shape)
    print("Time array dimensions:", t.shape)
    plt.figure(figsize=(6, 4))
    plt.pcolormesh(t[:frame.shape[1]], f, frame, cmap=cmap)
    print("Time slice:", t[:frame.shape[1]])
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.colorbar()
    plt.title(f'Spectrogram Frame {i}')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Spectrogram frame {i} saved as '{output_file}'")
