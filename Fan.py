import os
import time
import RPi.GPIO as GPIO

pin=18

maxTemp = 65
minTemp = 25
difTemp = maxTemp-minTemp

GPIO.setmode(GPIO.BCM)

GPIO.setup(pin, GPIO.OUT)

pwm = GPIO.PWM(pin,25000) #set to 25 Khz for pwm fan

def getCPUtemperature():
   res = os.popen('vcgencmd measure_temp').readline()
   temp =(res.replace("temp=","").replace("'C\n",""))
   #print(temp)
   return temp



def getTEMP():
   CPU_temp = float(getCPUtemperature())
   if CPU_temp<=minTemp:
      print(f'{CPU_temp}|{100.0}',end="\r")
      pwm.start(100)
   elif CPU_temp>minTemp:
      print(f'{CPU_temp}|{(((minTemp-CPU_temp)/difTemp)+1)*100:.2f}',end="\r")
      pwm.start((((minTemp-CPU_temp)/difTemp)+1)*100)
   elif CPU_temp>maxTemp:
      print(f'{CPU_temp}|{0.0}',end="\r")
      pwm.start(0)
   return()

try:
   while True:
      getTEMP()
      time.sleep(10) # Read the temperature every 5 sec, increase or decrease this limit if you want
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt 
   pwm.stop()
   GPIO.cleanup() # resets all GPIO ports used by this program
