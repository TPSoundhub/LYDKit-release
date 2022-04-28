# LKS4-simple-7key-KBOSC.py
#
# Program der genererer toner for frekvenserne der svarer til de 7 noder A4 til G5, svarende til
# LKS3-simple-7key-piano, men her genereres toner ikke lokalt i program, men der sendes OSC triggere
# ud på lokal netværket (evt lokalt på computeren) til et andet program. Tonerne aktiveres med tastetryk
# på computerens tastatur.
#
# Forudsætter at man har installeret biblioteket: "pythonosc" via Tools>Manage packages i Thonny.
#
# Version 1.2 - 12-Jan-2022 - Tilføjet tydeligere eksempel vedr. sample så man kan komme igang.
#                           - Fjernet is_playing da den ingen effekt har (kan kun starte lyde i sonic pi/ikke stoppe)
# Version 1.1 - 24-Nov-2021 - Rettet fejl med 2 gange definition af key tabel.
# Version 1.0 - 17-Nov-2021 - Rettet kommentarer og navn.
# Version 0.1 - 06-Apr-2021 - Knud Funch, Soundhub danmark - LYDKit til undervisningbrug - Region MidtJylland
#
# Her FORUDSÆTTES at der er et andet program som lytter.
# I dette eksempel forudsættes at man har startet en session i Sonic PI med følgende indhold:
#
#  live_loop :foo1 do
#    use_real_time
#    s, n, a, p = sync "/osc*/trigger/synth"
#    use_synth s
#    play hz_to_midi(n), amp: a, pan: p
#  end
#  live_loop :foo2 do
#    use_real_time
#    s, n, a, p, ps = sync "/osc*/trigger/sample"
#    sample s, rate: n, amp: a, pan: p, pitch: ps, window_size: 0.5
#  end
#
# Desuden skal man i input/output delen af sonic PI have tilladt OSC og set at port nummer stemmer overens
# med det som står i koden i Python koden nedenfor.
#
# Sonic PI er et gratis program hvor man med tekstbaseret programmering kan lave musik. Det er gratis, det fungerer på
# både PC,MAC og PI. Det kan hentes på: https://sonic-pi.net/
#
# Det er forudinstalleret på det diskimage som findes til PI's for Lyd-Kit.
#
# HUSK - Skal have fokus i det lille sorte vindue for at tasttryk kommer igennem!.
#  

from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import pygame

#
# Udvid med flere noder og keys hvis I synes - DER SKAL være samme antal elementer i de 2 tabeller!
#

frequency = [  # node and index/position in table/array
440.00,           # A4 - pos 0
493.88,           # B4 - pos 1
523.25,           # C5 - pos 2
587.33,           # D5 - pos 3
659.25,           # E5 - pos 4
698.46,           # F5 - pos 5
783.99,           # G5 - pos 6
]

#
# Udvid med flere nrates og keys hvis I synes - DER SKAL være samme antal elementer i de 2 tabeller!
#


rate = [
    0.2,
    0.4,
    0.6,
    1.0,
    1.2,
    1.4,
    1.6
]

keys=['a', 's', 'd', 'f', 'g', 'h', 'j']

# Local host - via IP på lokal maskine - Altid på IP nummer 127.0.0.1
sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

# External host - på et lokalt netværk hvor router tillader kommunikation via porten
# SKAL finde det rigtige IP nummer og sætte ind!! Findes i Sonic PI på den computer
# der kører Sonic PI.
#sender = udp_client.SimpleUDPClient('10.0.100.136', 4560)


# Vindue med fokus for at kunne få tastaturinput til programmet. (ESC stopper og lukker vinduet)
screen = pygame.display.set_mode((150, 150))

# Map keys og lyde sammen i et dictionary for hurtig opslag - brugt sammen med synth playback (en node)
key_sound = dict(zip(keys, frequency))

# Map keys og rate sammen i et dictionary for hurtig opslag - brugt sammen med sample playback (hasstighedsskift)
key_rate = dict(zip(keys,rate))

# Så længe run er True tages tastatur input og konverteres til node/hastigheda
# Start ved keydown. (sender OSC trigger)

run = True
while run:
    event = pygame.event.wait()

    if event.type == pygame.QUIT: run = False  # X'ed i window
    else:
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)
            print(key)
            if event.key == pygame.K_ESCAPE: run = False
            if (event.type == pygame.KEYDOWN) and (key in key_sound.keys()):
                # prøv med andre synth værdier end "piano" - Find dem i Sonic PI dokumentationen!!
                # udvid program så man med tastetryk kan skifte mellem forskellige synths.
                # find de forskellige muligheder for taster i dokumentationen for Pygame.
                # kan I få noget ud af at bruge \trigger\sample til noget ??
                # lav evt andre triggere i Sonic PI og kommuniker med dem via udvidelser i dette
                # python program!!
                
               sender.send_message('/trigger/synth',["piano",key_sound[key], 1, 0])
#               sender.send_message('/trigger/sample',["C:/Lyde/Creaking-wood.wav",key_rate[key],1,0,0])
#               sender.send_message('/trigger/sample',["perc_bell",key_rate[key],1,0,0])


# Ved program exit, ryddes op og vindue fjernes:
pygame.quit()

# Opgaver:
# - Udvid med flere taster toner/rates
# - Udvid med flere parametre som ændres vha taster/input
# - Lav koden om så der bruges sensor inputs fra Micro:Bits istedet for keyboard input
#  (sammenlign 7 key keyboard og microbit ...)
          