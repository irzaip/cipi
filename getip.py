import socket
import ConfigParser

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
myip = (s.getsockname()[0])
print "My IP Adress: " + myip
s.close()

config = ConfigParser.SafeConfigParser()

config.read("config.ini")
config.set("MQTT","broker", myip)

with open('config.ini', 'wb') as configfile:
    config.write(configfile)
