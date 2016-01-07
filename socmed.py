#!/usr/bin/python
 
import smtplib, string, subprocess, time

import sys
from twython import Twython
import urllib2
import random

from myconfig import *
 
###############################################

cp_api = Twython(cp_CONSUMER_KEY,cp_CONSUMER_SECRET,cp_ACCESS_KEY,cp_ACCESS_SECRET)
mst_api = Twython(mst_CONSUMER_KEY,mst_CONSUMER_SECRET,mst_ACCESS_KEY,mst_ACCESS_SECRET)


def cipitweet(status):
  try:
    cp_api.update_status(status=status)
  except:
    print "Error updating twitter status"

def msttweet(status):
  try:
    mst_api.update_status(status=status)
  except:
    print "Error updating twitter status"
 
def sendgmail(recipient,subjecttxt,mailtxt):
    
  SUBJECT = subjecttxt + ' Report at: %s' % time.asctime()
  TO = recipient
  FROM = SMTP_USERNAME
  BODY = string.join((
    'From: %s' % FROM,
    'To: %s' % TO,
    'Subject: %s' % SUBJECT,
    '',
    mailtxt
    ), '\r\n')
  try:
    server = smtplib.SMTP(SMTP_SERVER)
    # server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_USERNAME,SMTP_PASSWORD)
    server.sendmail(FROM, [TO], BODY)
    server.quit()
 
    print "Done emailing..."
  except:
    print "Error sending email"

