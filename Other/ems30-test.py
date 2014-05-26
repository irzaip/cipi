#  Robot from TOP
#       
#            front   
#          +========+
#          |        |
#  left  []|        |[] right
#  wheel   |        |   wheel
#          +--------+
#             rear
#

import time
from pyfirmata import Arduino, util

board = Arduino('COM4')

it = util.Iterator(board)
it.start()

HIGH = 1
LOW = 0

LED = board.get_pin('d:13:o')

MIN1_1 = board.get_pin('d:2:o')
MIN1_2 = board.get_pin('d:3:o')
MEN1_1 = board.get_pin('d:4:o')
MEN1_2 = board.get_pin('d:5:o')
MPWM1 = board.get_pin('d:6:p')

MIN2_1 = board.get_pin('d:7:o')
MIN2_2 = board.get_pin('d:8:o')
MEN2_1 = board.get_pin('d:9:o')
MEN2_2 = board.get_pin('d:10:o')
MPWM2 = board.get_pin('d:11:p')

#forward
def forward():
  MIN1_1.write(HIGH)
  MIN1_2.write(LOW)
  MEN1_1.write(HIGH)
  MEN1_2.write(HIGH)
  
  MIN2_1.write(HIGH)
  MIN2_2.write(LOW)
  MEN2_1.write(HIGH)
  MEN2_2.write(HIGH)
  
  
if __name__ == '__main__':
  forward()
  LED.write(HIGH)
  MPWM1.write(0.9)
  MPWM2.write(0.9)
  time.sleep(2)
  LED.write(LOW)
  MPWM1.write(0)
  MPWM2.write(0)
  time.sleep(2)
  board.exit()

  
  
  
  
  
