import numpy as np
import pyaudio
from GuitarString import GuitarString
import time
# import matplotlib.pyplot as plt
# initialize the different guitar strings
fs = 8000 #sampling rate of 8000 hz
freqs = [50, 500, 1000, 175, 200, 225, 250]
stretch_factors = [2 * f/98. for f in freqs]
strings = []
for freq, stretch_factor in zip(freqs, stretch_factors):
    string = GuitarString(freq, 0, fs, stretch_factor)
    strings.append(string)

# guitar_sound = [sum(string.get_sample() for string in strings) for _ in range(fs * 6)]
# x = np.array(guitar_sound)

tunes = [string.get_pluck(50000) for string in strings]
track_loc = [0 for _ in strings]
# plucked = [False for i in freqs]

def encode(signal):
    # Convert a 2D numpy array into a byte stream for PyAudio.
    # Signal has chunk_size rows and channels columns.
    interleaved = signal.flatten()
    out_data = interleaved.astype(np.float32).tostring()
    return out_data

def callback(in_data, frame_count, time_info, flag):
    global tunes, track_loc
    # print("got callback")
    result = np.zeros((len(track_loc),frame_count))
    for index, value in enumerate(track_loc):
        if track_loc[index] != 0:
            curr_loc = track_loc[index]
            result[index] = tunes[index][curr_loc:curr_loc+frame_count]
            track_loc[index] += frame_count
            if track_loc[index] > 48000:
                track_loc[index] = 0
    result = encode(np.sum(result,axis=0))
    return (result, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
    channels=1,
    rate=10000,
    output=True,
    output_device_index=1,
    stream_callback=callback
    )
stream.start_stream()

loop = True
while loop:
    # time.sleep(0.1) # 0.5
    ch = ""
    try:
        ch = raw_input("Press q, w, e, r to plunk a string (p to quit): ")
    except:
        pass
    if ch == 'q':
        track_loc[0] = 1
    if ch == 'w':
        track_loc[1] = 1
    if ch == 'e':
        track_loc[2] = 1
    if ch == 'r':
        track_loc[3] = 1
    if ch == 'p':
        # Exit and write to file.
        loop = False
        stream.stop_stream()
        time.sleep(1)
    else:
        pass
stream.stop_stream()
stream.close()

p.terminate()

# data = x.astype(np.float32).tostring()
# stream.write(data)
