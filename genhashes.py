import numpy as np
from scipy.ndimage import maximum_filter
import hashlib
from typing import List, Tuple

def get_peaks(S, amp_min=10):
    """
    Find local maxima (peaks) in a spectrogram magnitude array S.
    Returns: List of (frequency_bin, time_bin)
    """
    neighborhood_size = (20, 10)  # freq x time
    local_max = maximum_filter(S, size=neighborhood_size) == S
    detected_peaks = np.argwhere(local_max & (S > amp_min))
    # Each peak is (freq_bin, time_bin)
    return [(int(f), int(t)) for f, t in detected_peaks]

def generate_hashes(peaks: List[Tuple[int, int]], fan_value: int = 5) -> List[Tuple[str, int]]:
    """
    Generate robust hashes from peak pairs (like Shazam).
    Returns: List of (hash, time_offset)
    """
    idx_freq = 0
    idx_time = 1
    peaks.sort(key=lambda x: x[1])  # sort by time
    hashes = []
    for i, (freq1, t1) in enumerate(peaks):
        for j in range(1, fan_value):
            if i + j < len(peaks):
                freq2, t2 = peaks[i + j]
                t_delta = t2 - t1
                if 0 < t_delta <= 200:
                    h = hashlib.sha1(f"{freq1}|{freq2}|{t_delta}".encode('utf-8'))
                    hash_val = h.hexdigest()[0:20]
                    hashes.append((hash_val, t1))
    return hashes