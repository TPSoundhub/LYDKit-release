# LKS1Mb-Sender-2.py
# Besked fra input sendt kontinuerligt (løbende) med 
# på default kanal med default sendestyrke med 500msec interval
from microbit import *
import radio

radio.on()
besked = input("Indtast det som skal sendes: ")   # Venter på input fra shell
    
while True:
    radio.send(besked)
    sleep(500)          # Er vigtig nu da program IKKE venter på input hver gang det kommer rundt
                        # Bemærk forskel i modtager ift. sender-1.