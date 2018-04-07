import RPi.GPIO as GPIO

fing1 = 6
fing2 = 13
fing3 = 19
fing4 = 26
GPIO.setmode(GPIO.BCM)

GPIO.setup(fing1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(fing2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(fing3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(fing4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
    if (GPIO.input(fing1) == 0):
        print("fing1")
    if (GPIO.input(fing2) == 0):
        print("fing2")
    if (GPIO.input(fing3) == 0):
        print("fing3")
    if (GPIO.input(fing4) == 0):
        print("fing4")
    