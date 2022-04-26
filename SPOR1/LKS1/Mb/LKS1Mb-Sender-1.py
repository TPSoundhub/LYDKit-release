# LKS1Mb-Sender-1.py
# Besked fra input sendt een gang for hver runde.
# på default kanal med default sendestyrke
from microbit import *
import radio

radio.on()

while True:
    besked = input("Indtast det som skal sendes: ")  # Venter på input fra shell
    radio.send(besked)
    sleep(500)          # Betyder ikke noget da program venter på input hver gang det kommer rundt