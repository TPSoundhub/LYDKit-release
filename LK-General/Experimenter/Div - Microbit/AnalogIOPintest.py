# AnalogIOPintest.py
# Forsøg med at bruge max antal pins som analog input - (med display_off som beskrevet i dokumentation)
# KFU-SHD 17-Feb-2022
# Som med test af digital input viser det sig at man ikke kan bruge dem som er reserveret til display
# på MB V2! De opererer som een. (input på en pin smitter af på de andre)
#
from microbit import *

print("Udlæs analog værdi")    # Ready

display.off()   # for at kunne køre med pin 3,4 og 10 som analog input

while True:
    
    v1 = pin0.read_analog()
    v2 = pin1.read_analog()
    v3 = pin2.read_analog()
    v4 = pin3.read_analog()
    v5 = pin4.read_analog()
    v6 = pin10.read_analog()

    print("Analog værdi på pin 0,1,2,3,4 og 10:  ",v1,v2,v3,v4,v5,v6)

    sleep(30)