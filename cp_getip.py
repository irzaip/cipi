import commons
import time

try:
  txt = commons.get_rnd_txt()
  ip = commons.get_outside_ip()
  commons.tweet(txt+"-"+ip)

except:
  pass

