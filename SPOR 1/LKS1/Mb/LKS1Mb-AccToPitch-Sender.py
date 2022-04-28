# LKS1Mb-AccToPitch-Sender.py
# Accelerometer data fra x-akse sendt på radio som tekst streng

from microbit import *
import radio

display.show("ATP-S")             # Udskriver på MB display for at identificere funktion
                                  # som 'Acc -> Pitch sender" når MB kører med batteri (svært at se ellers).
radio.on()
radio.config(channel=22)          # hvis kanal angives skal det være samme kanal i både sender og modtager
                                  # Hvis kanal ikke angives er default kanal nr 7 i begge
while True:
    acc_x,acc_y,acc_z = accelerometer.get_values()   
    f_num = acc_x+1500            # adderer tilstrækkelig stor værdi til at de fleste er indenfor OK pitch område.
    print(f_num,"  ",type(f_num)) # test udskrift for at vise hvad vi har fået fra funktionskaldet til accelerometeret
    radio.send(str(f_num))        # radio.send() funktionen sender tekst strenge så tal konverteres til tekst-streng.
    sleep(50)                     # Bør bruge samme værdi i både sender og modtager. Samme takt.