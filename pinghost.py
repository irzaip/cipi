import os
import json


allhost = json.load(open("host.txt"))


#and then check the response...
for n in allhost['hosts']:
  hostname = n['ip']
  print "Checking " + str(hostname)
  response = os.system("ping -c 1 " + hostname)
  if response == 0:
    print hostname, 'is up!'
    n['lastseen'] = 1
    print ""
  else:
    print hostname, 'is down!'
    n['lastseen'] = int(n['lastseen']) + 1
    if (int(n['lastseen']) > 3):
       print "FAKTAP"
       print ""


json.dump(allhost,open('host.txt','w'))

