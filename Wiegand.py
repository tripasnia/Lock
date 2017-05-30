import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)
GPIO.setup(21,GPIO.IN)

bits = ''
timeout = 5
def one(channel):
    #global bits
    #bits = bits + '1'
    #timout = 5
    print('1')

def zero(channel):
    #global bits
    #bits = bits + '0'
    #timeout = 5
    print('0')

GPIO.add_event_detect(23, GPIO.FALLING, callback=one)
GPIO.add_event_detect(24, GPIO.FALLING, callback=zero)

print('Present Card')
while 1:       
    #if len(bits) == 26:
        #time.sleep(0.1)
        #print(25 * '-')
        #print('Binary:',bits)
        #print('Decimal:',int(str(bits),2))
        #print('Hex:',hex(int(str(bits),2)))
        #bits = ''
        #time.sleep(0.1)
    bits = bits + '1'



            
