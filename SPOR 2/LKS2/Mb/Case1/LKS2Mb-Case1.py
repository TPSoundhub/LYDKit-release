# -*- coding: utf-8 -*-
# Linien ovenfor er inkluderet for at sikre korrekt håndtering af special tegn (DK) ved start af program fra boot
# (headless)
#
# LKS2Mb-Case1.py - Kode eksempel med 1 sæt lyde der kan trigges af forskellige events fra forskellige Micro:Bits
#                 - Micro:Bit kode som hører sammen med dette eksempel findes i LKS2 under MicroBit-Koder-1 (alle typerne)
#
# Version 1.1 - 22-Dec-2021  Tilføjet kommentar i hoved løkke.
# Version 1.1 - 25-Okt-2021  Rettet fejl i kommentar - Beskrivelse.
# Version 1.0 - 20-Okt-2021, Rettet i navne og kommentarer til frigivelse.
# Version 0.2 - 23 Aug 2021, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
#                            Dette er et første hurtigt skud som kunne bruges til en case med lyd i det offentlige rum med
#                            valgfri trigger. Ex. Vippe med MB-Type1 kode. Kan bruges til at demonstrere de forskellige
#                            MB type koder.
#
# Import af de biblioteker og funktioner vi har brug for i denne sammenhæng
#
from LKlib import *

#
# Så længe lyd filerne ligger i samme direktorie som programmet, og det startes fra editor (Thonny)
# skal der IKKE angives en sti.
sti = ""
# Hvis I vil lave en pæn direktoriestuktur med lydene i et andet direktorie, eller I vil starte program
# fra kommando promt - for eksempelvis at lave et headles setup med raspberry PI skal I angive sti.
# Der skal man være opmærksom på special tegn. 

# Skal man have programmet til at køre fra Boot på headless setup med PI skal sti defines som nedenfor:
# sti = "/home/pi/LKS2/Mb/Case1/"

#
# En liste af fil navne på lyd filer med lyd klip som ex. Skal Ændres så det passer til case.
# Kan bare gemme nye lyde i de samme navne så fungerer det.
# Og kan bare gøre liste kortere, hvis man ikke vil have så mange.
#
lyde = [
sti+"a.wav",        # index 0  - Gråd
sti+"b.wav",        # index 1  - Grin
sti+"c.wav",        # index 2  - Cafe
sti+"d.wav",        # index 3  - Banegård
sti+"e.wav",        # index 4  - Rådhusklokken
sti+"f.wav",        # index 5  - Skrivemaskine 
sti+"g.wav",        # index 6  - Boremaskine
sti+"h.wav",        # index 7  - Forlystelsespark
sti+"i.wav",        # index 8  - Helikopter
sti+"j.wav",        # index 8  - Kasseapparat
sti+"k.wav",        # index 9  - Bil
sti+"l.wav",        # index 10 - Plæneklipper
sti+"m.wav",        # index 11 - Floddamper
sti+"n.wav",        # index 12 - Orkester
sti+"o.wav",        # index 13 - Smed
sti+"p.wav",        # index 14 - Syresump
sti+"q.wav",        # index 15 - Kanalsøgning
sti+"r.wav"         # index 16 - Vand (bølger)
]

#
# Initialisering af:
#  - seriel port til kommunikation med tilsluttet Micro:Bit.
#  - Lyd mixer, der kan håndtere op til 8 lyde samtidigt. (startet med play_sound(). Kun een med play_background()) 
ser=init_serial()
init_mixer()

while True:
    k = get_microbit_input(ser)
    if k:
        print(k," modtaget på den serielle")
        # Afspil en tilfældig lyd fra listen af lyde når der kommer en af triggerne nedenfor.
        # Dvs tilfældig lyd fra en trigger fra en MB med enten type 0,1,2,3,4 eller 6
        # Hvad skal der til for at få trigger fra type 5 til også at virke?
        if (k in ["1","2","4","B","M","L","S","H","V"]):
            play_background(lyde[random.randint(0,len(lyde)-1)],forever=False)
            
        if k == "A": stop_background()
        
        # genetabler forbindelse til MB, hvis forbindelse tabes    
        if k == TABT_FORBINDELSE : ser=init_serial()                