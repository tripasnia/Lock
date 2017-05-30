import RPi.GPIO as GPIO
import time

gpio_start = 19
gpio_end = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for x in range (gpio_start, gpio_end):
   GPIO.setup(x, GPIO.OUT)
   GPIO.setup(17, GPIO.OUT)
   GPIO.setup(27, GPIO.OUT)

while True:
   GPIO.output(17, True)
   GPIO.output(27, False)
   for y in range (gpio_start, gpio_end):
      GPIO.output(y, True)
      #print ('on ', y)
   time.sleep(.5)
   
   for z in range (gpio_start, gpio_end):
      GPIO.output(z, False)
      #print ('off ',z)
   
   GPIO.output(17, False)
   GPIO.output(27, True)
   time.sleep(10)
   
