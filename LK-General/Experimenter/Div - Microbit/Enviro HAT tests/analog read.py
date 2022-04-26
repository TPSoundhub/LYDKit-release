from microbit import *

while True:
        val = pin1.read_analog()
        print(val)
        sleep(100)