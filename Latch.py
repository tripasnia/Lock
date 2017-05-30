import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH)

while True:
    GPIO.output(4, True)
    time.sleep(0.5)
    GPIO.output(4, False)
    time.sleep(10)

GPIO.cleanup()

            
            

