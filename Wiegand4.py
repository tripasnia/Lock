import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN)
GPIO.setup(24,GPIO.IN)
GPIO.setup(21,GPIO.IN)



while True:
    bits = ''
    i = 0
    GPIO.wait_for_edge(21,GPIO.RISING)
    while i<26:
        if GPIO.input(23) == 1:
            bits = bits + '1'
        else:
            bits = bits + '0'
        i = i + 1
        time.sleep(0.0015)
    print(25 * '-')
    print('Binary:',bits)
    print('Decimal:',int(str(bits),2))
    print('Hex:',hex(int(str(bits),2)))
    bits = ''
    input()
    



GPIO.cleanup()
    
