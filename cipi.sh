#!/bin/sh

#python getip.py

read -p "Press any key" var1

#python serusb.py &
python sser.py &
#python cpaiml.py &
python cpnav.py &

sleep 6

read -p "Press any key to contine" var1

python wi2.py
#python teleop.py


killall python
