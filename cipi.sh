#!/bin/sh

#python getip.py

#read -p "Press any key" var1

python cp_motor.py&

sudo /etc/init.d/bluetooth stop
sudo hciconfig hci0 up

python cp_wii.py&

python cp_speak.py&
python cp_emo.py&

#python cp_teleop.py

sleep 6

python cp_getip.py

#read -p "Press any key to continue" var1



#killall python
