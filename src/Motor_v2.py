import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
AN2 = 12
AN1 = 13
DIG2 = 19 
DIG1 = 16 

GPIO.setup(AN2, GPIO.OUT)
GPIO.setup(AN1, GPIO.OUT)
GPIO.setup(DIG2, GPIO.OUT)
GPIO.setup(DIG1, GPIO.OUT)
sleep(1)
p1 = GPIO.PWM(AN1, 100)
p2 = GPIO.PWM(AN2, 100)

try:
    while True:
        print("Forward")
        GPIO.output(DIG1, GPIO.HIGH)
        GPIO.output(DIG2, GPIO.HIGH)
        p1.start(50)
        p2.start(50)
        sleep(5)
        
        print("Backward")
        GPIO.output(DIG1, GPIO.LOW)
        GPIO.output(DIG2, GPIO.LOW)
        p1.start(50)
        p2.start(50)
        sleep(5)
except:
    p1.start(0)
    p2.start(0)
