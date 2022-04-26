# LKS1Mb-3Key-Sender.py
# Sender 3 værdier for hhv pin 0, 1 og 2 på radio.
# PIN 0,1,2 is_touched -> sender "1", "2", "4".
# Når der ikke er nogen PINs der er aktive sendes et "0"
# PIN kan være aktive samtidigt så der er flere kombinationsmuligheder.
# Opgave: Udvid til at sende 7 forskellige keys "1" - "7" ud fra de mulige kombinationer.

from microbit import *
import radio

display.show("3KS")               # Udskriver en tekst på display for at identificere MB når der kommer strøm på 
sleep(1000)                       # Venter 1 sekund inden vi går videre for at besked kan ses færdig.
                                  # Bliver overskrevet, da key løbende udskrives i display.
radio.on()
radio.config(channel=33)          # Brug kanalnummer der er udleveret/aftalt (0-83)

while True:
    p0 = pin0.is_touched()
    p1 = pin1.is_touched()
    p2 = pin2.is_touched()
    if p0:
        key = "1"
    elif p1:
        key = "2"
    elif p2:
        key = "4"
    else:
        key = "0"

    radio.send(key)               # radio.send() funktionen sender key der er et tegn
    display.show(key)             # viser key på MBs display
    sleep(50)                     # Bør bruge samme værdi i både sender og modtager. Samme takt.