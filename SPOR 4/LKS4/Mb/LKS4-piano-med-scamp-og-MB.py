# -*- coding: utf-8 -*-
# Linien ovenfor er inkluderet for at sikre korrekt håndtering af special tegn (DK) ved start af program fra boot (headless).
#
# LKS4-piano-med-scamp-og-MB.py
#
# Program der genererer toner for frekvenserne der svarer til de 12 noder C4 til G5, og mapper dem til 4
# unikke Micro:Bits af type 0 eller K (identifiers 0,1,2,3), hvilket system/setup mæssigt svarer helt til Quiz (Case 3)
# eksemplet fra Spor 2.
#
# En naturlig progression fra "LKS4-piano-MBtype-0ogK.py" med forbedringer ud fra oplevelsen med dem.
#
# Bemærk der også er en mere analog/flydende oplevelse med input fra MBType-A,B,C og D
# (key= P,X,I,M og value fra hhv et potentiometer, indbygget accelerometer, lysmåler og magnetometer)
#
# Nu genereres lydende af et mere avanceret bibliotek end det vi har i LKlib.
# Et bibliotek der hedder scamp og som vi ikke umiddelbart kan kikke ind i og se hvordan er kodet.
#
# For at koden i denne fil skal virke skal man have installeret biblioteket "scamp" via Thonny (Tools - Manage Packages)
# Mere information om scamp findes på:
#
# https://pypi.org/project/scamp/
# http://scamp.marcevanstein.com/
#
# Scamp benytter sig af de såkaldte Soundfonts, hvor man har optaget lyd og efterbehandlet dem så de
# indeholder alle pitch'es.
#
# Der findes programmer så man selv kan generere sin egen soundfont hvis man skulle få lyst til det.
# Ex.: https://www.polyphone-soundfonts.com/
#
# Version 1.3 - 21-Jan-2021 - Lavet mere 'analog' oplevelse med input fra MB - accelerometer, lydmåler, magnetometer
#                             og potentiometer for illustrationens skyld - Var ikke så tydelig tidligere.
# Version 1.2 - 17-Nov-2021 - Tilføjet sti med soundfonts direktorie som er tilføjet på PI disk image!
#                             Så kan man der opleve andre soundfonts - og laver man sine egne kan man placere
#                             dem der og bruge dem i koden.
# Version 1.1 - 15-Nov-2021 - Tilføjet test på at man ikke starter samme node uden den først er
#                             afsluttet. Efter brug i forløb på SSG der viste at man kan misse en 'tast sluppet'.
# Version 1.0 - 11-Nov-2021 - Rettet til.
# Version 0.1 - 26-Nov-2020 - Knud Funch, Soundhub Danmark - LYDKit til undervisningbrug - Region MidtJylland Oprettet.
#

from LKlib import *     # For at læse MicroBit input
from scamp import *     # Til at generere og styre lydene

#
# Konstant til test udskrift.
# Hvis I vil se lidt mere om hvad der sker så sæt TEST_PRINT_ON = True
#
TEST_PRINT_ON = False

#
# Dictionary der mapper ident og key til midi note
# Udvid hvis I vil have flere noter med. Og tilføj flere Micro:Bit's i opstillingen.
# Lav anden skala etc .. ..
#
# Reference til midi/frekvens/node: Udleveret regneark "node frekvenser og midi numre.xlsx"

ident_and_key_to_midi = {   # C-major scale
# Ident+Key    Midi note
   '01':           60,            #   - relateret til C4 in midi 
   '02':           62,            #   - relateret til D4 in midi
   '04':           64,            #   - relateret til E4 in midi
   '11':           65,            #   - relateret til F4 in midi
   '12':           67,            #   - relateret til G4 in midi
   '14':           69,            #   - relateret til A4 in midi
   '21':           71,            #   - relateret til B4 in midi
   '22':           72,            #   - relateret til C5 in midi
   '24':           74,            #   - relateret til D5 in midi
   '31':           76,            #   - relateret til E5 in midi
   '32':           77,            #   - relateret til F5 in midi
   '34':           79,            #   - relateret til G5 in midi 
}

#
# Liste med instrumenter der kan vælges mellem med A/B tastetryk fra MBType-0 Micro:Bit
# Liste a med instrumenter der bliver ved med at spille og b for instrumenter der klinger ud forholdsvis hurtigt.
#
# Ud fra den liste I kan få af instrumenter kan I udvide/ændre i listerne nedenfor.
#
instrumenter_a   = ["clavinet","tuba","organ","fiddle","ocarina","poly","sax","oboe"]
instrumenter_b   = ["glock","harpsichord","piano","banjo","guitar","kalimba"]

#
# Variable og deres initial værdi.
#
active_notes = {k: None for k in ident_and_key_to_midi} 
idx_instrument_a = 0
idx_instrument_b = 0


