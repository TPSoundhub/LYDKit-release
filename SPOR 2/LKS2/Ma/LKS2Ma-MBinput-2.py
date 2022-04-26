# LKS2Ma-MBinput-2.py - Kode der modtager tegn på den serielle kanal fra MicroBit
#
# Version 1.1 - 22-Dec-2021, Rettet kommentar.
# Version 1.0 - 22-Okt-2021, Justeret til Spor 2, Modul a, introduktion. Sammen med MB type 0 i MicroBit (Alle til demo)
#             - Husk radio kanal sat forskelligt for alle i lokalet!!
# Version 0.3 - 20-jul 2021, Justeret brugt 1x og 3x intro.
# Version 0.2 - 14 jan 2021, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland


# Import af de biblioteker og funktioner vi har brug for. Samlet i LKlib!

from LKlib import *
#
# Initialisering af:
#  - seriel port til kommunikation med tilsluttet Micro:Bit.
#  - Lyd mixer, der kan håndtere op til 8 lyde samtidigt. 
ser=init_serial()
init_mixer()


# Loop forever

while True:
    modtaget_tuple = get_microbit_input(ser,all_info=True)
    if modtaget_tuple:
        i,t,k,v = modtaget_tuple
        print(modtaget_tuple," tuple modtaget på seriel port (MB ident, MB type, MB key, MB value)")
        if k == "A":
            play_sound("cheer-crowd.wav")
        if k == "B":
            play_sound("buu-trombone.wav")
        if k == TABT_FORBINDELSE: ser=init_serial()
        
