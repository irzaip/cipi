import time
import commons

a = commons.getmillis()

while True:
  b = commons.getmillis()
  if b-a > 5000:
    print "5000"
    a = commons.getmillis()


