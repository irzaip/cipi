###########################################
#                                         #
# cp_hand.py                              #
# author: irza pulungan                   #
#                                         #
# this py will forward incoming MQTT      #
# message to Serial USB port arduino      #
# loaded with custom sketch               #
#                                         #
###########################################

import serial
import paho.mqtt.client as mqtt

ser = serial.Serial("/dev/ttyACM0",9600)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if (msg.topic == "servo"):
      print str(msg.payload)
      ser.write(str(msg.payload)+"\n\r")
      ser.flushInput()
      ser.flushOutput()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("192.168.0.100", 1883, 60)
client.subscribe("servo",0)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
client.loop_forever()

