import hashlib
from typing import List, Tuple
from operator import itemgetter

def generate_hashes(peaks: List[Tuple[int, int]], fan_value: int = 5) -> List[Tuple[str, int]]:
    """
    Generate hashes from a list of peak frequencies and times.

    :param peaks: A list of peak frequencies and times.
    :param fan_value: The degree to which a fingerprint can be paired with its neighbors.
    :return: A list of hashes with their corresponding offsets.
    """
    # Indices for accessing frequency and time in the tuples
    idx_freq = 0
    idx_time = 1

    # Sort peaks by time if needed
    if True:
        peaks.sort(key=itemgetter(1))

    hashes = []
    for i, (freq1, t1) in enumerate(peaks):
        # Iterate over neighboring peaks within the fan_value
        for j in range(1, fan_value):
            if i + j < len(peaks):
                freq2, t2 = peaks[i + j]

                # Calculate time difference between peaks
                t_delta = t2 - t1

                # Check if time difference falls within specified range
                if 0 <= t_delta <= 200:
                    # Generate hash using SHA-1 algorithm
                    h = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(t_delta)}".encode('utf-8'))

                    # Truncate hash to fixed length
                    hash_value = h.hexdigest()[0:20]

                    # Add hash and its corresponding time offset to the list
                    hashes.append((hash_value, t1))

    return hashes
