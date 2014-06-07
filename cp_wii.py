#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# wii_remote_1.py
# Connect a Nintendo Wii Remote via Bluetooth
# and  read the button states in Python.
#
# Project URL :
# http://www.raspberrypi-spy.co.uk/?p=1101
#
# Author : Matt Hawkins
# Date   : 30/01/2013
 
# -----------------------
# Import required Python libraries
# -----------------------
import cwiid
import time
import string
import mosquitto
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")

broker = config.get("MQTT","broker")
port = int(config.get("MQTT","port")) 

button_delay = 0.1

arah = "1:1:"
LPWM = 0
RPWM = 0
MAXLPWM = 40
MAXRPWM = 40
is_last_stop = False
stop_count = 0

menu = ["print", "music", "main", "display", "light"]
selected_menu = "print"
last = 0

def on_connect(mosq, obj, rc):
  if rc==0:
    print "Connected broker"
  else:
    raise Exception


def on_publish(mosq, obj,val):
   pass


def sendCommand():
  global arah
  global LPWM
  global RPWM
  global is_last_stop
  global stop_count
  command = arah + str(LPWM) + ":" + str(RPWM) + ":#"
  if stop_count < 3:
    #print command
    MQ.publish("wii",command)
  else:
    pass
  #send command


def addPWM(l,r):
  global LPWM
  global RPWM
  global MAXLPWM
  global MAXRPWM
  global stop_count
  stop_count = 0
  if LPWM < MAXLPWM:
     LPWM = LPWM + l
  else:
     LPWM = MAXLPWM
  if RPWM < MAXRPWM:
     RPWM = RPWM + r
  else:
     RPWM = MAXRPWM
  sendCommand()
  
def subPWM(l,r):
  global LPWM
  global RPWM
  global stop_count
  if LPWM > 0:
    LPWM = LPWM - l
  else:
    LPWM = 0
  if RPWM > 0:
    RPWM = RPWM - r
  else:
    RPWM = 0
  if LPWM == 0 and RPWM == 0:
    stop_count = stop_count + 1
    arah = "1:1:"
  sendCommand()

def stop():
  global LPWM
  global RPWM
  global is_last_top
  LPWM = 0
  RPWM = 0
  sendCommand()
 
def getWii():
  try:
    print "press 1+2"
    wii=cwiid.Wiimote()
    print "connected"
    wii.rpt_mode = cwiid.RPT_BTN
    wiiconnected = True
    wii.led = 1
    return wii
  except:
    wiiconnected = False
    try:
      wii.close()
    except:
      pass
    print "retry to reconnect in 5 seconds"
    time.sleep(5)
 
def main():
  global arah
  global LPWM
  global RPWM
  global is_last_stop

  wii = getWii()

  while wii: 
    try:
      wii.request_status()
    except:
      print "DISCONNECTED"
      try:
        wii.close()
      except:
        pass
      wii = getWii()

    try: 
      buttons = wii.state['buttons']
    except:
      pass
 
    # If Plus and Minus buttons pressed
    # together then rumble and quit.
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
      print '\nClosing connection ...'
      try:
        wii.rumble = 1
        time.sleep(0.1)
        wii.rumble = 0
      except:
        pass
      try:
        wii.close()
      except:
        pass

 
    # Check if other buttons are pressed by
    # doing a bitwise AND of the buttons number
    # and the predefined constant for that button.

    if (buttons & cwiid.BTN_LEFT):
      if LPWM > 0 and RPWM > 0 and arah == "1:1:":
         addPWM(0,3)
         subPWM(1,0)
      else:
        arah = "0:1:"
        addPWM(3,3)
      sendCommand()
 
    if(buttons & cwiid.BTN_RIGHT):
      if LPWM > 0 and RPWM > 0 and arah == "1:1:":
         addPWM(3,0)
         subPWM(0,3)
      else:
         arah = "1:0:"
         addPWM(3,3)
      sendCommand()
 
    if (buttons & cwiid.BTN_UP):
      #print 'Up pressed'
      arah = "0:0:"
      addPWM(3,3)
      sendCommand()

 
    if (buttons & cwiid.BTN_DOWN):
      arah = "1:1:"
      addPWM(3,3)
      sendCommand()
 
    if (buttons & cwiid.BTN_1):
      MQ.publish("sound","rnd")
      time.sleep(1)
 
    if (buttons & cwiid.BTN_2):
      MQ.publish("speak","rnd")
      time.sleep(1)
 
    if (buttons & cwiid.BTN_A):
      MQ.publish("wii","1:1:0:0:#")
 
    if (buttons & cwiid.BTN_B):
      print 'Button B pressed'
 
    if (buttons & cwiid.BTN_HOME):
      global last
      global selected_menu
      last = last + 1
      if last == len(menu):
         last = 0
      selected_menu = menu[last]
      MQ.publish("speak", str(menu[last]))
      time.sleep(1)

    if (buttons & cwiid.BTN_MINUS):
      MQ.publish("speak", selected_menu+" stop")
      time.sleep(1)
 
    if (buttons & cwiid.BTN_PLUS):
      MQ.publish("speak", selected_menu+" start")
      time.sleep(1)


    time.sleep(button_delay)
    subPWM(1,1)

  print "DISCONECTED"
  time.sleep(3)
  getWii()

MQ = mosquitto.Mosquitto("wii")
MQ.on_connect = on_connect
MQ.on_publish = on_publish
MQ.connect("localhost", port, 0)  
while True:
  MQ.loop()
  main()
