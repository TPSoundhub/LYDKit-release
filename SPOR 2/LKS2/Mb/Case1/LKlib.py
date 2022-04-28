# LKlib.py
# -----------------------------------------------------------------------------------------------------------------------
# Basis funktioner ift. lyd kit - en indpakning af de relevante funktioner så de kan abstraheres væk fra
# overordnede programeksempler i Lyd-Kit. De overordnede eksempler bliver derved lettere at overskue, og det understøtter
# tanken om 'lukket bog' hvor man kan bruge de overordnede programmet uden at gå i detaljer med implementation.
#
# Der er mange kommentarer i koden for at forklare den ifm 'åben bog' tilgang. Det kunne have været placeret for sig selv
# og endnu bedre i en readthedocs (se https://readthedocs.org/) online fil, men det blev ikke indenfor udviklingsprojektets
# rammer og er et forbedringspunkt til evt videreudvikling ..
# ------------------------------------------------------------------------------------------------------------------------
#
# Version 3.0  - 25-Okt-2021 Klar til frigivelse som version ved afslutnig af projekt ultimo 2021.
# Version 2.3  - 23-okt-2021 Tilføjet nye funktioner til optionelle moduler i Spor 3 og 4. FM/AM kombineret.. envelope ..
# Version 2.2  - 21-okt-2021 Ryddet op i del med hearlib og tilføjet (udkommenteret) ex med scipy ..
# Version 2.1  - 31-aug-2021 Integration med andre funktionsbiblioteker så der kun er eet i Lyd-Kit. Og ændret navn til LKlib.py 
# Version 2.0  - 19-jul-2021 Seriel med auto detekt .... og reetablering hvis seriel afbrydes.
# Version 1.9  - 05-Maj-2021 Fjernet differentiering i læs fra seriel aht. start fra boot da det ikke er nødvendigt i Raspberry OS fra 2021
# Version 1.8  - 02-Mar-2021 Tilføjet value mulighed fra Micro:Bit
#                Knud Funch, Soundhub danmark - LYDKit til undervisningbrug - Region MidtJylland. 
# ......
# ---------------------------------------------------------------------------------------------------------------------------
# Funktioner til brug i Spor 2 (Byg med sensorer og lyd klip) - Benyttes også i Spor 4 (Byg et elektronisk instrument):
#
#      init_mixer()
#      play_sound(sound)                     med optionelle argumenter:   ,vol_l=INIT_VOL,vol_r=INIT_VOL,forever=False)
#      play_background(sound)                med optionelle argumenter:   ,volume=INIT_VOL,forever=True)
#      stop_background()        
#      set_background_vol(volume)
#      set_channel_vol(ch,vol_l,vol_r)
#      stop_sound(ch)
#
#      init_serial()
#      get_microbit_input(ser)               med optionelle argumenter:   ,all_info=False,test_print=False)
#
# ....................................
#
# Funktioner til brug i Spor 3 (Byg med sinus) - Benyttes også i Spor 4 (Byg et elektronisk instrument):
#
#      play_signal(mono_signal)              med optionelle argumenter:    ,vol_l=1,vol_r=1,forever=False)
#      generate_sine(freq)                   med optionelt argument:       ,amp_max=6000)
#      exp_decay(sig)                        med optionelt argument:       ,fac=-4)
#
# -----Yderligere funktioner (option/avanceret):
#
#      env(sig)                              med optionelle argumenter:    ,attack_f=10,decay_f=2,release_f=5,sustain_level=0.4)
#      generate_triangle(freq)               med optionelt argument:       ,amp_max=6000):
#      generate_freq_modulated_sine(freq)    med optionelle argumenter:    ,amp_max=6000,fmf=100,fmi=1):   
#      generate_amp_modulated_sine(freq)     med optionelle argumenter:    ,amp_max=6000,amf=60,ami=1):
#      generate_amp_modulated_fmsine(freq)   med optionelle argumenter:    ,amp_max=6000,amf=60,ami=1,fmf=100,fmi=1):
#      generate_sweep_by_power()             med optionelle argumenter:    amp_max=6000,duration=DURATION,power=2):
#
# ---------------------------------------------------------------------------------------------------------------------------
# LKlib.py kan (og bør) som et bibliotek placeres i Python Path, men det er bevidst gjort sådan at det er kopieret rundt
# i alle de direktorier som findes ifm Lyd-Kit. Det er for at understøtte muligheden for 'åben bog'. Det ligger ligefor
# at kikke ned i 'motorrummet'. Det kan så samtidigt bruges til at tage en snak om fordelen ved at have det liggende et
# sted fremfor rundt omkring.
#
# ---------------------------------------------------------------------------------------------------------------------------
# En forudsætning for at bruge dette bibliotek er at man via Tools/manage packages i Thonny har installeret følgende:
#
#         - pygame - for at kunne mixe flere lyde.
#         - numpy  - for at kunne regne på tabeller ifm signal generering.
#
#
# Import i hovedprogram med "from LKlib import *" - svarer til at de ting der står i denne fil var i den hvor den inkluderes
# ----------------------------------------------------------------------------------------------------------------------------


