# LKS2Ma-MBinput-1.py - Kode der modtager tegn på den serielle kanal fra MicroBit
#
# Version 1.1 - 22-Dec-2021, Rettet kommentar.
# Version 1.0 - 22-Okt-2021, Justeret til Spor 2, Modul a, introduktion. Sammen med MB type 0 i MicroBit
#             - Husk radio kanal sat forskelligt for alle i lokalet!!
# Version 0.3 - 20-jul 2021, Justeret brugt 1x og 3x intro.
# Version 0.2 - 14 jan 2021, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland

#
# Import af de biblioteker og funktioner vi har brug for. Samlet i LKlib.

from LKlib import *

#
# Initialisering af:
#  - seriel port til kommunikation med tilsluttet Micro:Bit.
#  - Lyd mixer, der kan håndtere op til 8 lyde samtidigt. 
ser=init_serial()
init_mixer()


# Loop forever

while True:
    key = get_microbit_input(ser)
    if key:
        print(key," tegn modtaget på den serielle")
        if key == "A":
            play_sound("cheer-crowd.wav")
        if key == "B":
            play_sound("buu-trombone.wav")
    else:
        print("timeout - så man kan lave andet i programmet, end at vente på input fra den serielle hvis man vil")
        
# Opgave:
#  - Prøv at lave en kortslutning fra GND til PIN 0,1 og 2 - Hvad modtages på den serielle?
#  - Udvid evt. program så der kommer en lyd når en af pinnene kortsluttes!