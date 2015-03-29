import paho.mqtt.client as mosquitto
import time
from pyfirmata import Arduino, util
import commons

DIRL = 0
DIRR = 0
PWML = 0
PWMR = 0
HIGH = 1
LOW = 0


board = Arduino('/dev/ttyUSB0')

it = util.Iterator(board)
it.start()

#right wheel
MIN1_1 = board.get_pin('d:2:o')
MIN1_2 = board.get_pin('d:3:o')
MEN1_1 = board.get_pin('d:4:o')
MEN1_2 = board.get_pin('d:5:o')
MPWM1 = board.get_pin('d:6:p')

#left wheel
MIN2_1 = board.get_pin('d:7:o')
MIN2_2 = board.get_pin('d:8:o')
MEN2_1 = board.get_pin('d:9:o')
MEN2_2 = board.get_pin('d:10:o')
MPWM2 = board.get_pin('d:11:p')

def forward():
    MIN1_1.write(HIGH)
    MIN1_2.write(LOW)
    MEN1_1.write(HIGH)
    MEN1_2.write(HIGH)
    MIN2_1.write(HIGH)
    MIN2_2.write(LOW)
    MEN2_1.write(HIGH)
    MEN2_2.write(HIGH)
    
def backward():
    MIN1_1.write(LOW)
    MIN1_2.write(HIGH)
    MEN1_1.write(HIGH)
    MEN1_2.write(HIGH)
    MIN2_1.write(LOW)
    MIN2_2.write(HIGH)
    MEN2_1.write(HIGH)
    MEN2_2.write(HIGH)


def turn_left():
    MIN1_1.write(HIGH)
    MIN1_2.write(LOW)
    MEN1_1.write(HIGH)
    MEN1_2.write(HIGH)
    MIN2_1.write(LOW)
    MIN2_2.write(HIGH)
    MEN2_1.write(HIGH)
    MEN2_2.write(HIGH)


def turn_right():
    MIN1_1.write(LOW)
    MIN1_2.write(HIGH)
    MEN1_1.write(HIGH)
    MEN1_2.write(HIGH)
    MIN2_1.write(HIGH)
    MIN2_2.write(LOW)
    MEN2_1.write(HIGH)
    MEN2_2.write(HIGH)

    
def processcommand(msg):
    try:
        msg = msg.split(":")
        if msg[4] == "#":
            DIRL = int(msg[0])
            DIRR = int(msg[1])
            PWML = commons.map(msg[2],0,100,0,1)
            PWMR = commons.map(msg[3],0,100,0,1)
            #print "Speed" + str(PWML) + " - " +  str(PWMR)
            
            if DIRL == 1 and DIRR == 1:
                forward()
            if DIRL == 0 and DIRR == 1:
                turn_left()
            if DIRL == 1 and DIRR == 0:
                turn_right()
            if DIRL == 0 and DIRR == 0:
                backward()
            MPWM1.write(PWMR)
            MPWM2.write(PWML)
            time.sleep(0.02)

    except:
        print "Command Ignored"
    
def on_connect(mosq, obj, rc):
    print "Connected"
    mosq.subscribe("motor", 0)
    #print("rc: "+str(rc))

def on_message(mosq, obj, msg):
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    processcommand(msg.payload)

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
mqttc = mosquitto.Mosquitto("motor")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
mqttc.connect("192.168.0.100", 1883, 60)
mqttc.publish("speak","motor ready")

while True:
    mqttc.loop()

    #pelan-pelan makin pelan             
    if PWML > 0:
        PWML = PWML - 2
        if PWML < 0:
            PWML = 0
    if PWMR > 0:
        PWMR = PWMR - 2
        if PWMR < 0:
            PWMR = 0
    #send the PWM

board.exit()
