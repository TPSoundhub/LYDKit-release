# -*- coding: utf-8 -*-
# Linien ovenfor er inkluderet for at sikre korrekt håndtering af special tegn (DK) ved start af program fra boot
# (headless).
#
# LKS2Mb-Case3.py - Kode eksempel med en Quiz med 12 lyde der kan matches med 12 taster fra 4 Micro:Bits til PC/MAC/PI
#                 - Micro:Bit kode som hører sammen med dette eksempel findes i LKS2 under MicroBit-Koder-1 som MBType-0.py
#
# Version 2.0 - 18-Jan-2021, Knud Funch, SoundHub Denmark - LYDkit til undervisning - Region Midtjylland
#                            Til test forløb med 1x SSG jan-feb 21 - Simplificeret version af tidligere udgave
#                            Kommentarer på dansk.
# Version 2.1 - 14-Jul-2021, Rettet så Prøve lyd stoppes hvis ny.
# Version 2.2 - 19-Jul-2021, Lavet med 'dict' for at få ensartethed i div moduler.
# Version 2.3 - 20-Jul-2021, Lavet med recovery på tabt forbindelse til MB.
# Version 2.4 - 23-Aug-2021, Rettet op mht navngivning til spor 2
# Version 2.5 - 22-Okt-2021, Rettet div skrivefejl og anvender default volumen fra ny udgave af LKlib aht Headless.
#
# 12 lyde brugt i quiz - fugle sange i udleveret eksempel
# - Kan udskiftes ifm ny quiz efter eget valg uden ellers at lave om i koden.
# - Placer lyd filer i samme direktorie (ellers skal man have sti med i navn)
# - Kan også let udvides til at kunne bruge flere input's. Her 4 stk Microbits (MB) med Type 0 Software og ID 0-3 
# - Tilføjes flere MB's udvides tabellen nedenfor bare tilsvarende med 3 lydfiler pr. MB.
#
# Brug koden med nye lydfiler og lav en ny Quiz uden at iøvrigt at ændre i koden.
# Udvid evt. tabellerne så I får flere lyde og MB's med i Quiz.
# Hvis I vil kikke mere ind i programmet og forstå det bør I først kikke på State/Event diagrammet fra oplæg.

from LKlib import *

#
# Så længe lyd filerne ligger i samme direktorie som programmet, og det startes fra editor (Thonny)
# skal der IKKE angives en sti.
sti = ""
# Hvis I vil lave en pæn direktoriestuktur med lydene i et andet direktorie, eller I vil starte program
# fra kommando promt - for eksempelvis at lave et headles setup med raspberry PI skal I angive sti.
# Der skal man være opmærksom på special tegn. 

# Skal man have programmet til at køre fra Boot på headless setup med PI skal sti defines som nedenfor:
# sti = "/home/pi/LKS2/Mb/Case3/"

#
# Dictionary der mapper ident og key til quiz lyde i wav filer
# For at lave en ny Quiz med andre lyde skal I bare udskifte lydfilerne i direktoriet hvor programet ligger.
# I det medfølgende eksempel med fugle lyde er der følgende lyde i filerne:
#
#          01.wav : Stork
#          02.wav : Ugle
#          04.wav : Spætte
#          11.wav : Svale
#          12.wav : Måger
#          14.wav : Pingvin
#          21.wav : Skovskade
#          22.wav : Gøg
#          24.wav : Solsort
#          31.wav : Hane
#          32.wav : Gæs
#          34.wav : Lærk
#
# Hvis I laver en Quiz med samme antal lyde som den der er i eksemplet med fugle behøver man ikke at ændre i programmet
#
# Udvid hvis I vil have flere Quiz lyde med - husk samtidigt flere Micro:Bits med type 0 og nyt id i rækken.
#

ident_and_key_to_quiz_sound = {
# Ident+Key    navn på Quiz lyd fil
    '01':       sti+"01.wav",      # Lyd 01.wav  - mappes til MB ident "0" key "1"  (MB type 0 kode)
    '02':       sti+"02.wav",      # Lyd 02.wav  - mappes til MB ident "0" key "2"  (MB type 0 kode)
    '04':       sti+"04.wav",      # Lyd 04.wav  - mappes til MB ident "0" key "4"  (MB type 0 kode)
    '11':       sti+"11.wav",      # Lyd 11.wav  - mappes til MB ident "1" key "1"  (MB type 0 kode)
    '12':       sti+"12.wav",      # Lyd 12.wav  - mappes til MB ident "1" key "2"  (MB type 0 kode)
    '14':       sti+"14.wav",      # Lyd 14.wav  - mappes til MB ident "1" key "4"  (MB type 0 kode)
    '21':       sti+"21.wav",      # Lyd 21.wav  - mappes til MB ident "2" key "1"  (MB type 0 kode)
    '22':       sti+"22.wav",      # Lyd 22.wav  - mappes til MB ident "2" key "2"  (MB type 0 kode)
    '24':       sti+"24.wav",      # Lyd 24.wav  - mappes til MB ident "2" key "4"  (MB type 0 kode)
    '31':       sti+"31.wav",      # Lyd 31.wav  - mappes til MB ident "3" key "1"  (MB type 0 kode)
    '32':       sti+"32.wav",      # Lyd 32.wav  - mappes til MB ident "3" key "2"  (MB type 0 kode)
    '34':       sti+"34.wav"       # Lyd 34.wav  - mappes til MB ident "3" key "4"  (MB type 0 kode)
}

