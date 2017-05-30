#!/usr/bin/env python3

import pymysql
import time


global lockType
lockType = 'Ambulance'

def GetAccess():
    #Pull Access from Ricview
    try:
        Ricview = pymysql.connect(host='50.62.209.119',user='richmondavl',passwd='RicAVL123',db='Ricview')
        inCursor = Ricview.cursor()
        inQuery = '''Select Card_ID from Ambulance_Access;'''
        inCursor.execute(inQuery)

        Local = pymysql.connect(host='localhost',user='Lock',passwd='lockpw',db='Lock',autocommit=True)
        outCursor = Local.cursor()
        outCursor.execute('''DELETE FROM Access;''')
        for (Card_ID) in inCursor:
            inDictionary = {'Card_ID': Card_ID}
            outQuery = '''INSERT INTO Access (Card_ID) VALUES (%(Card_ID)s);'''
            outCursor.execute(outQuery,inDictionary)
    except:
        pass

def PushLog():
    #Push Access to Ricview
    try:
        Local = pymysql.connect(host='localhost',user='Lock',passwd='lockpw',db='Lock',autocommit=True)
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

while True:
    try:
        GetAccess()
        PushLog()
        time.sleep(10)
    except:
        pass
