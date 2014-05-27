"""
This script demonstrates how to create a bare-bones, fully functional
chatbot using PyAIML.
"""
from espeak import espeak
import mosquitto
import aiml
import sys
import ConfigParser
import time

config = ConfigParser.ConfigParser()
config.read("config.ini")

broker = config.get("MQTT","broker")
port = int(config.get("MQTT","port"))


client_name="aiml"
mqttc = mosquitto.Mosquitto(client_name)

mqttc.connect(broker, port, 60)



def on_connect(obj,rc):
    if rc == 0:
        print "AIML to Broker Connected"
    else:
        raise Exception

def on_message(obj, msg):
    espeak.synth(kern.respond(str(msg.payload)))

# Create a Kernel object.
kern = aiml.Kernel()

# When loading an AIML set, you have two options: load the original
# AIML files, or load a precompiled "brain" that was created from a
# previous run. If no brain file is available, we force a reload of
# the AIML files.
brainLoaded = False
forceReload = False
while not brainLoaded:
	if forceReload or (len(sys.argv) >= 2 and sys.argv[1] == "reload"):
		# Use the Kernel's bootstrap() method to initialize the Kernel. The
		# optional learnFiles argument is a file (or list of files) to load.
		# The optional commands argument is a command (or list of commands)
		# to run after the files are loaded.
		kern.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
		brainLoaded = True
		# Now that we've loaded the brain, save it to speed things up for
		# next time.
		kern.saveBrain("standard.brn")
	else:
		# Attempt to load the brain file.  If it fails, fall back on the Reload
		# method.
		try:
			# The optional branFile argument specifies a brain file to load.
			kern.bootstrap(brainFile = "standard.brn")
			brainLoaded = True
		except:
			forceReload = True

# Enter the main input/output loop.
mqttc.on_connect=on_connect
mqttc.on_message=on_message
mqttc.subscribe("aiml",1)

espeak.set_voice('id')
espeak.set_parameter(3,10)

espeak.synth("okay, saya siap")

while mqttc.loop() == 0:
        time.sleep(.1)
        pass

print "End of AIML"