#
# Lyde til at indikere rigtigt og forkert svar.
# Lydene som er med fra en start er en "Cheer Crowd" og en "Buu-trombone" lyd
# MEN I kan jo bare bruge en anden lyd med de samme navne sammen med programet for at give en anden 'oplevelse'
# SKAL være en wav fil, gerne i stereo og af kort varighed.
#
cheer_or_buh_sounds = {
  'RIGTIG':     sti+"rigtig.wav",
  'FORKERT':    sti+"forkert.wav"
}

#
# Konstanter, Hvis I vil fjerne test udskrifter så sæt TEST_PRINT_ON = False
#
PRACTICE      = "Øve"
QUIZ          = "Quiz"
TEST_PRINT_ON = True

#
# Variable og deres initial værdi
#

mode        = PRACTICE
playing_idx = 0


#
# Funktion til at starte tilfældig QUIZ lyd.
# Lavet som funktion da den bliver brugt 2 steder i hovedprogrammet.
# - Når man går ind i Quiz mode
# - Når der gættes rigtigt og ny tilfældig lyd skal vælges
# Returner
# - Nøgle til den lyd som er startet så man kan sammeholde med input for rigtigt/forkert svar
# - Kanal som lyden er startet i for at kunne slukke igen for den senere
#
def start_random_quiz_lyd():
    n = random.choice(list(ident_and_key_to_quiz_sound))
    if TEST_PRINT_ON:
        print("Starter Quiz mode med lyd ident/Key: ",n)
    c = play_sound(ident_and_key_to_quiz_sound[n],forever=True)
    return n,c
 
#
# Initialisering af:
#  - seriel port til kommunikation med tilsluttet Micro:Bit.
#  - Lyd mixer, der kan håndtere op til 8 lyde samtidigt. 
ser=init_serial()
init_mixer()

# Spiller en start lyd for at vise programmet er igang med vol sat til 0.3 i både højre og venstre kanal
#
quiz_channel = play_sound(sti+"start-seq.wav")


# Hoved program der løbende læser input fra den serielle kanal og afspiller lyde enten i øve eller i quiz mode.
# Ved at trykke på knap A -> øve mode
# Ved at trykke på knap B -> quiz mode
#
while True:

    modtaget_tuple = get_microbit_input(ser,all_info=True)
    if modtaget_tuple:
        if TEST_PRINT_ON: print(modtaget_tuple, " tuple modtaget på seriel port (MB ident, MB type, MB key, MB value)")
        i,t,k,v = modtaget_tuple

        ident_and_key_input = i+k
        
        if k == "A" and mode != PRACTICE:                          # skift til øve mode efter at have været i quiz mode
            mode = PRACTICE
            stop_sound(quiz_channel)                               # stop afspilning af Quiz lyd
            if TEST_PRINT_ON: print(mode)
        if k == "B" and mode != QUIZ:                              # skift til quiz mode efter at have været i øve mode
            mode = QUIZ
            stop_sound(quiz_channel)                               # stop afspilning af practise lyd
            ident_and_key_playing, quiz_channel = start_random_quiz_lyd()

        if ident_and_key_input in ident_and_key_to_quiz_sound:
            if mode == PRACTICE:
                stop_sound(quiz_channel)
                quiz_channel = play_sound(ident_and_key_to_quiz_sound[ident_and_key_input])
            if mode == QUIZ:
                if ident_and_key_input == ident_and_key_playing:    # Korrekt svar
                    stop_sound(quiz_channel)                        # stop playing quiz lyden
                    play_sound(cheer_or_buh_sounds["RIGTIG"])       # cheer for rigtigt svar
                    time.sleep(6)                                   # vent til cheer er over inden ny quiz lyd startes
                    ident_and_key_playing, quiz_channel = start_random_quiz_lyd()
                else:
                    play_sound(cheer_or_buh_sounds["FORKERT"])      # buuh lyd ved forkert svar

        if k == TABT_FORBINDELSE : ser=init_serial()                # genetabler forbindelse til MB, hvis forbindelse tabt