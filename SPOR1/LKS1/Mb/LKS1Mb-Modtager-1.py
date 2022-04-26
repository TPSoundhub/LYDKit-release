# LKS1Mb-Modtager-1.py
# Checker om der er kommet besked på default kanal hvert halve sekund. (500 msek).
# Der udskrives None i shell, hvis der ikke er modtaget noget.
# Er der modtaget noget udskrives det i shell.
from microbit import *
import radio

radio.on()

while True:
    besked = radio.receive()
    print(besked)
    sleep(500)