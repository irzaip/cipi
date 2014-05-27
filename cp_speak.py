#!/usr/bin/python

from espeak import espeak
import mosquitto
from datetime import datetime
import subprocess

language = "kr"

def on_connect(mosq, obj, rc):
    mosq.subscribe("speak", 0)
    print("rc: "+str(rc))

def on_message(mosq, obj, msg):
    global language
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    if msg.payload == "en2":
      language = "en2"
      return
    if msg.payload == "en":
      language = "en"
      return
    if msg.payload == "ko":
      language = "ko"
      return
    if msg.payload == "id":
      language = "id"
      return
    if language == "en":
      espeak.synth(msg.payload)
    if language == "ko":
      subprocess.call(["/home/pi/cipi/speech_ko.sh",msg.payload])
    if language == "id":
      subprocess.call(["/home/pi/cipi/speech_id.sh",msg.payload])
    if language == "en2":
      subprocess.call(["/home/pi/cipi/speech_en.sh",msg.payload])

def on_publish(mosq, obj, mid):
    print("mid: "+str(mid))

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

mqttc.loop_forever()

