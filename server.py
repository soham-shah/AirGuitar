import numpy as np
import pyaudio
from GuitarString import GuitarString
import time
from flask import Flask, request, jsonify

# run the thing: export FLASK_APP=server.py 
# flask run --host=0.0.0.0

app = Flask(__name__)

@app.route('/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    parseRequest(content)
    return jsonify({"uuid":uuid})

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)

def map(x):
	return round((x-5.)/(60.-5.) * (600.-50.) + 50.)

def encode(signal):
    interleaved = signal.flatten()
    out_data = interleaved.astype(np.float32).tostring()
    return out_data

def callback(in_data, frame_count, time_info, flag):
    global strings
    result = np.zeros((len(strings),frame_count))
    for index, string in enumerate(strings):
        result[index] = string.get_pluck(frame_count)
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

trigWaitTime = 10 #amount of iterations to wait
trigWait = 0
strings = []
def parseRequest(content):
	global strings, trigWait, trigWaitTime
	strings = removeStrings(strings)
	if (content["ultra"] != 0):
		if (trigWait == 0):
			# add the things to what's being played so far
			basePitch = map(content["ultra"])
			delay = 0
			if(content["fing1"] == True):
				strings = createString(strings,basePitch,delay)
				delay += 50
			if(content["fing2"] == True):
				strings = createString(strings,basePitch + 20, delay)
				delay += 50
			if(content["fing3"] == True):
				strings = createString(strings,basePitch + 30, delay)
				delay += 50
			if(content["fing4"] == True):
				strings = createString(strings,basePitch + 40, delay)
				delay += 50
			# restart the timer
			trigWait = trigWaitTime
	if (trigWait != 0):
		trigWait -= 1

def createString(strings,freq, start):
	#check if it exists
	exists = False
	for string in strings:
		if abs(freq - string.pitch) < 20:
			exists = True
			print("prevented")
	
	if (not exists):
		fs = 8000 #sampling rate of 8000 hz
		stretch = 5* freq/98. if 2* freq/98. >= 1 else .5 
		# print(stretch)
		string = GuitarString(freq, start, fs, stretch)
		strings.append(string)
	
	return strings

def removeStrings(s):
	return [string for string in s if string.loc <= 10000]
