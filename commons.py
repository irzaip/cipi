
import os
import re
import subprocess
import random
import socket
import urllib2
import time

def map(x, in_min, in_max, out_min, out_max):
  myresult = (float(x) - float(in_min)) * (float(out_max) - float(out_min)) / (float(in_max) - float(in_min)) + float(out_min)
  return round(myresult,2)

def get_pid(proc_name):
    ps = subprocess.Popen("ps ax -o pid= -o args= ", shell=True, stdout=subprocess.PIPE)
    ps_pid = ps.pid
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()

    for line in output.split("\n"):
        res = re.findall("(\d+) (.*)", line)
        if res:
            pid = int(res[0][0])
            if proc_name in res[0][1] and pid != os.getpid() and pid != ps_pid:
                return pid
    return False

def killpid(pid):
   subprocess.call(["kill",pid])

def tweet(twit):
   time.sleep(10)
   subprocess.call(["mosquitto_pub","-t","tweet","-h","127.0.0.1","-m",twit])

def get_rnd_txt():
   g = file("/home/pi/cipi/addition/random.txt","rb")
   cp = g.readlines()
   return random.choice(cp)

  
def get_local_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("gmail.com",80))
  myip = (s.getsockname()[0])
  #print "My IP Adress: " + myip
  s.close()
  return str(myip)

def get_outside_ip():
  try:  
    try:
      myip = urllib2.urlopen("http://myip.dnsdynamic.org/").read()
    except:
      myip = urllib2.urlopen("http://myexternalip.com/raw").read()
    return myip
  except:
    return 


