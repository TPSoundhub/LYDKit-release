# LKS1Mb-Modtager-2.py
# Checker om der er kommet besked på angivet kanal hvert halve sekund. (500 msek).
# Der udskrives None i shell, hvis der ikke er modtaget noget.
# Er der modtaget noget udskrives det i shell.
from microbit import *
import radio

radio.on()
radio.config(channel=10)   # Kanal der kommunikeres på - Kan være mellem 0 og 83 (incl)

while True:
    besked = radio.receive()
    print(besked)
    sleep(500)