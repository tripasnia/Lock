# 'Breathe' an LED, change speed with button-press

import RPi.GPIO as GPIO
import math # For the Sine function
import time # For sleep() delay

# Pin Number Definitions
pwmPin = 18
ledPin = 23

# Function to simplify calling the sine function
def sin(x):
    return math.sin(x)

# Linearly map an input scale to an output scale. This can be used
# to map the sin function (-1 to 1) into a duty cycle (0 to 100)%
def mapFun(x, inLo, inHi, outLo, outHi):
    inRange = inHi - inLo
    outRange = outHi - outLo
    inScale = (x - inLo) / inRange  # normalised input (0 to 1)
    return outLo + (inScale * outRange) # map normalised input to output
    

GPIO.setmode(GPIO.BCM)          # Use Broadcom pin-numbering
GPIO.setup(ledPin,GPIO.OUT)     # Setup an ouptut pins
GPIO.setup(pwmPin,GPIO.OUT)


pwm = GPIO.PWM(pwmPin, 200)     # Initialise PWM channel at 200Hz

GPIO.output(ledPin, GPIO.LOW)   # LED off
pwm.start(0)                    # Initialise PWM with 0 duty


#### Main Loop ####

x = 0
try:
    while 1:
        # Decide how fast to breathe the LED

        duty = mapFun(sin(x),-1,1,0,100) # Call our special map function
        x += step                        # Equivalent to: x = x + step
        pwm.ChangeDutyCycle(duty)
        #print(duty)
        # If you want to remove the print, make sure you have a time.sleep
        # Otherwise the program will run too fast and spoil the effect.
        time.sleep(0.01)
        if x >= 2*math.pi:               # Keep x bounded (0 to 2Pi)
            x = 0

            
            

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print('Halted Cleanly')