#
# Samlet import af de basale biblioteker til alle Spor i Lyd-Kit - for at gøre det lettere at overskue de overordnede programeksempler.
# 
import time
import random
import serial
from serial.tools.list_ports import *
import pygame
import numpy as np  # af hensyn til delen med generering af signaler


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
#
# Funktioner til at afspille lyde og til at læse input fra seriel kanal fra en Micro:Bit type x
# Anvendes i Spor 1 og Spor 4.
# ---------------------------------------------------------------------------------------------

# Konstanter

TABT_FORBINDELSE = '?' # Tegn der returneres fra get_microbit_input(ser) hvis der ikke længere er forbindelse.

SAMPLERATE = 44100     # Sampling frekvens! samples pr. sekund. 2*max freq (Nyquist).

INIT_VOL   = 0.06      # Default niveau for play_sound() og play_background() Passer med PI i Headless!


# Funktion til at initialisere Pygame Mixer.
# Skal kaldes inden man kan bruge funktioner til at afspille lyde.
#
def init_mixer():
    pygame.mixer.init(SAMPLERATE,-16,channels=2)              # Skal ind i hovedprogram for at få startet mixer op.


# --------
# Funktion der afspiller et lydklip fra en lydfil af kort varighed (skal kunne være i hukommelsen).
# Lyd afspilles i en tilgængelig kanal i pygame.mixer.
# Kanal returneres så man senere kan bruge kanal til at stoppe lyd eller ændre på volumen i kanal etc.
# Så den kan kaldes enten ved at skrive:
#   "ch = play_sound(lyd_fil)" eller bare "play_sound(lyd_fil)" hvis man ikke senere skal gøre noget med kanalen.
#
# Der er 8 kanaler som kan bruges samtidigt i mixer.
#
# Parametre:
# - sound       : Den lyd som skal afspilles - skal være en stereolyd (2 spor) af typen wav.
#                 Skal altid angives
# - vol-l,vol_r : Kan sættes til værdi mellem 0 og 1. Kan være forskellige og derved kan lyd panoreres.
#                 Kan udelades i kald, så er default sat til værdi i konstant INIT_VOL.
# - forever     : Kan sættes til True hvorved lyden bliver ved med at gentage sig selv (loop) eller False hvor den kun spilles een gang.
#                 Kan udelades og default er False.
#
# channel returneres sådan at den kan bruges til kontrol senere. Ex. til at panorere dvs ændre styrken i hhv højre og venstre
# Bemærk at None returneres hvis der ikke er en fri channel til at afspille lyd på, og så startes lyden ikke!
#
def play_sound(sound,vol_l=INIT_VOL,vol_r=INIT_VOL,forever=False):
    channel = pygame.mixer.find_channel()
    if channel != None:
        channel.set_volume(vol_l,vol_r)
        if forever:
            channel.play(pygame.mixer.Sound(sound),-1)
        else:
            channel.play(pygame.mixer.Sound(sound))
    return channel                                


# --------
# Funktion der afspiller en længere lyd fra en lydfil af længere varighed (hentes/loades løbende fra filen).
# Lyd afspilles i mixers bagrunds musik afspiller. Der kan kun afspilles een ad gangen, men samtidigt med op til 8 korte lyde i de andre kanaler.
#
# Parametre:
# - sound       : Den lyd som skal afspilles - skal være en stereofil (2 spor) af typen wav.
#                 Skal altid angives
# - volume      : Kan sættes til værdi mellem 0 og 1.
#                 Kan udelades i kald, så er default sat til værdi i konstant INIT_VOL.
# - forever     : Kan sættes til True hvorved lyden bliver ved med at gentage sig selv (loop) eller False hvor den kun spilles een gang.
#                 Kan udelades og default er True.
#
def play_background(sound,volume=INIT_VOL,forever=True):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.set_volume(volume)
    if forever:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()


