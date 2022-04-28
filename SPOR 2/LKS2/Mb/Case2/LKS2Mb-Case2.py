# -*- coding: utf-8 -*-
# Linien ovenfor er inkluderet for at sikre korrekt håndtering af special tegn (DK) ved start af program fra boot
# (headless)
#
# LKS2Mb-Case2.py - Kode eksempel med 3 sæt lyde der kan matches med taster fra Micro:Bits til PC/MAC/PI
#                 - Kan bruges til at lave et nudging setup i en butik hvor man så skal finde passende lyde.
#                 - Micro:Bit kode som hører sammen med dette eksempel findes i LKS2 under MicroBit-Koder-1 som MBType-0.py
#
# Version 0.2 - 02 mar 2021, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
#                            Dette er et første hurtigt skud som kunne bruges til en NUDGE case.
# Version 1.0 - 20-Okt-2021, Rette i navne og kommentarer til frigivelse.
#
# Illustration af brug af Type 0 i MicroBit og 2 lister med lyd. Kan ex. bruges til nudging case. 
# - Når trigger fra pin 0 så een lyd i venstre højtaler     (måske placeret ved grøntsagerne)
# - Når trigger fra pin 1 så een anden lyd i højre højtaler (måske placeret ved vin afdelingen)
# Kan også spille en baggrunds lyd - Den startes ved tryk på knap "B" på een af MB'erne. Og slukkes igen ved tryk på "A"
#
# Lydene skal udskiftes - kunne ex. være nogle oplysninger om et emne, eller en lyd der kan assosieres med en bestemt vare.
# Kommer der input "1" vælges lyde fra den ene liste og "2" så vælges fra den anden liste.
#
# Laver man 3 Microbits med Type 0 kode, og kobler den ene på usb og de andre for sig selv med batteri
# vil pin 1 på alle i dette tilfælde medføre at funktion 'trigges'.
# Men bruger man ex. kun den ene med en 'knap' på pin 1 og den anden på pin 2 kan man uden at ændre i
# koden have 2 adkilte 'triggere' placeret forskellige steder ex. i en butik.
#
# Man kunne måske også bruge en anden type trigger, men så skal man ændre lidt i koden.

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
# sti = "/home/pi/LKS2/Mb/Case2/"


# Liste med korte lyde til venstre kanal (fugle lyde i ex. Udskift dem med andre med samme navn, som passer til nudge case)
# Lydene som følger med i ex til en start er en Stork, en Ugle og en Spætte. DE har INGENTING med nudging at gøre!!
#
lydeV = [
sti+"v-a.wav",        # index 0
sti+"v-b.wav",        # index 1
sti+"v-c.wav"         # index 2
]

# Liste med korte lyde til højre kanal (div lyde i ex. Udskift med andre med samme navn, som passer til nudge case)
# Lydene som følger med i ex til en start er en boremaskine, et kasseapparat, en bil og en Smed. DE har INGENTING med nudging at gøre!!
#
lydeH = [
sti+"h-a.wav",        # index 0 
sti+"h-b.wav",  
sti+"h-c.wav",       
sti+"h-d.wav"         # index 3
]

#
# Liste af fil navne på lydfiler der er lidt længere i varighed til afspilning i baggrunden i begge kanaler
# Lydene som følger med i ex til en start er lyden af en by udenfor, og lyden af en cafe indenfor. DE har INGENTING med nudging at gøre!!
#
lydeB = [
sti+"b-a.wav",        # index 0
sti+"b-b.wav"         # index 1
]

#
# Initialisering af:
#  - seriel port til kommunikation med tilsluttet Micro:Bit.
#  - Lyd mixer, der kan håndtere op til 8 lyde samtidigt. 
init_mixer()
ser=init_serial()

# -----------  afspil lyde random ud fra aktivering af pin 0 eller pin 1 på MB nr x  -----------

ch_left  = None
ch_right = None

# Loop forever

while True:
    k = get_microbit_input(ser)
    if k:
        print(k," modtaget på den serielle")
        if k == "1":
            stop_sound(ch_left)  # Hvis der allerede er een igang.
            ch_left = play_sound(lydeV[random.randint(0,len(lydeV)-1)],vol_l=0.05,vol_r=0)
        elif k == "2":
            stop_sound(ch_right) # Hvis der allerede er een igang.
            ch_right = play_sound(lydeH[random.randint(0,len(lydeH)-1)],vol_l=0,vol_r=0.05)
        elif k == "B":         
            play_background(lydeB[random.randint(0,len(lydeB)-1)])
        elif k == "A":         
            stop_background()

        if k == TABT_FORBINDELSE : ser=init_serial()      # genetabler forbindelse til MB, hvis forbindelse tabt
