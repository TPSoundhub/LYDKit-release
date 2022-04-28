# OSC drumbeat.py
#
# Hurtigt eksemple på hvordan man kan kontrollere mønster, tempo of samples i et basis beat mønster, samt
# de samples der bruges som instrumenter i et program der bliver kørt af/i Sonic PI - filen "Drumbeat6.rb", via
# OSC kommandoer.  KFU - SHD - 13-jan-22
#
# Se i koden for hvilke taster der gør hvad i dette simple eksempel....
#
# Til inspiration for at man kan arbejde videre. Lav Python program der mere dynamisk kan opsætte mønster for de 4
#   - open
#   - closed
#   - snare
#   - kick
#
# samt skifte tempo i flere trin..
#
# og udskifte samples for de 4 - både ud fra de som er med i Sonic PI, men også med egne optagelser....
#
# enten via keyboard eller vildere via sensor inputs fra MicroBit's .... .. .. . . . .
#
# Til inspiration/læring omkring forskellige rytmer så henvises til:
# https://learningmusic.ableton.com/make-beats/make-beats.html
#

from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import pygame



# Local host - via IP på lokal maskine - Altid på IP nummer 127.0.0.1
sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

# External host - på et lokalt netværk hvor router tillader kommunikation via porten
# SKAL finde det rigtige IP nummer og sætte ind!! Findes i Sonic PI på den computer
# der kører Sonic PI.
#sender = udp_client.SimpleUDPClient('10.0.100.136', 4560)


# Vindue med fokus for at kunne få tastaturinput til programmet. (ESC stopper og lukker vinduet)
screen = pygame.display.set_mode((150, 150))

# Så længe run er True tages tastatur input og konverteres til node/hastighed
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
            if (event.type == pygame.KEYDOWN):
                if key == "up":
                    sender.send_message('/trigger/drumbeat_control',["tempo",120])
                if key == "down":
                    sender.send_message('/trigger/drumbeat_control',["tempo",60])
                if key == "left":
                    sender.send_message('/trigger/drumbeat_control',["on_off",0])
                if key == "right":
                    sender.send_message('/trigger/drumbeat_control',["on_off",1])
                #  ------------
                if key == "q":
                    sender.send_message('/trigger/drumbeat_patern_open',  [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1])
                if key == "a":
                    sender.send_message('/trigger/drumbeat_patern_open',  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
                # -------------
                if key == "w":
                    sender.send_message('/trigger/drumbeat_patern_closed',[0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
                if key == "s":
                    sender.send_message('/trigger/drumbeat_patern_closed',[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0])
                # -------------
                if key == "e":
                    sender.send_message('/trigger/drumbeat_patern_snare', [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0])
                if key == "d":
                    sender.send_message('/trigger/drumbeat_patern_snare', [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])
                # -------------
                if key == "r":
                    sender.send_message('/trigger/drumbeat_patern_kick',  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
                if key == "f":
                    sender.send_message('/trigger/drumbeat_patern_kick',  [1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0])
                # -------------
                if key == "y":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["open", "drum_cymbal_pedal"])
                if key == "h":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["open", "drum_cymbal_open"])
                # -------------
                if key == "u":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["closed", "drum_cymbal_soft"])
                if key == "j":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["closed", "drum_cymbal_closed"])
                # -------------
                if key == "i":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["snare", "drum_cowbell"])
                if key == "k":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["snare", "sn_zome"])
                # -------------
                if key == "o":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["kick", "drum_bass_hard"])
                if key == "l":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["kick", "drum_heavy_kick"])
                # -------------

# Ved program exit, ryddes op og vindue fjernes:
pygame.quit()