# --------
# Funktion der stopper baggrunds lyden i mixerens musik kanal.
#
def stop_background():
    pygame.mixer.music.stop()


# --------
# Funktion der sætter baggrunds/music kanalens volume i mixer værdi mellem 0 og 1
# Kan dermed bruges til at justere i volumen efter at baggrundslyden er startet i kaldet play_background()
#
# Parameter:
# - volume      : Kan sættes til værdi mellem 0 og 1.
#                 Kan udelades i kald, så er default sat til værdi i konstant INIT_VOL, men da det også er
#                 default værdi for kaldet play_background() giver det ikke nogen ændring (mening).
#                 Ideen med at bruge denne funktion er for at ændre værdien. At skrue op/ned for lyd styrken.
#                 Man SKAL så holde styr på værdi i hovedprogram for at få det til at fungere.
#
def set_background_vol(volume=INIT_VOL):
    pygame.mixer.music.set_volume(volume)


# --------
# Funktion der sætter en bestemt kanals volume i mixer til enværdi mellem 0 og 1 for hhv venstre og højre udgang.
# Kan dermed bruges til at lave panning mellem de 2 udgange. Skal have kanal fra kaldet play_sound med som argument!
#
# Parametre:
# - ch          : Den kanal som lyd er startet i ved kaldet ch = play_sound().
#                 Skal altid angives for at funktionen kan fungere.
# - vol-l,vol_r : Kan sættes til værdi mellem 0 og 1. Kan være forskellige og derved kan lyd panoreres.
#                 Kan udelades i kald, så er default sat til værdi i konstant INIT_VOL. men da det også er
#                 default værdi for kaldet play_sound() giver det ikke nogen ændring (mening).
#                 Ideen med at bruge denne funktion er for at ændre værdien.
#                 At skrue op/ned for lyd styrken individulet i de 2 udgange og dermed evt panorere lyden
#                 Man SKAL så holde styr på værdier i hovedprogram for at få det til at fungere.
#
def set_channel_vol(ch,vol_l=INIT_VOL,vol_r=INIT_VOL):
    if ch != None: ch.set_volume(vol_l,vol_r)

# --------
# Funktion der stopper afspilning af lyd i given kanal (som skal være aktiv). Kanal skal angives som argument i kaldet.
#
# Parametre:
# - ch          : Den kanal som lyd er startet i ved kaldet ch = play_sound().
#                 Skal altid angives for at funktionen kan fungere.
def stop_sound(ch):
    if ch != None: ch.stop()


# ------
# ------
# Funktioner til at modtage tegn fra Micro:Bit på seriel kanal via USB stikket.
#
# Er lavet sådan at MicroBit og navn på seriel kanal findes automatisk, men man kan også tvinge en opkobling til en
# navngiven seriel port igennem. Hvis ikke MicroBit findes automatisk får man i shell beskrivelse på hvordan man navngiver
# og tvinger opkobling til port igennem.
#

# Lokal funktion til at auto detektere MicroBit. Er ikke tænkt som noget man skal kalde fra hovedprogram.
#
def auto_detect_microbit():
    while True:
        try:
            ports=comports()                       # Læser de aktive serieller porte ind i liste ports!!
            ser = serial.Serial(timeout=2)
            ser.baudrate = 115200
            found=False
            for idx in range(len(ports)):
                if ports[idx].pid==516:            # Det id som MicroBit v1 og v2 udstiller når den bliver spurgt!
                    ser.port = ports[idx].device
                    found=True
                    ser.open()
                    print("Port åbnet initielt :", ports[idx].device)
                if found:break
            if found:
                return ser
            else:
                raise serial.SerialException("Kan ikke finde nogen tilsluttet Micro:Bit på seriel port") 
        except serial.SerialException as e:
            print("")
            print(e)
            print("Bliver ved med at prøve - ifald Micro:Bit ikke er sat i stik")
            print("Hvis Micro:Bit er sat i stik så stop program og prøv at angive port navn i kaldet til init_serial")
            print("  - På MAC: ""/dev/cu.usbmodem14102""  Evt. andet ciffer i position 3 (14x00)")
            print("  - På PC: ""COM1""                    Typisk med et andet nummer end 1")
            print("  - På PI:""/dev/ttyACM0""             Evt. med andet nummer end 0")
            print("Kan finde port navn ved at klikke i Thonny - Run - select interpreter Micro:Bit - Port")
            print("")
            time.sleep(5)


