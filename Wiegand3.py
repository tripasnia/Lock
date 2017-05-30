import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21,GPIO.IN, pull_up_down=GPIO.PUD_UP)

print('Present Card')

bits = ''
timeout = 5

def read(channel):
    global bits
    while GPIO.input(21)==1:
        if GPIO.input(23) == 1:
            bits = bits + '1'
        else:
            bits = bits + '0'
        time.sleep(0.0015)
    print(25 * '-')
    print('Binary:',bits[:26])
    print('Decimal:',int(str(bits[:26]),2))
    print('Hex:',hex(int(str(bits[:26]),2)))
    bits = ''
    


GPIO.add_event_detect(21, GPIO.RISING, callback=read)
    

while GPIO.input(21) == GPIO.LOW:
    time.sleep(0.001)


GPIO.cleanup()
    



            
