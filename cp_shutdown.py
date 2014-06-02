from espeak import espeak
import time
import subprocess


subprocess.call(["aplay","/home/pi/cipi/sounds/shutdowninprocess.wav"])
time.sleep(2)
subprocess.call(["sudo","shutdown","-r","now"])