# --------
# Funktion der finder og initialiserer seriel port med tilkoblet Micro:Bit.
# Den serielle port (ser) returneres og skal bruges i efterfølgende kald til get_microbit_input(ser).
# I hoved program skal man således kalde funktionved at skrive "ser = init_serial()".
#
# Parameter:
# - port_name   : Kan sættes til en streng der repræsenterer en specifik port.
#                 Kan udelades i kald, og så forsøger funktionen selv at finde port med MicroBit tilsluttet.
#                 Det fungerer både på Raspberry PI (Raspberry OS), PC (Windows) og MAC (Mac OS).
#                 Skal man/vil man gøre det manuelt er strengen man skal bruge i kaldet:
#                 - På MAC: ""/dev/cu.usbmodem14102""  Evt. andet ciffer i position 3 (14x00)")
#                 - På PC: ""COM1""                    Typisk med et andet nummer end 1")
#                 - På PI:""/dev/ttyACM0""             Evt. med andet nummer end 0")
#                 man kan finde port navn ved at klikke i Thonny - Run - select interpreter Micro:Bit - Port"
#
def init_serial(port_name="auto"):
    if port_name == "auto":
        ser = auto_detect_microbit()
    else:
        ser = serial.Serial(timeout=2)
        ser.baudrate = 115200
        ser.port = port_name
        ser.open()
        
    return ser

# --------
# Funktion der modtager input event fra een eller flere MicroBit's i opstilling.
# Een af MB'erne skal være koblet til PC/MAC/PC via USB kabel.
# Resten af MB'erne sender events via radio. Deres input kommer til PC/MAC/PI via den ene MB som er koblet via USB
# Man kan skelne de enkelte MB's ved hjælp af type og ident nummerering. Se MicroBit type x under microbit koder.
#
# Parametre:
# - ser         : Den serielle port som er fundet ved kaldet ser = init_serial().
#                 Skal altid angives for at funktionen kan fungere.
# - all_info    : Kan sættes til True, hvorved funktion returnerer et sæt af værdier (ident,type,key,val)
#                 Kan udelades og så er den default sat til False, hvorved funktion bare returnerer key som tegn.
#                 Derved kan man lave enkel og overskuelig kode i hovedprogram, hvis man ikke har brug for flere informationer
# - test_print  : Kan sættes til True, hvorved man får en udskrift i shell på hvad der modtages på den serielle port.
#                 Kan udelades og så er default sat til False, hvor man ikke får nogen testudskrift.
#
# Funktion returnerer None, hvis der efter timeout ikke er modtaget noget fra den serielle kanal.
#
# Hvis der modtages noget returneres med (hvis all_info=True - ellers kun Key):
# - Ident : Acsii tegn for at identificere MicroBit - se mere i beskrivelsen af MicroBit type x
# - Type  : Acsii tegn for at identificere MicroBit type - se mere i beskrivelsen af MicroBit type x
# - Key   : Acsii tegn for at identificere MicroBit event/sensor input - se mere i beskrivelsen af MicroBit type x
# - val   : evt een værdi afhængig af den type MicroBit der er tilsluttet. 0 hvis MB ikke sender en værdi
#
# Hvis forbindelse til MicroBit er tabt af en eller anden grund (USB-kabel trukket ud eller en kortslutning med 3V)
# returners med ?,?,?,0 (konstant TABT_FORBINDELSE = '?') så kan man i hovedprogram lave en genetablering af forbindelse med
# ser=init_serial()
#
def get_microbit_input(ser,all_info=False,test_print=False):
    try:
        microbitdata = str(ser.readline())
        if test_print: print(len(microbitdata),microbitdata)
        if len(microbitdata)>3:
            mb_id   = microbitdata[2]
            mb_type = microbitdata[3]
            mb_key  = microbitdata[4]
            mb_val = 0
            if len(microbitdata)>10:
                mb_val_str  = microbitdata[5:len(microbitdata)-5]                 
                if test_print: print("val str: ",mb_val_str," length val str: ",len(mb_val_str))
                try:
                    mb_val = int(mb_val_str)
                except:
                    mb_val= 0
                    if test_print: print("Kunne ikke konvertere modtaget værdi til et heltal")
            if all_info:
                return mb_id,mb_type,mb_key,mb_val
            else:
                return mb_key
        else: return None                       # when there is a timeout on the inputs -> no input from MB
    except serial.SerialException as e:
        print("Tabt forbindelsen til Micro:bit - Er den faldet ud af stikket? Genetabler og Genstart!")
        print(e)
        print("Kan checke for det og forsøge at reetablere kontakt til Micro:Bit ved at bruge følgende i hovedprogram:")
        print("        if k == TABT_FORBINDELSE : ser=init_serial() ")
        print("da get_microbit_input vil returnere ""TABT FORBINDELSE"" (?) i: i,t,k")
        print("")
        time.sleep(2)
        if all_info:
            return TABT_FORBINDELSE,TABT_FORBINDELSE,TABT_FORBINDELSE,0
        else:
            return TABT_FORBINDELSE

