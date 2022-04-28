# LKS1Mb-Sender-3.py
# Besked sendt kontinuerligt på default kanal med default sendestyrke med 500msec interval.
# MEN med et løbenummer mellem 1 og 9, så man kan se om alle beskeder kommer igennem.
# Forsøg med forskellige ventetider og se resultatet på modtager siden.
from microbit import *
import radio

radio.on()
besked_nr = 1
besked = "Hej med jer "          # Her er besked bare skrevet direkte til variablen. Venter ikke på input

while True:
    radio.send(besked+str(besked_nr))   
    print(besked+str(besked_nr))  # Når man sammensætter skal begge være strenge - derfor str() på integer
    besked_nr = besked_nr+1
    if besked_nr>9:
        besked_nr = 1
    sleep(500)                    # Betyder noget for hvor mange beskeder der bliver sendt over tid.
                                  # Kør med 1000 hhv 100 msec her og se hvad der sker på modtager siden.