# LKS3-simple-7key-piano.py
#
# Program der genererer toner for frekvenserne der svarer til de 7 noder A4 til G5.
# Noderne (tonerne) mappes til tastatur tasterne A,S,D,F,G,H,J så det kan bruges som et meget basalt 'piano',
# og vise princip.
#
# Version 1.1 - 25 Okt 2021 - Rettet nogle stavefejl i kommentarerne
# Version 1.0 - 23 Okt 2021 - Justeret til nyt LKlib
# Version 0.9 - 21 Okt 2021 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Fokus skal være i det lille sorte vindue, som åbnes når programmet køres.
#  
# Program lukkes med ESC eller X i rammen på det sorte vindue - eller via stop i IDE/Editor (Thonny).

from LKlib import *

#
# Udvid med flere noder og keys hvis I synes - DER SKAL være samme antal elementer i de 2 tabeller!
#

frequency = [  # node og index/position in table/array A-minor med start i middel A (kammertonen).
440,           # A4 - pos 0
494,           # B4 - pos 1
523,           # C5 - pos 2
587,           # D5 - pos 3
659,           # E5 - pos 4
698,           # F5 - pos 5
784            # G5 - pos 6
]

keys=['a', 's', 'd', 'f', 'g', 'h', 'j']  # som mappes til node positionerne


# Funktion der laver tonerne.
# Modificer funktionen for at lave andre toner ved at bruge og kombinere signaler lavet med funktionerne i LKlib.
# Ex ved at addere overtoner. Prøv dem som er udkommenteret.
def make_tones(freq):
#    x = generate_sine(freq)
#    x = env(generate_sine(freq))
#    x = exp_decay(generate_sine(freq))
#    x = generate_triangle(freq)
#    x = env(generate_triangle(freq))
#    x = exp_decay(generate_freq_modulated_sine(freq,fmf=int(freq/2),fmi=5),-3)
#    x = exp_decay(generate_amp_modulated_fmsine(freq,fmf=int(freq/2),fmi=5,amf=8,ami=0.4),-3)
    x = env(generate_amp_modulated_fmsine(freq,fmf=int(freq/2),fmi=10,amf=8,ami=0.2))
    return x

#
# Koden nedenfor læser tastetryk og konverterer til afspilning af lyd!
# Det behøver man ikke at ændre på!!! Udvides tabel overfor fungerer resten stadig!!
#  - Dog kan det tænkes at ændre mellem .play(-1) og .play() for at spille lyd kontinuert eller kun een gang pr tastetryk!!
#

init_mixer()

range_of_tones = range(0, len(frequency))                         # laver tabel med en længde der svarer til liste af frekvenser 
sound_table = [make_tones(frequency[i]) for i in range_of_tones]  # og generere toner ind i tabel
generated_sounds = map(generate_stereo_sound,sound_table)         # og konverterer til lyd filer der kan afspilles af play_sound()

# Mapper taster (keys) og de genererede lyde sammen i et dictionary for let og hurtigt opslag
key_sound = dict(zip(keys, generated_sounds))
# is_playing dictionary for at holde samling på hvilke der er aktive og spiller en lyd - initialiseres alle til False (not playing)
is_playing = {k: False for k in keys}

# Windue med fokus for at kunne få tastaturinput til programmet. (ESC stopper og lukker vinduet)
screen = pygame.display.set_mode((150, 150))

# Så længe run er True tages tastatur input og konverteres til node. Start ved keydown og stop ved keyup.
run = True
while run:
    event = pygame.event.wait()

    if event.type == pygame.QUIT: run = False  # X'ed in window
    else:
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)
            print(key)                                    # test udskrift i shell for at se tast er aktiveret
            if event.key == pygame.K_ESCAPE: run = False
            if (event.type == pygame.KEYDOWN) and (key in key_sound.keys()) and (not is_playing[key]):
                key_sound[key].play(-1)                   # -1 betyder tone spiller indtil den stoppes. Fjernes den så spilles tone kun een gang. 
                is_playing[key] = True
            elif event.type == pygame.KEYUP and key in key_sound.keys():
                key_sound[key].stop()
                is_playing[key] = False

# Ved program exit, ryddes op og vindue fjernes:
pygame.quit()  
            