#
#
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
#
# Funktioner til at generere og afspille signaler. Bruges i Spor 3 og 4
# ---------------------------------------------------------------------------------------------
#
DURATION   = 1.0    # Længden af signal der genereres i sekunder.

# --------
# Funktion der ud fra et mono signal genererer en stereo lyd, som kan afspilles med play_sound (pygame mixer).
# Returnerer lyden som kan afspilles. Er ikke tænkt til at blive kaldt fra hovedprogram, da det typisk er
# via funktionen play_signal() som benytter generate_stereo_sound().
#
# Parameter:
# - mono_signal    : Et numpy array med SAMPLERATE*DURATION antal heltal værdier i int16 format, som
#                    repræsenterer et mono signal ex. genereret vha generate_sine() - altså en sinus kurve med hørbar frekvens.
#
def generate_stereo_sound(mono_signal):
    signal_left = mono_signal
    signal_right = mono_signal
    # samme signal i både venstre og højre udgang - og arrangeret i memory sådan at pygame make sound kan håndtere det.
    stereo_signal = np.array((signal_left,signal_right)).T.copy()
    sound = pygame.sndarray.make_sound(stereo_signal)
    return sound

# --------
# Funktion der ud fra et mono signal genererer en stereo lyd og afspiller den vha play_sound() (se den funktion tidligere)
# Kanal returneres så man senere kan bruge kanal til at stoppe lyd eller ændre på volumen i kanal etc.
# Den kan kaldes enten ved at skrive:
#   "ch = play_signal(sig)" eller bare "play_signal(sig)", hvis man ikke senere skal gøre noget med kanalen.
#
# Da man kan starte lyd stort set samtidigt i flere kanaler ved gentagne kald til funktionen kan man ved at angive volume i
# hhv. venstre og højre udgang til hhv 0 og 1 blande 2 forskellige signaler i luften ved at afspille de 2 signaler i de 2 højtaler
# udgange samtidigt. Ex: (findes som Eksempel 2 i Spor 3): Genererer stødtoner i mediet (luft) med 2 rene toner i de 2 udgange.
#
#                   sig1 = generate_sine(440)
#                   sig2 = generate_sine(443)
#                   play_signal(sig1,1,0)
#                   play_signal(sig2,0,1)
#
# Parametre:
# - mono_signal : Det signal som skal afspilles - skal være et mono signal dvs et numpy array med SAMPLERATE*DURATION længde.
#                 Skal altid angives
# - vol-l,vol_r : Kan sættes til værdi mellem 0 og 1. Kan være forskellige og derved kan 2 lyde blandes i de 2 udgange.
#                 Kan udelades i kald, så er default sat til 1 (fuld styrke i begge forstærker/højtaler udgange)
#                 - overordnet volume styres med master vol gennem PC/MAC/PI's GUI.
# - forever     : Kan sættes til True hvorved lyden bliver ved med at gentage sig selv (loop) eller False hvor den kun spilles een gang.
#                 Kan udelades og default er False. Ved False venter koden med at returne til hovedprogram indtil lyd er færdig afspillet!
#
# channel returneres sådan at den kan bruges til kontrol senere.
# Ex. til at panorere dvs ændre styrken i hhv højre og venstre eller til at stoppe lyden med stop_sound()
# Bemærk at None returneres hvis der ikke er en fri channel til at afspille lyd på, og så startes lyden ikke!
#
def play_signal(mono_signal,vol_l=1,vol_r=1,forever=False):
    sound = generate_stereo_sound(mono_signal)
    channel = play_sound(sound,vol_l,vol_r,forever)
    if forever == False:
        time.sleep(DURATION+0.2)                            # Lad lyden spille til ende inden funktionen returnerer.
    return channel


