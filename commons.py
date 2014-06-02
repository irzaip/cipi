import os
import re
import subprocess


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
   subprocess.call(["mosquitto_pub","-t","tweet","-h","127.0.0.1","-m",twit])

  
  
