#!/usr/bin/env python
#
# Get Current IP on raspberry pi.
# and post to twitter.
#
# requirement: pip install twython


import sys
from twython import Twython
import urllib2
import random

from socmed import *

try:
  f = open('oneliner.txt','r')
  one = f.readlines()
  oneliner = one[random.randint(1,len(one))]
  print oneliner

except:
   print "Error getting joke -- put default"
   oneliner = "oh oh - my ip:"


try:
  response = urllib2.urlopen('http://getip.dyndns.org')
  html = response.read()
  #parse the response
  ext_ip = html.split(" ")[6]
  ext_ip = ext_ip.split("<")[0]

  f = open('curr_ip.txt','r')
  last_ip = f.read()

  print "Last ip:" + last_ip
  print "Ip Now:" + ext_ip
  
  if ext_ip == last_ip:
	  print "Exactly same - go to sleep again"
	  quit()
  else:
	  print "Different - writing new"
	  f = open('curr_ip.txt','w')
	  f.write(ext_ip)
	  f.close()
	  
except:
  print "error fetching ip -- try another 10 minutes"
  quit()

status = oneliner + " -" + ext_ip

try:
  cipitweet(status)
except:
  print "Error tweeting ip address"

print status

#try:
 # api.update_status(status=status)
#except:
  #print "Error updating twitter status"