# --------
# Funktion der genererer og returnerer et sinus signal med den frekvens der angives som argument.
# Ex genereres ren sinus tone med frekvensen 440 (kammertonen) med:
#        kammertonen = generate_sine(440)
# hvor kammertonen så kan bruges i play_signal(kammertonen) efterfølgende for at høre den afspillet.
#
# Parametre:
# - freq        : Den frekvens man ønsker signal lavet i.
# - amp_max     : Amplituden. Dvs den største værdi signalet skal have.
#                 Kan udelades og så vil den bruge default værdi på 6000. Men man kan give et argument som har en anden værdi
#                 for højere eller lavere amplitude (signal højde - volume/loudness - relativt til de 16bit som lydkort kan håndtere)
#                 Hvis man efterfølgende begynder at lægge signaler sammen skal man sikre sig at man ikke får værdier
#                 der overstiger +/- 32,767  (signed 16 bit integer - som er det lydkortet kan håndtere)
#                 Der er IKKE noget der går i 'stykker' hvis det sker men det kommer til at lyde mærkeligt. Signalet bliver
#                 digitalt klippet af - men prøv det endelig for at høre effekten.
#
def generate_sine(freq,amp_max=6000):  
    t = np.arange(0,DURATION,1/SAMPLERATE)            
    sine = (amp_max*np.sin(freq*2*np.pi*t)).astype(np.int16)
    return sine

# --------
# Funktion der kan bruges til at give en overordnet form på signal hen over den periode (DURATION) signalet laves til. Ex:
#      sig = generate_sine(440)
#      signal_med_aftagende_styrke = exp_decay(sig)
#
# Parametre:
# - signal : Det signal som skal ganges med 'form' - skal være et mono signal dvs et numpy array med SAMPLERATE*DURATION længde.
# - fac    : med negative værdier i fac så dæmpes signal over tid - simpel udgave af en envelope (bruger en exponentiel funktion)
#            med positive værdier øges signal over tid indtil der går digital overflow og digitale 'fejl' i det.
#            Kan udelades og så bruges default -4, så værdier i 'form' går fra 1 til e opløftet til -4 (0.0183) over signalets længde.
#
def exp_decay(sig,fac=-4):
    x1  = np.linspace(0,fac,int(DURATION*SAMPLERATE),endpoint=False)
    y1  = np.exp(x1)
    s   = (y1*sig).astype(np.int16)
    return s


#
# ---------------------
# Yderligere (lidt mere avancerede) funktioner til at generere signaler - Tilvalg/Option
#
# Bemærk at det stadig er simple funktioner, som kun opererer på basale signaler og er statiske i natur.
# Vil man dybere i det skal man dybere med diskret matematik og digital signal behandling.. ;-)
# - Tale om tidsdomæne, frekvensdomæne bruge også de komplekse tal .... .. .
# - Gå dybere i emner som Frekvensanalyse, spektrum etc. .. ..
#
# Ambitionen med Lyd-Kit er kun at give en introduktion og holde det i samme 'digitale' univers for
# alle spor i Lyd-Kit - både at bygge med lyd klip og sensorer samt vise nogle grundlæggende ting omkring signaler og lyd
# som så igen kan bruges til at bygge basale elektroniske instrumenter med.
#
# LKlib kan udvides over tid med andre funktioner og evt. bedre funktioner over tid..
#
# Se ex.: som inspiration: https://www.youtube.com/watch?v=spUNpyF58BY.
#

