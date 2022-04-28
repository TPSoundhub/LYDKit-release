# LKS1Mb-AnaPitch-Modtager.py
# Forventer at modtage en tal værdi fra radio som kan bruges til at lave en lyd.
# Vil IKKE virke hvis der modtages andet end et tal. Så vil program gå ned med en fejl.
# Sikrer selv at værdi er mellem 50 og 3907 før den kalder music.pitch() med det tal der modtages
# De 3907 kommer fra V1 af Micro:Bitten, da den ikke kan håndtere pitch højere end 3907.
# Forklar hvad nof_nones bliver brugt til. Hvad er effekten?
from microbit import *
import music
import radio

display.show("APM")                  # Udskriver på MB display for at identificere funktion
                                     # som 'Analog Pitch Modtager' når MB kører med batteri (svært at se ellers).
radio.on()
radio.config(channel=22)             # Brug kanalnummer der er udleveret/aftalt (0-83)

nof_nones = 0

while True:
    f_str = radio.receive()
    print(f_str,"  ",type(f_str))    # Test udskrift af hvad der modtages i shell incl typen af det
    if f_str:                        # Det samme som "f_str != None:"  men IKKE som "f_str == True:"
        f_num = int(f_str)           # Men altså 'noget er modtaget' fra funktionen. Tekst-streng konverteres til tal.
        nof_nones = 0
        if (f_num>50) and (f_num<3907):
            music.pitch(f_num)
        else:
            music.stop()
    else: nof_nones = nof_nones+1
    if nof_nones > 20 : music.stop()
    sleep(50)