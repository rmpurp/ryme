from audiotsm import phasevocoder
import numpy as np
from audiotsm import wsola 
from audiotsm.io.wav import WavReader, WavWriter
from audiotsm.io.array import ArrayReader
from progressbar import ProgressBar
from scipy.io import wavfile
import ffmpeg

input_filename = "cs170.wav"
output_filename = "out.wav"


def group(lst, n):
    """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]
    
    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.
    
    >>> group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    return zip(*[lst[i::n] for i in range(n)]) 


print(f"Reading {input_filename}")
rate, data = wavfile.read(input_filename)


condition = np.abs(data[:,0]) < 100

min_removal_time = rate // 100
print("Finding removal times...")
lens = np.diff(np.where(np.concatenate(([True], condition[:-1] != condition[1:], [True])))[0])
times = np.cumsum(lens)
print(f"Removal times: {times}")

should_remove = condition[0]


run_beg = -1
top = len(condition)

start = 1 if should_remove else 0

for beg, end in group(times[start:], 2):
    if (end - beg < min_removal_time):
        condition[beg: end] = [False] * (end - beg)
    else:
        condition[beg: beg + min_removal_time // 2] = [False] * (min_removal_time // 2)
        condition[end - min_removal_time // 2 : end] = [False] * (min_removal_time // 2)


# lens = np.diff(np.where(np.concatenate(([True], condition[:-1] != condition[1:], [True])))[0])
# times = np.cumsum(lens)

print("Writing...")
wavfile.write(output_filename, rate, data[~np.array(condition)])


# reader = WaveReader(input_filename, )

# with WavWriter(output_filename, reader.channels, rate) as writer:
#    tsm = wsola(reader.channels, speed=1)
#    tsm.run(reader, writer)

