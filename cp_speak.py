#!/usr/bin/python
import commons
from espeak import espeak
import mosquitto
import subprocess
from os import listdir
import random
from os.path import join
from twython import Twython
import ConfigParser
#import time
import moc
import math
from datetime import *
from pytz import timezone
import calendar
from dateutil.relativedelta import *


config = ConfigParser.ConfigParser()
config.read("config.ini")

CONSUMER_KEY = config.get("TWYTHON","CONSUMER_KEY")
CONSUMER_SECRET = config.get("TWYTHON","CONSUMER_SECRET")
ACCESS_KEY = config.get("TWYTHON","ACCESS_KEY")
ACCESS_SECRET = config.get("TWYTHON","ACCESS_SECRET")

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

rndspeak = ["seenee","hai","hallo","bip bip","robot","yuhu","ea","oi","we","oh","aah"]



folder = "/home/pi/cipi/sounds/"
files = listdir(folder)

plfolder = "/home/pi/cipi/playlist/"
playlist = listdir(plfolder)
language = "en"

musiclist = []

atime = commons.getmillis()
stoptime = commons.getmillis()
stoptimeb = commons.getmillis()
# start the moc server
try:
  moc.start_server()
except:
  pass


def dt(str):
   r = datetime.strptime(str,"%Y-%m-%d")
   return r

def get_cal():
   f = file("agenda.txt","rb")
   ap = f.readlines()
   data = []
   for dt in ap:
      data.append(dt.split("	"))
   return data

#SPEAK EVENT FOR TODAY
def today_event():
   today = datetime.today()
   now = datetime.now()
   for dt in mycal:
      print dt
      ev_dt=datetime.strptime(dt[0]+" "+dt[1],"%Y-%m-%d %H:%M")
      evnt = dt[6]
      if ev_dt.date() == today.date():
        espeak.synth("dont forget to " + evnt +"\n" )

#COMPARE HALF HOUR EVENT
def event_reminder():
   today = datetime.today()
   now = datetime.now()
   for dt in mycal:
      ev_dt=datetime.strptime(dt[0]+" "+dt[1],"%Y-%m-%d %H:%M")
      evnt = dt[6]
      if ev_dt.date() == today.date():
         if ev_dt > now:
            intime = int(math.floor((ev_dt - now).seconds / 60))
            if intime < 300:
               data = evnt + ", event in " + str(intime) + " minutes"
               espeak.synth(data)


def event_ongoing():
   today = datetime.today()
   now = datetime.now()
   for dt in mycal:
      ev_fr=datetime.strptime(dt[0]+" "+dt[1],"%Y-%m-%d %H:%M")
      ev_to=datetime.strptime(dt[2]+" "+dt[3],"%Y-%m-%d %H:%M")
      evnt = dt[6]
      if ev_fr < now:
         if ev_to > now:
            data = "Do "+evnt+" now"
            espeak.synth(data)

#RETRIEVE CALENDAR FROM GOOGLE CAL AND WRITE TO FILE
def retrieve_agenda():
   try:
     mycmd = "gcalget.sh"
     subprocess.call(["sh",mycmd])
   except:
     espeak.synth("calendar error")


def parsemusic(dat):
    f = file(dat,"r")
    a = f.readlines()
    try:
      a.remove('\n')
    except:
      pass
    return a 


  
def on_connect(mosq, obj, rc):
    mosq.subscribe("speak", 0)
    mosq.subscribe("sound", 0)
    mosq.subscribe("tweet", 0)
    mosq.subscribe("teleop", 0)
    mosq.subscribe("wii",0)
    print("rc: "+str(rc))

def on_message(mosq, obj, msg):
   global folder
   global files
   global language
   global api
   global stoptime

   #routing dari teleop/wii ke topic MOTOR
   if msg.topic == "teleop":
     try:
       mqttc.publish("motor",msg.payload)
       a = 0
     except:
       pass
     return
   if msg.topic == "wii":
     try:
       mqttc.publish("motor",msg.payload)
       a = 0
     except:
       pass

   
   #process topic tweet
   if msg.topic == "tweet":
     try:
       api.update_status(status=str(msg.payload))
       espeak.synth("Tweeted")
     except:
       espeak.synth("Tweet failed")
     return
 
   #process topic speak
   if msg.topic == "speak":
     #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
     if msg.payload == "en2":
         language = "en2"
         return
     elif msg.payload == "en":
         language = "en"
         return
     elif msg.payload == "ko":
         language = "ko"
         return
     elif msg.payload == "id":
         language = "id"
         return
     elif msg.payload == "rnd":
         espeak.synth(random.choice(rndspeak))
         return


     #incoming from wii
     if msg.payload == "music start":
         espeak.synth("play music")
         musiclist = parsemusic(join(plfolder,random.choice(playlist)))
         moc.quickplay(musiclist)
         return
     elif msg.payload == "music stop":
         moc.stop()
         espeak.synth("music stop")
         return
     elif msg.payload == "volume up":
         moc.increase_volume(10)
         return
     elif msg.payload == "volume down":
         moc.decrease_volume(10)
         return
     elif msg.payload == "next music":
         moc.next()
         return
     elif msg.payload == "previous music":
         moc.previous()
         return
     elif msg.payload == "toggle shuffle":
         moc.toggle_shuffle()
         return
     elif msg.payload == "enable shuffle":
         moc.enable_shuffle()
         return
     elif msg.payload == "disable shuffle":
         moc.disable_shuffle()
         return
     elif msg.payload == "main++":
         espeak.synth("run main")
         commons.run_main()
         return
     elif msg.payload == "main--":
         espeak.synth("kill main")
         commons.kill_main()
         return
     elif msg.payload == "display++":
         espeak.synth("display plus plus")
         return
     elif msg.payload == "display--":
         espeak.synth("display minus minus")
         return
     elif msg.payload == "light++":
         espeak.synth("light plus plus")
         return
     elif msg.payload == "light--":
         espeak.synth("light minus minus")
         return
     elif msg.payload == "print++":
         espeak.synth("print plus plus")
         return
     elif msg.payload == "print--":
         espeak.synth("print minus minus") 
         return
     
     if language == "en":
         espeak.synth(msg.payload)
     elif language == "ko":
         subprocess.call(["/home/pi/cipi/speech_ko.sh",msg.payload])
     elif language == "id":
         subprocess.call(["/home/pi/cipi/speech_id.sh",msg.payload])
     elif language == "en2":
         subprocess.call(["/home/pi/cipi/speech_en.sh",msg.payload])


   #process topic sound
   if msg.topic == "sound":
       if msg.payload == "rnd":
          subprocess.call(["aplay",join(folder,random.choice(files))])
       else:
          subprocess.call(["aplay",msg.payload])

def on_publish(mosq, obj, mid):
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mosquitto.Mosquitto("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mosquitto.Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
mqttc.connect("127.0.0.1", 1883, 60)

#mqttc.subscribe("string", 0)
#mqttc.subscribe(("tuple", 1))
#mqttc.subscribe([("list0", 0), ("list1", 1)])

#Speak agenda
retrieve_agenda()
mycal = get_cal()
today_event()

while True:
  mqttc.loop()


  #loop reminder for every 5 minutes
  btime = commons.getmillis()
  if btime-atime > 300000:
    atime = commons.getmillis()
    event_reminder()
    event_ongoing()
  
  #loop timer untuk stop motor tiap 10 detik / safety
  stoptimeb = commons.getmillis()
  if stoptimeb-stoptime > 5000:
    stoptime = commons.getmillis()
    mqttc.publish("motor","1:1:0:0:#")
    
