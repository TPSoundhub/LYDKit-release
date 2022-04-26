# LKS1Mb-DigPitch-Modtager.py
# Forventer at modtage en key for et input der er aktivt og nul når ingen er aktive.
# Reagerer på key's med værdi 1,2,3,4,5,6,7 og spiller en tone/frekvens for hver af dem.
# Modtages 0 stoppes tone.
#
from microbit import *
import music
import radio

display.show("DPM")                  # Udskriver på MB display for at identificere funktion
                                     # som 'Digital Pitch Modtager' når MB kører med batteri (svært at se ellers).
radio.on()
radio.config(channel=33)             # Brug kanalnummer der er udleveret/aftalt (0-83)

nof_nones = 0

# Dictionary med key (1-7) som nøgle (til opslag) - Key som tegn derfor i ""
# og tone som frekvens som det man får retur      - Frekvens som tal derfor ikke i ""
key_til_pitch = { # key:  Frekvens:
                    "1":  440,         # A4 - Kammertonen
                    "2":  493,         # B4
                    "3":  523,         # C5
                    "4":  587,         # D5
                    "5":  659,         # E5
                    "6":  698,         # F5
                    "7":  783          # G5
    }

while True:
    key_str = radio.receive()
    if key_str:                      # noget modtaget
        nof_nones = 0
        print(key_str)               # som testudskrift i shell når koblet til PC/MAC
        if key_str == "0" : music.stop()
        else: music.pitch(key_til_pitch[key_str])
    else: nof_nones = nof_nones+1
    if nof_nones > 20 :              # sender er slukket eller udenfor rækkevidde. Stop evt. lyd!
        music.stop()              
        nof_nones = 0
    sleep(50)