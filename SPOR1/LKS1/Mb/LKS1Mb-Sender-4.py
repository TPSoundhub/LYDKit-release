# LKS1Mb-Sender-4.py
# Besked sendt på forskellige kanaler til forskellige elevgrupper
# Elevergrupper skal gerne kun modtage besked med det
# kanal nummer de har fået tildelt.

from microbit import *
import radio

radio.on()
# Dictionary med elevgruppe som nøgle (til opslag)
# og kanalnummer som det man får retur
elev_gr_til_k_nr = { # elevgruppe:  Kanalnummer:
                                1:  10,
                                2:  20,
                                3:  30,
                                4:  40,
                                5:  50,
                                6:  60,
                                7:  70,
                                8:  80
    }

# Default max 29 tegn - 3 til nummer. Altså 26 i første del af besked.
#         123456789012345678901234567890
besked = "Hej jer med kanalnummer: "

while True:
    for elev_gr in elev_gr_til_k_nr:     # For alle nøgler i distionary
        k_nr = elev_gr_til_k_nr[elev_gr] # slås kanal nummeret op og bruges
        radio.config(channel=k_nr)       # til at sætte radiokanal op
        radio.send(besked+str(k_nr))     # til at sende besked på
        print(besked+str(k_nr))          # skriver hvad der sendes i shell
        sleep(500)                       # holder en pause.
        