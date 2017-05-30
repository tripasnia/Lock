import RPi.GPIO as GPIO
import time
import datetime

import urllib.request
from xml.dom import minidom

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)


while True:
            try:
                usock = urllib.request.urlopen('http://www.ricview.org/DM.XML')
                xmldoc = minidom.parse(usock)
                for element in xmldoc.getElementsByTagName('W'):
                    W = int(element.firstChild.nodeValue)
                for element in xmldoc.getElementsByTagName('R'):
                    R = int(element.firstChild.nodeValue)
                for element in xmldoc.getElementsByTagName('T'):
                    T = int(element.firstChild.nodeValue)
            except:
                pass
            if W > 43200:
                GPIO.output(17, False)
                GPIO.output(27, False)
                GPIO.output(22, False)
            elif W > 3600:
                GPIO.output(17, True)
                GPIO.output(27, False)
                GPIO.output(22, False)
            elif W > 300:
                GPIO.output(17, False)
                GPIO.output(27, True)
                GPIO.output(22, False)
            else:
                GPIO.output(17, False)
                GPIO.output(27, False)
                GPIO.output(22, True)

            if R > 43200:
                GPIO.output(5, False)
                GPIO.output(6, False)
                GPIO.output(13, False)
            elif R > 3600:
                GPIO.output(5, True)
                GPIO.output(6, False)
                GPIO.output(13, False)
            elif R > 300:
                GPIO.output(5, False)
                GPIO.output(6, True)
                GPIO.output(13, False)
            else:
                GPIO.output(5, False)
                GPIO.output(6, False)
                GPIO.output(13, True)

            if T > 43200:
                GPIO.output(19, False)
                GPIO.output(26, False)
            elif T > 3600:
                GPIO.output(19, False)
                GPIO.output(26, False)
            elif T > 300:
                GPIO.output(19, True)
                GPIO.output(26, False)
            else:
                GPIO.output(19, False)
                GPIO.output(26, True)  
            time.sleep(1)

GPIO.cleanup()
