import numpy as np
import pyaudio
from GuitarString import GuitarString
import time

# initialize the different guitar strings
fs = 8000 #sampling rate of 8000 hz
freqs = [100, 125, 150, 175, 200, 225, 250]
stretch_factors = [2 * f/98 for f in freqs]
strings = []
for freq, stretch_factor in zip(freqs, stretch_factors):
    string = GuitarString(freq, 0, fs, stretch_factor)
    strings.append(string)

# guitar_sound = [sum(string.get_sample() for string in strings) for _ in range(fs * 6)]
# x = np.array(guitar_sound)

tunes = [string.get_pluck(40000) for string in strings]
track_loc = [0 for _ in strings]
plucked = [False for i in freqs]
frame_count_global = 0

def callback(in_data, frame_count, time_info, flag):
    global plucked, frame_count_global
    # print("got callback")
    result = np.zeros(frame_count)
    frame_count_global = frame_count
    for index, value in enumerate(plucked):
        if value == True:
            curr_loc = track_loc[index]
            result = tunes[index][curr_loc:curr_loc+frame_count]
            track_loc[index] += frame_count
            if track_loc[index] > 40000:
                plucked[index] = False
                track_loc[index] = 0

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
        ch = raw_input("Press q, w, e, r to plunk a stering (p to quit): ")
    except:
        pass
    if ch == 'q':
        plucked[0] = True
    if ch == 'w':
        plucked[1] = True
    if ch == 'e':
        plucked[2] = True
    if ch == 'r':
        plucked[3] = True
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
