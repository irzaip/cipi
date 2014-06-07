import math
from datetime import *
import subprocess, shlex
import commons
from pytz import timezone
import calendar
from dateutil.relativedelta import *

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
      ev_dt=datetime.strptime(dt[0]+" "+dt[1],"%Y-%m-%d %H:%M")
      evnt = dt[6]
      if ev_dt.date() == today.date():
        print ev_dt.date(),evnt


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
               commons.speak(data)
               
 
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
            commons.speak(data)
               

#RETRIEVE CALENDAR FROM GOOGLE CAL AND WRITE TO FILE
def retrieve_agenda():
   try:
     mycmd = "gcalget.sh"
     subprocess.call(["sh",mycmd])
   except:
     espeak.synth("calendar error")


retrieve_agenda()
mycal = get_cal()
#today_event()
event_reminder()
event_ongoing()






