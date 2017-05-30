import serial
import time
ser = serial.Serial('/dev/ttyAMA0',9600)
while True :
    data = ser.readline
    print(data)
    ser.close()
    
    
