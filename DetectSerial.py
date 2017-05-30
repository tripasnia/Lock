import serial

serialPort = ''
ser = serial


try:
    ser = serial.Serial('/dev/ttyACM0',9600)
    while ser.read():
        #global serialPort
        serialPort = '/dev/ttyACM0'
        print('ACM0')
        break
    ser.close()
except:
    pass

try:
    ser = serial.Serial('/dev/ttyACM1',9600)
    while ser.read():
        #global serialPort
        serialPort = '/dev/ttyACM1'
        print('ACM1')
        break
    ser.close()
except:
    pass

try:
    ser = serial.Serial('/dev/ttyACM2',9600)
    while ser.read():
        #global serialPort
        serialPort = '/dev/ttyACM2'
        print('ACM2')
        break
    ser.close()
except:
    pass

try:
    print('Found: ' + serialPort)
except:
    print('Error')
