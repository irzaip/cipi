import time
from pyfirmata import Arduino, util


board = Arduino('COM3')

it = util.Iterator(board)
it.start()

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

