# LKS4-piano-med-scamp-og-KB.py
#
# Program der genererer toner for frekvenserne der svarer til de 12 noder C4 til G5, og mapper dem til Keys på keyboard A-rækken
# Svarer til LKS4-piano-med-scamp-og-MB, hvor noderne mappes til Micro:Bits, men her altså bare med keyboard input
#
# I denne er der tilføjet pitch bend på up og down for sidst aktiverede og aktive node.
#
# Version 1.0 - 20-Jan-2022 - Knud Funch, Soundhub Danmark - LYDKit til undervisningbrug - Region MidtJylland Oprettet.
#
#
# For at denne kode skal virke skal man have installeret biblioteket scamp via Thonny (Tools - Manage Packages)
# for mere om scamp se:
#
# https://pypi.org/project/scamp/
# http://scamp.marcevanstein.com/
#
#

import pygame
from scamp import *     # Til at generere og styre lydene

#
# Konstant til test udskrift.
# Hvis I vil se lidt mere om hvad der sker så sæt TEST_PRINT_ON = True
#
TEST_PRINT_ON = False
MAX_MIDI_TO_RUN = 90
MIN_MIDI_TO_RUN = 40
midi_to_run = MIN_MIDI_TO_RUN

#
# Dictionary der mapper ident og key til midi note
# Udvid hvis I vil have flere noter med.
# Lav anden skala etc .. ..
#
# Reference til midi/frekvens/node: Udleveret regneark "node frekvenser og midi numre.xlsx"

key_to_midi = {   # C-major scale
# Ident+Key    Midi note
   'a':           60,            #   - relateret til C4 in midi 
   's':           62,            #   - relateret til D4 in midi
   'd':           64,            #   - relateret til E4 in midi
   'f':           65,            #   - relateret til F4 in midi
   'g':           67,            #   - relateret til G4 in midi
   'h':           69,            #   - relateret til A4 in midi
   'j':           71,            #   - relateret til B4 in midi
   'k':           72,            #   - relateret til C5 in midi
   'l':           74,            #   - relateret til D5 in midi
   'æ':           76,            #   - relateret til E5 in midi
   'ø':           77,            #   - relateret til F5 in midi
   "'":           79,            #   - relateret til G5 in midi 
}

#
# Liste med instrumenter der kan vælges mellem med F1 og F2 tastetryk
# Liste a med instrumenter der bliver ved med at spille og b for instrumenter der klinger ud forholdsvis hurtigt.
#
# Ud fra den liste I kan få af instrumenter kan I udvide/ændre i listerne nedenfor.
#
instrumenter_a   = ["clavinet","tuba","organ","fiddle","ocarina","poly","sax","oboe"]
instrumenter_b   = ["glock","harpsichord","piano","banjo","guitar","kalimba"]

#
# Keys til special funktioner
#
special_keys = ['f1','f2','up','down']

#
# Variable og deres initial værdi.
#
active_notes = {k: None for k in key_to_midi} 
idx_instrument_a = 0
idx_instrument_b = 0


# ---------------------------------------------------------------------
# Koden nedenfor læser input fra keyboard og konverterer til afspilning af lyd!
# Det behøver man ikke at ændre på!!!
#


#
# Initialiser en scamp session så der kan afspilles notes med syntheziser fra en soundfont.
#
# Bemærk at man vil kunne installere nye soundfonts på PC/MAC/PI som giver nye tonaliteter/nye instrumenter.
#
# Har man fået lagt en ny soundfont ind (på rigtig placering i direktorie struktur) så kan man skifte til den
# ved et kald som nedenfor og derved få andre lyde/udgaver af instrumenterne.
# Laver man sin egen soundfont så er det også her den placeres/vælges.