# --------
# Funktion der kan bruges til at give en overordnet form på signal hen over den periode (DURATION) signalet laves til.
# Form på signal overordnet set over tidsperioden:  Envelope = Attack, Decay, Sustain, Release (ADSR)
# Ex:
#      sig = generate_sine(440)
#      signal_med_envelope = env(sig)
#
# Parametre:
# - signal       : Det signal som skal ganges med 'form' - skal være et mono signal dvs et numpy array med SAMPLERATE*DURATION længde.
# - attack_f
# - decay_f
# - release_f
# - sustain_level: Værdier der er med til at give formen i 4 faser attack, decay,sustain og release (ADSR) som er begreber der
#                  anvendes på sythesizere - elektroniske instrumneter..
#                  KAN (BØR) udelades, og så er der default værdier, som giver en form hvor:
#                  Attack  er over 1/10 af signalets samlede længde og går fra 0 til 1 i værdi
#                  Decay   er over 1/2  af signalets samlede længde (efter attack) og går fra 1 til værdi i sustain_level (default 0.4)
#                  Sustain er over 1/5 (resten iforhold til de øvrige der samlet bliver 8/10 af signalets længde) hvor niveau fastholdes.
#                  Release er over 1/5  af signalets samlede længde (placeret sidst) og går fra sustain level til 0.
#
#                  Kan ændre _f værdierne så man får en anden form, men pas på! Må ikke være nul med den gældende implementation, og
#                  1/attack_f+1/decay_f+1/release_f skal være mindre end 1 - så der er plads til sustain og kan holdes indenfor
#                  signalets samlede længde!!!
#
def env(sig,attack_f=10,decay_f=2,release_f=5,sustain_level=0.4):
    attack_l   = len(sig) // attack_f
    decay_l    = len(sig) // decay_f
    release_l  = len(sig) // release_f
    sustain_l  = len(sig) - (attack_l + decay_l + release_l)

    attack     = np.linspace(0, 1,             num=attack_l)
    decay      = np.linspace(1, sustain_level, num=decay_l)
    release    = np.linspace(sustain_level, 0, num=release_l)
    sustain    = np.ones(sustain_l) * sustain_level
    envelope   = np.concatenate((attack, decay, sustain, release))
    env_sig    = (envelope*sig).astype(np.int16)
    return env_sig

# --------
# Funktion der genererer og returnerer et triangel formet signal med den frekvens der angives som argument.
# Ex genereres ren triangel tone med frekvensen 440 (kammertonen) med:
#        kammertonen = generate_triangle(440)
# hvor kammertonen så kan bruges i play_signal(kammertonen) efterfølgende for at høre den afspillet.
#
# Parametre:
# - freq        : Den frekvens man ønsker signal lavet i.
# - amp_max     : Amplituden. Dvs den største værdi signalet skal have.
#                 Kan udelades og så vil den bruge default værdi på 6000. Men man kan give et argument som har en anden værdi
#                 for højere eller lavere amplitude (signal højde - volume/loudness - relativt til de 16bit som lydkort kan håndtere)
#                 Hvis man efterfølgende begynder at lægge signaler sammen skal man sikre sig at man ikke får værdier
#                 der overstiger +/- 32,767  (signed 16 bit integer - som er det lydkortet kan håndtere)
#                 Der er IKKE noget der går i 'stykker' hvis det sker men det kommer til at lyde mærkeligt. Signalet bliver
#                 digitalt klippet af - men prøv det endelig for at høre effekten.
#
def generate_triangle(freq,amp_max=6000):
    t = np.arange(0,DURATION,1/SAMPLERATE)            
    triangle = (amp_max*2/np.pi*np.arcsin(np.sin(freq*2*np.pi*t))).astype(np.int16)
    return triangle

# --------
# Funktion der genererer og returnerer et sinus signal som er frekvens modelleret med den frekvens der angives som argument.
# 
# Parametre:
# - freq        : Den frekvens man ønsker signal lavet i. altså hovedsignalet som lydens pitch er bestemt af
# - amp_max     : Amplituden. Dvs den største værdi signalet skal have.
#                 Kan udelades og så er default 6000
# - fmf         : frekvens på modulations signalet
#                 Kan udelades. Så er default 100, som tydeligt kan ses på plot (og høres). Bør også prøves med andre værdier.
#                               En frekvens der er et rent forhold til frekvens på carrier giver noget der lyder harmonisk.
# - fmi         : index som ganges på modulations signalet. Giver et forhold mellem amplityderne på de 2 signaler (carrier og modulator)
#                 Kan udelades. Så er default 1. Bør prøves med andre værdier (større end 1)
#
def generate_freq_modulated_sine(freq,amp_max=6000,fmf=100,fmi=1):   
    t = np.arange(0,DURATION,1/SAMPLERATE)
    fm_signal = (amp_max*(np.sin(freq*2*np.pi*t+fmi*np.sin(fmf*2*np.pi*t)))).astype(np.int16) 
    return fm_signal

