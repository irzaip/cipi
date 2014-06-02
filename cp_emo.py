import time
import mosquitto

port = 1883

emo = ["anger","happy","friendly","bored","tired","crowded","lonely","frustrated","brave","curious","sad","disgusted","surprised","hungry","romantic","scared"]

anger = 0
happy = 10
friendly = 10
bored = 0
tired = 0
crowded = 0
lonely = 0
frustrated = 0
brave = 0
curious = 0
sad = 0
disgusted = 0
surprised = 0
hungry = 0
romantic = 0
scared = 0


def on_connect(mosq, msg, rc):
   for w in emo:
     mosq.subscribe(str(w),0)
     #if rc == 0:
        #print w + " connected"

def on_message(mosq, obj, msg):
   #print "from " + msg.topic + ":" + msg.payload
   pass     
      

def on_publish(mosq,obj,mid):
    pass

def on_subscribe(mosq,obj,mid,granted_qos):
    #print("Subscribed:"+str(mid)+" " + str(granted_qos))
    pass

mqtt = mosquitto.Mosquitto()
mqtt.on_subscribe = on_subscribe
mqtt.on_publish = on_publish
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.connect("127.0.0.1",port,60)

while True:
   mqtt.loop()
   time.sleep(0.1)

