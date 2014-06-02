import mosquitto

a = 0
port = 1883
command = "1:1:0:0:#"

mqtt = mosquitto.Mosquitto("teleop")
mqtt.connect("localhost",port, 0)


print "TELEOP Command with W,A,S,D,X"
print "-----------------------------"
print " Q to quit"
print ""

while True:
   mqtt.loop()
   input = raw_input("command:")
   if input == "q":
      exit()
   if input == "w":
      command = "1:1:20:20:#"
   if input == "x":
      command = "0:0:20:20:#"
   if input == "a":
      command = "0:1:20:20:#"
   if input == "d":
      command = "1:0:20:20:#"
   if input == "s":
      command = "1:1:0:0:#"

   mqtt.publish("teleop",command)
   a = a + 1