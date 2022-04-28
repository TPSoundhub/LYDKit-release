# -*- coding: utf-8 -*-
# Linien ovenfor er inkluderet for at sikre korrekt håndtering af special tegn (DK) ved start af program fra boot
# (headless).
#
# LKS4-simple-7key-piano-MicroBit.py
#
# Program der genererer toner for frekvenserne der svarer til de 7 noder A4 til G5, svarende til
# LKS3-simple-7key-piano, men her mappes ikke til taster på PC/MAC/PI men istedet til input fra MicroBit.
# Her FORUDSÆTTES at det er "MicroBit-7key.py", der kører lokalt på en Microbit tilkoblet PC/MAC/PI via USB.
#
# Kan bruges til at sammenholde oplevelsen med LKS3-simple-7key-piano og have dialog om:
#  - Hvordan man kan lave et mekannisk tastatur med 7 taster med kun 3 digitale inputs.
#  - Fordele og ulemper ved det.
#  - Forskel i oplevelse, og forbedrings muligheder.
#
# Version 1.0 - 10-Nov-2021 - Rettet kommentarer og navn.
# Version 0.5 - 21-Okt-2021 - Rettet til med LKlib funktioner
# Version 0.4 - 26 Nov 2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningbrug - Region MidtJylland
#
from LKlib import *

#
# Udvid med flere noder og keys hvis I synes - DER SKAL være samme antal elementer i de 2 tabeller!
#

# Bemærk at når man ikke har et helt tal, så betyder det at man ikke har et helt antal omgange
# i enhedscirklen, hvilket vil sige når man laver et sample på 1 sek så starter det i nul, men
# ender IKKE i nul, hvilket vil give ticks/click lyde når lyden loopes..

frequency = [     # node and index/position in table/array
440.00,           # A4 - pos 0
494.00,           # B4 - pos 1
523.00,           # C5 - pos 2
587.00,           # D5 - pos 3
659.00,           # E5 - pos 4
698.00,           # F5 - pos 5
784.00,           # G5 - pos 6
]

keys = [
'1',             # pos 0  - relateret til pos 0 i frequency 
'2',             # pos 1  - relateret til pos 1 i frequency
'3',             # pos 2  - relateret til pos 2 i frequency
'4',             # pos 3  - relateret til pos 3 i frequency
'5',             # pos 4  - relateret til pos 4 i frequency
'6',             # pos 5  - relateret til pos 5 i frequency
'7',             # pos 6  - relateret til pos 6 i frequency
]

# Funktion der laver tonerne.
# Modificer funktionen for at lave andre toner ved at bruge og kombinere signaler lavet med funktionerne i LKlib.
# Ex ved at addere overtoner. Prøv dem som er udkommenteret.
def make_tones(freq):
    x = generate_sine(freq)
#    x = env(generate_sine(freq))
#    x = exp_decay(generate_sine(freq))
#    x = generate_triangle(freq)
#    x = env(generate_triangle(freq))
#    x = exp_decay(generate_freq_modulated_sine(freq,fmf=int(freq/2),fmi=5),-3)
#    x = exp_decay(generate_amp_modulated_fmsine(freq,fmf=int(freq/2),fmi=5,amf=8,ami=0.4),-3)
#    x = env(generate_amp_modulated_fmsine(freq,fmf=int(freq/2),fmi=7,amf=8,ami=0.4))
    return x

# ---------------------------------------------------------------------------------------
# Koden nedenfor læser input fra MicroBit og konverterer til afspilning af lyd!
# Det behøver man ikke at ændre på!!!
#  - Dog kan det tænkes at ændre mellem .play(-1) og .play() for at spille lyd kontinuert eller kun een gang pr tastetryk
#

#
# Initialisering af:
#  - seriel port til kommunikation med tilsluttet Micro:Bit.
#  - Lyd mixer, der kan håndtere op til 8 lyde samtidigt. 
ser=init_serial()
init_mixer()

#
# Lav lydene som mappes til tasterne fra MicroBitten.
#
range_of_tones = range(0, len(frequency))
sound_table = [make_tones(frequency[i]) for i in range_of_tones]
generated_sounds = map(generate_stereo_sound,sound_table)

# Mapper taster (keys) og de genererede lyde sammen i et dictionary for let og hurtigt opslag
key_sound = dict(zip(keys, generated_sounds))


def play_note(key,is_playing):
    if key != is_playing:
        if is_playing in keys: key_sound[is_playing].stop()  # key different from "0" then stop the last sound
        is_playing = "0"
    if key in keys:
        key_sound[key].set_volume(1.0)
        key_sound[key].play(-1)                              # play sound related to key if key different from "0"
        is_playing = key
     
    return is_playing

last_playing = '0'

#
# Hoved program løkke, som læser input fra Microbit og afspiller node der passer til input 
#
last_playing = '0'

while True:
   
    mb_key = get_microbit_input(ser)
    if mb_key:
        print(mb_key)
        last_playing = play_note(mb_key,last_playing)
           