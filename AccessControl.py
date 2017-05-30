import RPi.GPIO as GPIO
import time
import serial
import datetime
import time
import pymysql

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)

ser = serial.Serial('/dev/ttyACM1',9600)
Local = pymysql.connect(host='localhost',user='eLock',passwd='lockpw',db='eLock',autocommit=True)
inCursor = Local.cursor()
inQuery = '''SELECT CARD_ID from Access;'''

global lastRead 
global valid
global lockName
lockName = 'TestLock'

outCursor = Local.cursor()


def Check(lastRead):
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

def WriteGranted(lastRead):
    outDictionary = {'AccessDateTime': datetime.datetime.now(),'AccessStatus': 'Granted', 'Card_ID': lastRead, 'LockName': lockName}
    outQuery = '''INSERT INTO AccessLog (Card_ID, LockName, AccessStatus,AccessDateTime) VALUES (%(Card_ID)s,%(LockName)s,%(AccessStatus)s,%(AccessDateTime)s);'''
    outCursor.execute(outQuery,outDictionary)

def WriteDenied(lastRead):
    outDictionary = {'AccessDateTime': datetime.datetime.now(),'AccessStatus': 'Denied', 'Card_ID': lastRead, 'LockName': lockName}
    outQuery = '''INSERT INTO AccessLog (Card_ID, LockName, AccessStatus,AccessDateTime) VALUES (%(Card_ID)s,%(LockName)s,%(AccessStatus)s,%(AccessDateTime)s);'''
    outCursor.execute(outQuery,outDictionary)

while True :
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

GPIO.cleanup()
