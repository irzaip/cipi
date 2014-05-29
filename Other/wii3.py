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
 
button_delay = 0.1
 

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
      wii.rumble = 1
      time.sleep(0.1)
      wii.rumble = 0
      try:
        wii.close()
      except:
        pass

 
    # Check if other buttons are pressed by
    # doing a bitwise AND of the buttons number
    # and the predefined constant for that button.
    if (buttons & cwiid.BTN_LEFT):
      print 'Left pressed'
      time.sleep(button_delay)
 
    if(buttons & cwiid.BTN_RIGHT):
      print 'Right pressed'
      time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_UP):
      print 'Up pressed'
      time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_DOWN):
      print 'Down pressed'
      time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_1):
      print 'Button 1 pressed'
      time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_2):
      print 'Button 2 pressed'
      time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_A):
      print 'Button A pressed'
      time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_B):
      print 'Button B pressed'
      time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_HOME):
      print 'Home Button pressed'
      time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_MINUS):
      print 'Minus Button pressed'
      time.sleep(button_delay)
 
    if (buttons & cwiid.BTN_PLUS):
      print 'Plus Button pressed'
      time.sleep(button_delay)
 
    time.sleep(0.01)

  print "DISCONECTED"
  time.sleep(3)
  getWii()

if __name__ == "__main__":
  while True:
    main()

