# DigitalIOPintest.py
# Forsøg med at bruge max antal pins som digitalt input - (med display_off som beskrevet i dokumentation)
# KFU-SHD 17-Feb-2022  - rettet fejl i kommentarer.
# KFU-SHD 19-Jan-2022
# 
# Med Micro:Bit V1 (den uden indbygget mic og højtaler) så virker digital input på pin
# 0,1,2,3,4,6,7,8,9,10,12,13,14,15 og 16  (pin 5 og 11 er knap A og B!)
# - Dvs her kan man lave 15 forskellige digitale inputs (knapper hvis man går all in!!)
# - Dvs med den kunne man lave en "MBType-8.py" der returnerer key værdier 0,1,2,3,4,5,6,7,8,9,A,B,C,D,E og dermed kunne lave
#   opstillinger med flere knapper/færre MB's ift når man bruger MBType-0. Ex kan een MB så håndtere Quiz ex. og en fuld oktav i spor 4.
# - Det vil være en fin åben bog opgave at stille.
# - Testet med Firmware 1.0.1 2018-12-13 MB v1.5
#
# https://microbit-micropython.readthedocs.io/en/v2-docs/pin.html?highlight=read_digital
# https://microbit-micropython.readthedocs.io/en/v2-docs/display.html?highlight=display_off
#
# MEN !!!
#
# Med Micro:Bit V2 er det kun pin 0,1,2,8,9,12,13,14,15 og 16 man kan regne med.
# 3,4,6,7,10 opererer som een (alle på en gang) også selvom man har slået displayet fra!
# Testet med Firmware 2.0.0 (2021-06-30) MB v2.0
#
# Så man kan stadig lave en MBType-8 men ikke med 15 forskellige inputs - kun med 10!
#
# OG !!!
#
# Kikker man på HW spec.
# https://tech.microbit.org/hardware/edgeconnector/
# står pin 0,1,2,8,13,14,15 til at være GPIO som default, og en række står med GPIO i parantes,
# hvilket betyder brug med forsigtighed.
# DET KAN VI SAMMEN MED OVENSTÅENDE OVERSÆTTE TIL: BRUG KUN DE 8 !
# og det vil virke på både version 1 og 2 - og vi risikerer ikke noget :-)
#
# KONKLUSION - EN ÅBENBOG OPGAVE MED AT LAVE EN TYPE 8 BØR KUN INDEBÆRE DE 8 PINS 0,1,2,8,13,14,15,16
# men der kan bruges flere afhængig af version og konfiguration iøvrigt!!
#
# Tilgengæld et rigtig godt eksempel på hvad der kan ske i detaljen ifm nye versioner og hvad bagudkompatibilitet betyder i
# denne fagre nye verden. Og at man skal teste i bund! og kende sine sensorer!!
#
#

from microbit import *

def dp(pin,x):
    if (pin.read_digital() == 1):
        x=x+'1'
    else: x=x+'0'
    return x

display.off()

while True:
    x =''
    x = dp(pin0,x)
    x = dp(pin1,x)
    x = dp(pin2,x)
    x = dp(pin3,x)
    x = dp(pin4,x)
    x = dp(pin5,x)
    x = dp(pin6,x)
    x = dp(pin7,x)
    x = dp(pin8,x)
    x = dp(pin9,x)
    x = dp(pin10,x)
    x = dp(pin11,x)
    x = dp(pin12,x)
    x = dp(pin13,x)
    x = dp(pin14,x)
    x = dp(pin15,x)
    x = dp(pin16,x)
    
    print('01234A67890B23456')
    print(x)
    sleep(200)