# ---------------------------------------------------------------------
# Koden nedenfor læser input fra MicroBit og konverterer til afspilning af lyd!
# Det behøver man ikke at ændre på. Der kan være nok udfordring i at vælge og udvide skala, samt
# bygge nogle gode 'knapper'.
#
# MEN - Det er omvendt en mulighed at dykke ned i det og se om ikke man kan lave andre
# interaktionsformer end 'knapper'. Nede i koden kan man se at eksempler på hvordan
# input fra MBType-A,B,C,D - dvs med key = P,X,I,M og værdier fra ex tilsluttet potentiometer,
# indbygget accelerometer, lys måler og magnet felts måler på simpel vis konverteres til MIDI
# noder. Man kan gå videre ad den vej og håndtere flere/andre parametre, gøre det anderledes,
# koble forskellige sensorer på forskellige instrumenter,parametre osv...
#
# Man kan for eksempel starte med at se på den anden parameter til kaldet "start_note".
# Der står "1" fast i dem alle i denne udgave af programmet.
# Det betyder afspilning med max styrke - men man kan give værdier mellem 0.0 og 1.0 og dermed ændre på lyd
# styrken af den enkelte node som afspilles med kaldet til "start_node"
#
# Hvad med at lave en slags Theremin hvor en sensor styrer pitch (midi node med decimal) og en anden der styrer
# lyd styrken af den node der spilles.
#

#
# Initialisering af:
#  - seriel port til kommunikation med tilsluttet Micro:Bit.
ser=init_serial()

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

# Main loop reading incomming keys from MicroBit and playing back corresponding note
#
while True:
   
    modtaget_tuple = get_microbit_input(ser,all_info=True)
    if modtaget_tuple:
        i,t,k,v = modtaget_tuple
        if TEST_PRINT_ON: print(modtaget_tuple," tuple modtaget på seriel port (MB ident, MB type, MB key, MB value)")

        if k == "A":     # vælger et nyt instrument ud fra listen instrumenter_a ved cyklisk af skifte rundt i index_a
            instrument.end_all_notes()   # uden denne risikerer man at der er en node som bliver 'hængende'
            active_notes = {k: None for k in ident_and_key_to_midi}
            instrument = s.new_part(instrumenter_a[idx_instrument_a])
            idx_instrument_a += 1
            if idx_instrument_a == len(instrumenter_a): idx_instrument_a = 0

        if k == "B":     # vælger et nyt instrument ud fra listen instrumenter_b ved cyklisk af skifte rundt i index_b
            instrument.end_all_notes()
            active_notes = {k: None for k in ident_and_key_to_midi}
            instrument = s.new_part(instrumenter_b[idx_instrument_b])
            idx_instrument_b += 1
            if idx_instrument_b == len(instrumenter_b): idx_instrument_b = 0
            
        if k in ["0","1","2","4"]:   # Der er kommet et key input som program kan håndtere
            
            index = i+k
            if k == "0":
                if   t == "0":                     # Ved type 0 kan vi ikke afgøre hvilken tast der er sluppet.
                    instrument.end_all_notes()  
                    active_notes = {k: None for k in ident_and_key_to_midi}
                elif t == "K":                     # Med type type K ved vi hvilken tast der er sluppet så ..
                    key = chr(v)
                    ident_and_key_to_stop = i+key

                    if ident_and_key_to_stop in active_notes:
                        if TEST_PRINT_ON: print("ident+key og tilhørende node der skal stoppes ",ident_and_key_to_stop,":",active_notes[ident_and_key_to_stop])
                        instrument.end_note(active_notes[ident_and_key_to_stop])
                        active_notes[ident_and_key_to_stop] = None
                        if TEST_PRINT_ON: print(active_notes)

            if index in ident_and_key_to_midi:
                if active_notes[index]:
                    instrument.end_note(active_notes[index]) # for at sikre der aldrig startes 2 noder på samme key (itilfælde af tabt telegram)
                last_playing = instrument.start_note(ident_and_key_to_midi[index],1)   
                active_notes[index] = last_playing.note_id
                if TEST_PRINT_ON: print(active_notes)
#
#  På indput med value laves en mere 'analog' oplevelse ved at konvertere value til et midi nummer med decimal mellem
#  45.0 og 97.0. Nedenfor bare en simpel konvertering. Man kan jo arbejde videre - måske ændre andre parametre ...
#                                             

        if k == "M":   # Fra en MBtype-D, der sender magnetfelstværdier når det ændres      
            midi_node = v/10000+40
            if TEST_PRINT_ON: print("value og midi: ",v,midi_node)
            last_playing = instrument.start_note(midi_node,1)
        
        if k == "P":    # Fra en MBType-A, med et potentiometer koblet på 
            midi_node = (v/20)+45
            if TEST_PRINT_ON: print("value og midi: ",v,midi_node)
            last_playing = instrument.start_note(midi_node,1)

        if k == "I":   # Fra en MBtype-C, der sender lys intensitetsværdier når lys ændres
            midi_node = v/10+50
            if TEST_PRINT_ON: print("value og midi: ",v,midi_node)
            last_playing = instrument.start_note(midi_node,1)

        if k == "X":   # Fra en MBtype-B, der sender accelerationsværdier når den vippes
            midi_node = (v+2100)/40+20
            if TEST_PRINT_ON: print("value og midi: ",v,midi_node)
            last_playing = instrument.start_note(midi_node,1)

        if k == TABT_FORBINDELSE :
            instrument.end_all_notes()       # uden denne risikerer man at der er en node som bliver 'hængende'
            ser=init_serial()                # genetabler forbindelse til MB, hvis forbindelse tabt

#
# Andre ting man kan forsøge sig med :
# http://scamp.marcevanstein.com/scamp/scamp.instruments.ScampInstrument.html?highlight=scampinstrument
#    instrument.change_note_pitch(last_playing.note_id,100,10)
#    instrument.change_note_volume(last_playing.note_id,0.5,10)