# Nogle bud på PC og PI - Forudsætning at der ligger soundfonts på det angivne sted/direktorie!!
# Er ikke verificeret på MAC ..
#sti = "C:\\Soundfonts\\"        # I rod på PC dobbelt slash fordi det er et special tegn!!!
#sti = "/home/pi/Soundfonts/"
#
#s = Session(default_soundfont = sti+"TimbresOfHeaven") 
#s = Session(default_soundfont = sti+"FluidR3_GM")
#s = Session(default_soundfont = sti+"SGM-v2.01-CompactGrand-Guit-Bass-v2.7")
#s = Session(default_soundfont = sti+"TimGM6mb")
#

# Default soundfont - virker på alle platforme med den som er med som default, uden at skulle angive sti etc..
s = Session()

# Med kommandoen "s.print_default_soundfont_presets()" kan man få en liste over de instrumenter 
# der findes i den valgte soundfont.
#
s.print_default_soundfont_presets()
# Vælger Oboe som instrument initielt
instrument = s.new_part("Oboe")

# Vindue med fokus for at kunne få tastaturinput til programmet. (ESC stopper og lukker vinduet)
screen = pygame.display.set_mode((150, 150))

# Main loop reading incomming keys from MicroBit and playing back corresponding note
#

run = True
while run:
    event = pygame.event.wait()

    if event.type == pygame.QUIT: run = False  # X'ed i window
    else:
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)
            print(key)
            if event.key == pygame.K_ESCAPE: run = False
            if (event.type == pygame.KEYDOWN) and (key in special_keys):

                if key == "f1":     # vælger et nyt instrument ud fra listen instrumenter_a ved cyklisk af skifte rundt i index_a
                    instrument.end_all_notes()   # uden denne risikerer man at der er en node som bliver 'hængende'
                    active_notes = {k: None for k in key_to_midi}
                    instrument = s.new_part(instrumenter_a[idx_instrument_a])
                    idx_instrument_a += 1
                    if idx_instrument_a == len(instrumenter_a): idx_instrument_a = 0
                    print("f1 done")

                if key == "f2":     # vælger et nyt instrument ud fra listen instrumenter_b ved cyklisk af skifte rundt i index_b
                    instrument.end_all_notes()
                    active_notes = {k: None for k in key_to_midi}
                    instrument = s.new_part(instrumenter_b[idx_instrument_b])
                    idx_instrument_b += 1
                    if idx_instrument_b == len(instrumenter_b): idx_instrument_b = 0
                    print("f2 done")                
                        
                if key == 'up':
                    try:
                        instrument.change_note_pitch(last_playing.note_id,midi_to_run+3,0.2)
                        if midi_to_run < MAX_MIDI_TO_RUN:
                            midi_to_run = midi_to_run+3
                        if TEST_PRINT_ON: print(midi_to_run)
                    except:
                        print("ingen last_playing")

                if key == 'down':
                    try:
                        instrument.change_note_pitch(last_playing.note_id,midi_to_run-3,0.2)
                        if midi_to_run > MIN_MIDI_TO_RUN:
                            midi_to_run = midi_to_run-3
                        if TEST_PRINT_ON: print(midi_to_run)
                    except:
                        print("ingen last_playing")

            
            if (event.type == pygame.KEYDOWN) and (key in key_to_midi):
                last_playing = instrument.start_note(key_to_midi[key],1)
                midi_to_run=key_to_midi[key]
                active_notes[key] = last_playing.note_id
                if TEST_PRINT_ON: print(active_notes)

            if (event.type == pygame.KEYUP) and (key in key_to_midi):
                if TEST_PRINT_ON: print("key og tilhørende node der skal stoppes ",key,":",active_notes[key])
                instrument.end_note(active_notes[key])
                active_notes[key] = None
                if TEST_PRINT_ON: print(active_notes)

#
# Fjern vindue og ryd op.
pygame.quit()

#
# Andre ting man kan forsøge sig med :
# http://scamp.marcevanstein.com/scamp/scamp.instruments.ScampInstrument.html?highlight=scampinstrument
#    instrument.change_note_volume(last_playing.note_id,0.5,10)
