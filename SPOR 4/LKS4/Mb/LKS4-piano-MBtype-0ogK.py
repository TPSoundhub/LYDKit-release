# -*- coding: utf-8 -*-
# Linien ovenfor er inkluderet for at sikre korrekt håndtering af special tegn (DK) ved start af program fra boot
# (headless).
#
# LKS4-piano-MBtype-0ogK.py
#
# Program der genererer toner for frekvenserne der svarer til de 12 noder C4 til G5, og mapper dem til 4
# unikke Microbits type 0 eller K (identifiers 0,1,2,3), hvilket system/setup mæssigt svarer helt til Quiz (Case 3)
# eksemplet fra Spor 2.
#
# En naturlig progression fra "LKS3-simple-7key-piano-MicroBit.py" med forbedringer ud fra oplevelsen med dem.
#
# Version 1.1 - 15-Nov-2021 - Tilføjet test på at man ikke starter samme node uden den først er
#                             afsluttet. Efter brug i forløb på SSG der viste at man kan misse en 'tast sluppet'.
# Version 1.0 - 10-Nov-2021 - Rettet kommentarer og navn.
# Version 0.5 - 21-Okt-2021 - Rettet til med LKlib funktioner
# Version 0.4 - 26 Nov 2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningbrug - Region MidtJylland
#
from LKlib import *

#
# Konstant til test udskrift.
# Hvis I vil se lidt mere om hvad der sker så sæt TEST_PRINT_ON = True
#
TEST_PRINT_ON = False

#
# Udvid med flere noder og ident+keys hvis I synes - DER SKAL være samme antal elementer i de 2 tabeller!
# lav skalaen om ... etc ..
# Bemærk at når man ikke har et helt tal, så betyder det at man ikke har et helt antal omgange
# i enhedscirklen, hvilket vil sige når man laver et sample på 1 sek så starter det i nul, men
# ender IKKE i nul, hvilket vil give ticks/click lyde når lyden loopes..

frequency = [     # node, position, ident og key i table/array - C-major scale
261.63,           # C4 - pos  0     - '01'
293.66,           # D4 - pos  1     - '02'
329.63,           # E4 - pos  2     - '04'
349.23,           # F4 - pos  3     - '11'
392.00,           # G4 - pos  4     - '12'     
440.00,           # A4 - pos  5     - '14'
493.88,           # B4 - pos  6     - '21'
523.25,           # C5 - pos  7     - '22'
587.33,           # D5 - pos  8     - '24'
659.25,           # E5 - pos  9     - '31'
698.46,           # F5 - pos 10     - '32'
783.99,           # G5 - pos 11     - '34'
]

ident_and_key = [
'01',             # pos  0  - relateret til pos  0 i frequency 
'02',             # pos  1  - relateret til pos  1 i frequency
'04',             # pos  2  - relateret til pos  2 i frequency
'11',             # pos  3  - relateret til pos  3 i frequency
'12',             # pos  4  - relateret til pos  4 i frequency
'14',             # pos  5  - relateret til pos  5 i frequency
'21',             # pos  6  - relateret til pos  6 i frequency
'22',             # pos  7  - relateret til pos  7 i frequency
'24',             # pos  8  - relateret til pos  8 i frequency
'31',             # pos  9  - relateret til pos  9 i frequency
'32',             # pos 10  - relateret til pos 10 i frequency
'34',             # pos 11  - relateret til pos 11 i frequency
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
#    x = generate_amp_modulated_fmsine(freq,fmf=int(freq/3),fmi=10,amf=8,ami=0.2)
#    x = env(generate_amp_modulated_fmsine(freq,fmf=int(freq/2),fmi=7,amf=8,ami=0.4))
    return x

# ---------------------------------------------------------------------------------------------------
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
# Lav lydene som mappes til tasterne fra MicroBit
#
range_of_tones = range(0, len(frequency))
sound_table = [make_tones(frequency[i]) for i in range_of_tones]
generated_sounds = map(generate_stereo_sound,sound_table)

# Mapper taster (keys) og de genererede lyde sammen i et dictionary for let og hurtigt opslag
key_sound = dict(zip(ident_and_key, generated_sounds))

# is_playing dictionary for at holde samling på hvilke der er aktive og spiller en lyd - initialiseres alle til False (not playing)
is_playing = {k: False for k in ident_and_key}

def end_all_notes():
    for k in ident_and_key:
        if is_playing[k]:
            key_sound[k].stop()
            is_playing[k]=False
            
def end_note(idx):
    if is_playing[idx]:
        key_sound[idx].stop()
        is_playing[idx]=False    

def play_note(idx):
    if idx in ident_and_key:
        if not is_playing[idx]:      # Hvis der ikke er kommet et stop så genstarter vi ikke noden!!
            key_sound[idx].set_volume(1.0)
            key_sound[idx].play(-1)  # Hvis man kun vil have lyden afspillet een gang så fjerner man -1
            is_playing[idx]=True

#
# Hoved program løkke, som læser input fra Microbit og afspiller node der passer til input 
#
last_playing = '0'

while True:
   
    modtaget_tuple = get_microbit_input(ser,all_info=True)
    if modtaget_tuple:
        i,t,k,v = modtaget_tuple
        if TEST_PRINT_ON: print(modtaget_tuple," tuple modtaget på seriel port (MB ident, MB type, MB key, MB value)")

        if k == "A":
            end_all_notes()
            # Her kan man jo ex. tilføje en funktion der skifter mellem forskellige lyde
            # Man kunne jo lave flere udgaver af make_tones() eller udvide den med en parameter til det..

        if k == "B":
            end_all_notes()
            # Her kan man jo ex. tilføje en funktion der skifter mellem forskellige skalaer

        if k in ["0","1","2","4"]:  # Der er kommet et key input som program kan håndtere
            
            index = i+k
            if k == "0":
                if   t == "0": end_all_notes()    # Ved type 0 kan vi ikke afgøre hvilken tast der er sluppet.
                elif t == "K":                    # men det  kan vi med type K 
                    key = chr(v)
                    ident_and_key_to_stop = i+key
                    if TEST_PRINT_ON: print("ident and key: ",ident_and_key_to_stop)

                    if ident_and_key_to_stop in ident_and_key:
                        if TEST_PRINT_ON: print(ident_and_key_to_stop,":",ident_and_key_to_stop)
                        end_note(ident_and_key_to_stop)
                        if TEST_PRINT_ON: print(is_playing)                        
            else:
                play_note(index)
                if TEST_PRINT_ON: print(is_playing)

        if k == TABT_FORBINDELSE :
            end_all_notes()                  # uden denne risikerer man at der er en node som bliver 'hængende'
            ser=init_serial()                # genetabler forbindelse til MB, hvis forbindelse tabt
