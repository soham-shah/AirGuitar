import requests
import time
import RPi.GPIO as GPIO

url = 'http://10.202.182.217:5000/1234'

# define which pins are being used
fing1 = 6
fing2 = 13
fing3 = 19
fing4 = 26
TRIG = 14
ECHO = 15

#init the pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(fing1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(fing2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(fing3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(fing4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

while True:
    # init defualt message
    mesg = {"fing1":False,"fing2":False,"fing3":False,"fing4":False,"ultra":0.0}

    # test which finger is touching
    if (GPIO.input(fing1) == 0):
        mesg["fing1"] = True
    if (GPIO.input(fing2) == 0):
        mesg["fing2"] = True
    if (GPIO.input(fing3) == 0):
        mesg["fing3"] = True
    if (GPIO.input(fing4) == 0):
        mesg["fing4"] = True
    
    GPIO.output(TRIG, False)                 #Set TRIG as LOW
    time.sleep(.01)                           #Delay of for the read

    GPIO.output(TRIG, True)                  #Set TRIG as HIGH
    time.sleep(0.00001)                      #Delay of 0.00001 seconds
    GPIO.output(TRIG, False)                 #Set TRIG as LOW

    while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
        pulse_start = time.time()                #Saves the last known time of LOW pulse

    while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
        pulse_end = time.time()                  #Saves the last known time of HIGH pulse 

    pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

    distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
    distance = round(distance, 2)            #Round to two decimal points

    if distance > 2 and distance < 100:      #Check whether the distance is within range
        mesg["ultra"] = distance             #Print distance with 0.5 cm calibration
    
    #post the final thing out
    res = requests.post(url, json=mesg)

