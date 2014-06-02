#!/usr/bin/python

import mosquitto

a = 0


def on_connect(mosq, obj, rc):
    mosq.subscribe("teleop", 0)
    mosq.subscribe("wii",0)
    #print("rc: "+str(rc))

def on_message(mosq, obj, msg):
   global a
   if msg.topic == "teleop":
     try:
       mqttc.publish("motor",msg.payload)
       a = 0
     except:
       pass
     return
   if msg.topic == "wii":
     try:
       mqttc.publish("motor",msg.payload)
       a = 0
     except:
       pass


def on_publish(mosq, obj, mid):
    #print("mid: "+str(mid))
    pass

def on_subscribe(mosq, obj, mid, granted_qos):
    #print("Subscribed: "+str(mid)+" "+str(granted_qos))
    pass

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

while True:
  a = a + 1
  mqttc.loop()
  if a > 10:
     mqttc.publish("motor","1:1:0:0:#")
     a = 0

  

