# LKS2Ma-Afspil-lyde.py
#
# Version 0.3 - 13 Jan-2021, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
# Version 1.0 - 22-Okt-2021, Justeret til Spor 2, Modul a, introduktion.

#
# Import af de biblioteker og funktioner vi har brug for i denne sammenhæng
#
from LKlib import *

# en liste af fil navne på lyd filer med korte lydklip med fugle lyde
#
fuglelyde = [
"ugle.wav",        # index 0
"solsort.wav",     # index 1
"hane.wav",        # index 2
"skovskade.wav"    # index 3
]

# -----------  afspil nogle lyde  -----------
init_mixer()

play_background("bagg-trafik.wav")   # start lydfil fra listen med baggrundslyde og brug den med index 0
time.sleep(5)                        # vent 5 sekunder - lyd fortsætter i baggrund
play_background("bagg-flod.wav")     # bemærk den overtager fra den første baggrundslyd og bliver ved ..
time.sleep(5)
play_sound("start-seq.wav")          # bemærk den spiller 'oveni'
time.sleep(5)
# så et eksempel hvor vi starter afspilning af alle lydfiler i listen fuglelyde som spiller oveni hinanden og oveni baggrundslyden
for x in range(0,len(fuglelyde)):
    play_sound(fuglelyde[x])
    print(x)
    time.sleep(1)
    
time.sleep(20)                       # vent til alle fuglelyde er færdig spillet

# og lad os tage en tilfældig fuglelyd til at slutte med
play_sound(fuglelyde[random.randint(0,len(fuglelyde)-1)])