# --------
# Funktion der genererer og returnerer et sinus signal som er amplitude modelleret med den frekvens der angives som argument.
# 
# Parametre:
# - freq        : Den frekvens man ønsker signal lavet i. altså hovedsignalet som lydens pitch er bestemt af
# - amp_max     : Amplituden. Dvs den største værdi signalet skal have.
#                 Kan udelades og så er default 6000
# - amf         : frekvens på amplitude modulations signalet
#                 Kan udelades. Så er default 60, som tydeligt kan ses på plot (og høres). Bør også prøves med andre værdier.
# - ami         : index som ganges på modulations signalet. Giver et forhold mellem amplityderne på de 2 signaler (carrier og modulator)
#                 Kan udelades. Så er default 1, som betyder at amplituden i samlet signal går til 0.
#                 Bør prøves med andre værdier (mindre end 1 - ex 0.5 som betyder samlet signal går til 0.5 istdet for 0)
#
def generate_amp_modulated_sine(freq,amp_max=6000,amf=60,ami=1):
    t = np.arange(0,DURATION,1/SAMPLERATE)    
    am_signal = (amp_max*(1+ami*np.sin(amf*2*np.pi*t))*np.sin(freq*2*np.pi*t)).astype(np.int16)
    return am_signal

# --------
# Funktion der genererer og returnerer et sinus signal som er frekvens modelleret og derefter amplitude modelleret.
# 
# Parametre:
# - freq        : Den frekvens man ønsker signal lavet i. altså hovedsignalet som lydens pitch er bestemt af
# - amp_max     : Amplituden. Dvs den største værdi signalet skal have.
#                 Kan udelades og så er default 6000
# - fmf,
# - fmi,
# - amf,
# - ami         : som for hhv frekvens og amplitude modulations funktionerne
#
def generate_amp_modulated_fmsine(freq,amp_max=6000,amf=60,ami=1,fmf=100,fmi=1):
    t = np.arange(0,DURATION,1/SAMPLERATE)    
    am_signal = (amp_max*(1+ami*np.sin(amf*2*np.pi*t))*np.sin(freq*2*np.pi*t+fmi*np.sin(fmf*2*np.pi*t))).astype(np.int16)
    return am_signal

# --------
# Funktion der genererer og returnerer en simpel swipe ud fra en opløft til power på alle punkter.
# Som illustration til at det er bedre end at prøve at stykke den sammen selv i hoved program.
# At man skal lave selve signalet vha matematik, men det kan gøres bedre ... .. .
# 
# Parametre:
# - amp_max     : Amplituden. Dvs den største værdi signalet skal have.
#                 Kan udelades og så er default 6000
# - duration    : Længden af swipe
#                 Kan udelades og så er default = DURATION (som er længden for andre signaler i LKlib)
# - power      :  Det som alle datapunkter opløftes til inden sinus funktionen anvendes på dem.
#                 Kan udelades og så er default = 2. Med højere værdier så bliver der digitale fejl/overløb, men prøv bare med 3 og 4
#                 -> 'sjove effekter' (sammen med duration som er længere end default)
#
def generate_sweep_by_power(amp_max=6000,duration=DURATION,power=2):
    t1  = np.linspace(0,duration*5*2*np.pi,int(duration*SAMPLERATE),endpoint=False)
    t2 = np.power(t1,power)  # Alle datapunkter i x1 bliver opløftet til værdi i t2 på samme position (alle værdier i t2 indeholder POWER som værdi)
    sweep = (np.sin(t2)*amp_max).astype(np.int16)
    return sweep

#
# -----------------------------
# Yderligere vej ind i signal behandling via biblioteket Scipy - MEN er udkommenteret og dermed overladt til den enkelte at arbejde videre med. 
#
# Ved at bruge biblioteket scipy kan man få flere og mere avancerede muligheder
# Det har vi valgt IKKE at bringe ind i LYD-KIT, men for illustrationens skyld er der nedenfor et par udkommenterede
# eksempler, som man kan tage ind hvis man synes.
#
# Der er også funktioner til ex. at lave frekvensanalyse. FFT.
#
#
# se mere: https://docs.scipy.org/doc/scipy/reference/signal.html
#


#from scipy import signal

#def generate_square(freq,amp_max=6000):  
#    t = np.arange(0,DURATION,1/SAMPLERATE)
#    square  = (signal.square(freq*2*np.pi*t)*amp_max).astype(np.int16)
#    return square

#def generate_sawtooth(freq,amp_max=6000):  
#    t = np.arange(0,DURATION,1/SAMPLERATE)
#    sawtooth  = (signal.sawtooth(freq*2*np.pi*t)*amp_max).astype(np.int16)
#    return sawtooth
#

#
# see: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.chirp.html#scipy.signal.chirp
#

#def generate_chirp(start_f=50,slut_f=12000,amp_max=6000):
#    t = np.arange(0,DURATION,1/SAMPLERATE)
#    chirp = (amp_max*signal.chirp(t,start_f,1,slut_f)).astype(np.int16)
#    return chirp