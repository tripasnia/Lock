import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)
GPIO.setup(21,GPIO.IN)

print('Present Card')

bits = ''
timeout = 5

def readFirst(channel):
    global bits
    while GPIO.input(21) ==1:
        if(GPIO.input(23) --1):
            bits = bits + '1'
        else:
            bits = bits + '0'

def one(channel):
    global bits
    #bits = bits + '1'
    #timout = 5  

def zero(channel):
    global bits
    #bits = bits + '0'
    #timeout = 5

GPIO.add_event_detect(23, GPIO.RISING, callback=one)
GPIO.add_event_detect(24, GPIO.RISING, callback=zero)
GPIO.add_event_detect(21, GPIO.RISING, callback=readFirst)
    

#while GPIO.input(21) == GPIO.LOW:
    #time.sleep(0.01)



while 1:
    if len(bits) == 26:
        time.sleep(0.1)
        print(25 * '-')
        print('Binary:',bits[:26])
        print('Decimal:',int(str(bits[:26]),2))
        print('Hex:',hex(int(str(bits[:26]),2)))
        bits = ''
GPIO.cleanup()
    



            
