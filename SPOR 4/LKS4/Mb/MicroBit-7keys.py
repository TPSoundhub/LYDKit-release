# MicroBit-7keys.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt i MicroBit,
#                     og kombineres med et andet program på PC/PI/MAC. Microbitten skal forblive koblet til
#                     PC/MAC/PI med USB.
#                   - Husk at det skal være med lille m i main.py ellers duer det ikke!
#                   - Bruges i Spor 4 som første trin efter at have brugt PC keyboard. Bruges sammen med
#                     LKS4-simple-7key-piano-MicroBit.py på PC/MAC/PI
#
# Version 1.0 - 09 Nov 2021 - Udgave til frigivelse/spredning i efteråret 2021.
#                             Tilpasset protokol med type og ident. Ellers lige ud fra Spor 1 Modul b
#                             Til brug i Spor 4 som et første trin i at lave keyboard.
#
from microbit import *

last_key = "0"
key      = "0"
display.show(key)

def read_key():
    p0 = pin0.is_touched()
    p1 = pin1.is_touched()
    p2 = pin2.is_touched()
    
    if p0 and p1 and p2:               key="7"
    elif not p0 and p1 and p2:         key="6" 
    elif p0 and not p1 and p2:         key="5" 
    elif not p0 and not p1 and p2:     key="4"
    elif p0 and p1 and not p2:         key="3"
    elif not p0 and p1 and not p2:     key="2" 
    elif p0 and not p1 and not p2:     key="1"
    else:                              key="0"
 
    return key


while True:

    key = read_key()
    sleep(50)
    key_control = read_key()      # Læser den 2 gange og skal være ens for at få effekt.
                                  # For at der ikke skal komme for mange 'falske aftastninger'
    
    if key == key_control:
        if last_key != key:
            print("00"+key)       # Dummy ident og type ("00") for at virke med LKlib/protokollen i LYD-Kit.
            display.show(key)
            last_key=key
    
    sleep(50)