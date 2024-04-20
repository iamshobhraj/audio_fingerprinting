import sys
from scipy.io import wavfile
from pydub import AudioSegment
import numpy as np

def preprocessing(input_file):
    # Load the audio file
    audio = AudioSegment.from_file(input_file, format=input_file.split(".")[-1])

    # Convert stereo to mono
    audio = audio.set_channels(1)
    
    # Set sample rate
    audio = audio.set_frame_rate(8192)

    # Set sample width (bit depth) to 16 bits
    audio = audio.set_sample_width(1)
    
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.int16)
    sample_rate = audio.frame_rate
    
    return audio_data, sample_rate

