import numpy as np
from pydub import AudioSegment
import librosa
from genhashes import get_peaks, generate_hashes

def preprocess(input_file):
    audio = AudioSegment.from_file(input_file, format=input_file.split(".")[-1])
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(8192)
    audio = audio.set_sample_width(2)
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.int16)
    sample_rate = audio.frame_rate
    return audio_data, sample_rate

def extract_fingerprint(filepath):
    audio_data, sample_rate = preprocess(filepath)
    audio_float = audio_data.astype(np.float32)
    if np.max(np.abs(audio_float)) > 0:
        audio_float /= np.max(np.abs(audio_float))
    S = np.abs(librosa.stft(audio_float, n_fft=2048, hop_length=512))
    peaks = get_peaks(S, amp_min=10)
    hashes = generate_hashes(peaks, fan_value=5)
    return hashes