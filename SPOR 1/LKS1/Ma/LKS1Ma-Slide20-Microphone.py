# Udlæsning af lyd niveau fra indbygget mikrofon.
from microbit import *

while True:
    s = microphone.sound_level()
    if s>0: print(s)                                   
    sleep(10)