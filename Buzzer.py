import RPi.GPIO as GPIO   #import the GPIO library
import time               #import the time library

class Buzzer(object):
 def __init__(self):
  GPIO.setmode(GPIO.BCM)  
  self.buzzer_pin = 22 #set to GPIO pin 22
  GPIO.setup(self.buzzer_pin, GPIO.IN)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)

 def __del__(self):
  class_name = self.__class__.__name__
  print (class_name, "finished")

 def buzz(self,pitch, duration):   #create the function “buzz” and feed it the pitch and duration)
 
  if(pitch==0):
   time.sleep(duration)
   return
  period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
  delay = period / 2     #calcuate the time for half of the wave  
  cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

  for i in range(cycles):    #start a loop from 0 to the variable “cycles” calculated above
   GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
   time.sleep(delay)    #wait with pin 18 high
   GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
   time.sleep(delay)    #wait with pin 18 low

 def play(self):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  x=0

  print("Playing tune ")

  pitches=[1047,261,1047,261,1047,261,1047,261,1047,261,1047,261]
  duration=0.1
  for p in pitches:
      self.buzz(p, duration)  #feed the pitch and duration to the function, “buzz”
      time.sleep(duration)




  GPIO.setup(self.buzzer_pin, GPIO.IN)

if __name__ == "__main__":
  buzzer = Buzzer()
  buzzer.play()
