import time
from pyfirmata import ArduinoMega, util


board = ArduinoMega('COM4')

it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()

PING_R_FRONT = 