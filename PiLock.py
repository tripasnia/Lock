#!/usr/bin/env python

import time
from threading import Thread
import serial
import pymysql
import RPi.GPIO as GPIO
import datetime


Local = pymysql.connect(host='localhost',user='eLock',passwd='lockpw',db='eLock',autocommit=True)
inCursor = Local.cursor()
inQuery = '''SELECT CARD_ID from Access;'''

global lastRead 
global valid
global lockName
lockName = 'TestLock'

outCursor = Local.cursor()

def detectSerial():
    #Find which tty the Arduino is connected to, dynamically assigned on connect
    serialPort = ''
    try:
        ser = serial.Serial('/dev/ttyACM0',9600)
        while ser.read():
            serialPort = '/dev/ttyACM0'
            break
        ser.close()
    except:
        pass
    try:
        ser = serial.Serial('/dev/ttyACM1',9600)
        while ser.read():
            serialPort = '/dev/ttyACM1'
            break
        ser.close()
    except:
        pass
    try:
        ser = serial.Serial('/dev/ttyACM2',9600)
        while ser.read():
            serialPort = '/dev/ttyACM2'
            break
        ser.close()
    except:
        pass
    return serialPort

def PullAccess():
    #Pull Access from Ricview
    while True:
        try:
            Ricview = pymysql.connect(host='50.62.209.119',user='richmondavl',passwd='RicAVL123',db='Ricview')
            inCursor = Ricview.cursor()
            inQuery = '''Select Card_ID,LastName,FirstName from Ambulance_Access;'''
            inCursor.execute(inQuery)
            Local = pymysql.connect(host='localhost',user='eLock',passwd='lockpw',db='eLock',autocommit=True)
            outCursor = Local.cursor()
            outCursor.execute('''DELETE FROM Access;''')
            for (Card_ID,LastName,FirstName) in inCursor:
                inDictionary = {'Card_ID': Card_ID,'LastName': LastName,'FirstName': FirstName}
                outQuery = '''INSERT INTO Access (Card_ID,LastName,FirstName) VALUES (%(Card_ID)s,%(LastName)s,%(FirstName)s);'''
                outCursor.execute(outQuery,inDictionary)
        except:
            pass
        time.sleep(10)

def PushLog():
    #Push Access to Ricview
    while True:
        try:
            Local = pymysql.connect(host='localhost',user='eLock',passwd='lockpw',db='eLock',autocommit=True)
            inCursor = Local.cursor()
            inQuery = '''SELECT Card_ID,LockName,AccessStatus,AccessDateTime FROM AccessLog;'''
            inCursor.execute(inQuery)
            Ricview = pymysql.connect(host='50.62.209.119',user='richmondavl',passwd='RicAVL123',db='Ricview')
            outCursor = Ricview.cursor()
            for (Card_ID,LockName,AccessStatus,AccessDateTime) in inCursor:
                outDictionary = {'AccessDateTime': AccessDateTime,'AccessStatus': AccessStatus, 'Card_ID': Card_ID, 'LockName': LockName}
                outQuery = '''INSERT INTO AccessLog (Card_ID, LockName, AccessStatus,AccessDateTime) VALUES (%(Card_ID)s,%(LockName)s,%(AccessStatus)s,%(AccessDateTime)s);'''
                outCursor.execute(outQuery,outDictionary)
            inCursor.execute('''DELETE FROM AccessLog;''')        
        except:
            pass
        time.sleep(10)

def Check(lastRead):
    try:
        valid = 0
        inCursor.execute(inQuery)
        results = inCursor.fetchall()
        for row in results:
            Card_ID = row[0]
            if str(Card_ID) == str(lastRead):
                valid = 1
        if valid == 1:
            return 1
        else:
            return 0
    except:
        pass

def WriteGranted(lastRead):
    try:
        outDictionary = {'AccessDateTime': datetime.datetime.now(),'AccessStatus': 'Granted', 'Card_ID': lastRead, 'LockName': lockName}
        outQuery = '''INSERT INTO AccessLog (Card_ID, LockName, AccessStatus,AccessDateTime) VALUES (%(Card_ID)s,%(LockName)s,%(AccessStatus)s,%(AccessDateTime)s);'''
        outCursor.execute(outQuery,outDictionary)
    except:
        pass

def WriteDenied(lastRead):
    try:
        outDictionary = {'AccessDateTime': datetime.datetime.now(),'AccessStatus': 'Denied', 'Card_ID': lastRead, 'LockName': lockName}
        outQuery = '''INSERT INTO AccessLog (Card_ID, LockName, AccessStatus,AccessDateTime) VALUES (%(Card_ID)s,%(LockName)s,%(AccessStatus)s,%(AccessDateTime)s);'''
        outCursor.execute(outQuery,outDictionary)
    except:
        pass

def Scan():
    ser = serial.Serial(detectSerial(),9600)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)
    while True:
        valid = 0
        checkString = (ser.readline())
        checkString = str(checkString,'ascii')
        checkFacility = checkString[19:22]
        if checkFacility == '246':
            checkCard = checkString[29:34]
            shouldOpen = Check(checkCard)
            if shouldOpen == 1:
                print('Opening...')
                GPIO.output(4,True)
                time.sleep(1)
                print('Closing')
                GPIO.output(4,False)
                valid = 0
                print('-'*25)
                WriteGranted(checkCard)
            else:
                print('Access Denied')
                print('-'*25)
                WriteDenied(checkCard)
        


def main():
    PullThread = Thread(target=PullAccess)
    PullThread.start()
    PushThread = Thread(target=PushLog)
    PushThread.start()
    ScanThread = Thread(target=Scan)
    ScanThread.start()
    while True:
        if (not ScanThread.isAlive()):
            GPIO.cleanup()
            break;


if __name__=='__main__':
    main()
