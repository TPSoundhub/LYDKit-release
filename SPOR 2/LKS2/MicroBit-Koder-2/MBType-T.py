# MBType-T.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt og kombineres med et program på PC/PI/MAC
#             - Husk at det skal være med lille m i main.py ellers duer det ikke!
#             - til brug sammen med Tinkerkit med sensorer på de angivne pin's
#             - OBS! Kan sandsynligvis ikke eksekveres indefra Thonny (memory allokation error, men fungerer
#               ved at den bliver gemt som main.py i MB!!
#
# Version 1.2 - 26 aug 2021 - Udgave til frigivelse/spredning i efteråret 2021.
#                           - Ændret navngivning, og rettet kommentarer.
# Version 1.1 - 26 apr 2021 - Tilføjet initiel udskrft af radio kanal aht identifikation ved opstart.
# Version 1.0 - 18 jan 2021 - Udgave brugt ved test i 1x SSG vinter 2021. LYD-KIT Region MidtJylland
#
# Type T:
# Program der løbende checker sensor input fra TinkerKIT sensorer. Det drejer sig om:
# Analog input sensorer:
# - 5 tasters keyboard
# - Potentiometer
# - Fugtigheds måler. Dvs modstand/ledningsevne mellem 2 'tænder' på sensor
# Digitale input sensorer:
# - Crash sensor
# - Bevægelses sensor (PIR)
#
# Når der er sensor input som er 'ny' sendes tegnene:
#
# Er det tilfældet sendes tegnene:
# "K" - for tast aktiveret på Keyboard efterfulgt af en værdi der indikerer hvilken tast (1,2,3,4,5)
# "k" - for ingen tast aktiveret (efter at der har været een aktiveret)
# "C" - for crash sensor aktiveret
# "c" - for crash sensor deaktiveret (efter at have været aktiveret)
# "B" - for bevægelses sensor aktiveret
# "b" - for bevægelses sensor deaktiveret (efter at have været aktiveret)
# "F" - for ny værdi i fugtigheds (modstands) måling efterfulgt af værdi som angiver niveau (1,2,3,4,5)
# "P" - for ny værdi i potentiometer eferfulgt af ny værdi (0-1023)
#
# Tegn og værdier sendes på USB og Radio
# sammen med MB id og Type identifikation for at gøre det til et unikt event med flere MB i opstilling.
#
# Modtages noget på radio sendes det videre på USB.
# Derved kan man sætte een MB til PC/MAC/PI og have flere andre (af forskellig type) der sender på radio og få
# input events fra alle overført til PC/MAC/PI
#
from microbit import *
import radio

#
# Konstanter til at identificere MB, som I skal rette til jeres opstilling
#

MB_TYPE = "T"     # identificerer denne MB som een der sender input fra tinker KIT sensorer. Lav IKKE om!
MB_ID   = "0"     # nummer på MB når I bruger flere af dem i opstilling for at kunne skelne dem ad
CH      = 60      # Den radio kanal I benytter til jeres opstilling/produkt

# Tinker KIT input
# Se: https://www.elecfreaks.com/learn-en/microbitKit/Tinker_Kit/index.html
#
# Pins brugt. Se MicroBit PIN layout på:
# https://microbit-micropython.readthedocs.io/en/v2-docs/pin.html?highlight=pins#module-microbit
# Bruger pin 0,1 og 2 som analog input, og pin 8 og 12 som digital input. Derved kan display stadig bruges.
# Alternativt kan man bruge nogle af de PINs som display benytter men så skal man bruge "display.off()" inden!
#
KEYboard_pin    = pin0
POT_pin         = pin1  
FUGT_pin        = pin2

CrashSensor_pin = pin8
PIRSensor_pin   = pin12

# antal målinger fugt (modstand mellem tænder) midles over
#
NOF_FUGT_LIM   = 20   

#
# Variabler til at holde styr på input og sidste ditto så kun ny/ændrede knap tryk sendes.

key      = "0"
last_key = "0"
last_displayed_key ="0"

#
# variabler til at holde styr på fugt sensor målinger
#
fugt_val  = 0
nof_fugt  = 0
fugt_val_midlet = 0
fval1     = 0
fval2     = 1
fval_old  = 1

# variabel til at holde styr på crash sensor målinger
#
last_crash_val = 1

# variabler til at holde styr på keyboard sensor værdi
#
kval      = 0
kval_old  = 0
last_keyb = "k"

# variabel til at holde styr på bevægelses sensor (PIR) målinger
#
last_pir_val = 0 

# variabel til at holde styr på potentiometer sensor målinger
#
last_pot_val = 0

# set up crash og PIR sensor Når vi bruger een af de frie digitale input så bør vi lave pull up
#
CrashSensor_pin.set_pull(CrashSensor_pin.PULL_UP)
PIRSensor_pin.set_pull(PIRSensor_pin.PULL_UP)

#
# Tænde for radio med fuld sende styrke men på specifik kanal som benyttes i opstillingen
#
radio.config(channel=CH)
radio.on()

#
# For at identificere MB på USB (hvis den er tilsluttet via USB) samt kokalt på MB display
#
# Da vi IKKE bruger nogle af de analoge PIN's der er anvedt af display kan vi bruge display
print("MicroBit på kanal : "+str(CH)+" med ID: "+MB_ID+" og af Typen: "+MB_TYPE)
display.show("K:"+str(CH)+"I:"+MB_ID+"T:"+MB_TYPE)
sleep(2000)
display.clear()

# Hoved program - uendelig løkke der står og tester sensorerne
#
while True:
    # Først læses værdier fra de forskellige sensorer
    key_val  = KEYboard_pin.read_analog()
    pot_val  = POT_pin.read_analog()

    crash_val = CrashSensor_pin.read_digital()
    pir_val = PIRSensor_pin.read_digital()

    # værdi fra fugt sensor midles da den kan vaierer fra gang til gang og vi ønsker en mere stabil aflæsning
    # ud over at midle skal der to ens til inden vi 'anerkender' det som een stabil værdi.
    fugt_val = fugt_val+FUGT_pin.read_analog()
    nof_fugt+=1
    if nof_fugt == NOF_FUGT_LIM:
        nof_fugt=0
        fugt_val_midlet = fugt_val//NOF_FUGT_LIM
        fugt_val=0
        if fugt_val_midlet<150:    fval1 = 1
        elif fugt_val_midlet<300:  fval1 = 2
        elif fugt_val_midlet<450:  fval1 = 3
        elif fugt_val_midlet<600:  fval1 = 4
        else:                      fval1 = 5
        if fval1 == fval2:
            if fval1 != fval_old:
                last_key = "0"
                key = "F"
        fval2=fval1

    # Check om der er ny værdi i crash sensor -
    # den får prioritet da det kan være det kun er en aflæsning med kontakt, som er lig nul i værdi
    # Dernæst er det keyboard der testes da der tilsvarende kan være en enkelt aflæsning med tast aktiveret
    # siden kommer bevægelses, fugtigheds og potentiometer aflæsningerne da de holder værdierne og
    # vil komme igennem senere hvis der skulle være flere på samme tid/ved samme aflæsningsrunde i programmet
    if crash_val == 0 and crash_val != last_crash_val:
        last_crash_val=crash_val
        key = "C"
    elif crash_val == 1 and crash_val != last_crash_val:
        last_crash_val=crash_val
        key="c"
    elif key_val < 600 and last_keyb == "k":
        key       = "K"
        if key_val   < 40:  kval = 1
        elif key_val <  80: kval = 2
        elif key_val < 120: kval = 3
        elif key_val < 400: kval = 4
        elif key_val < 600: kval = 5
    elif key_val >= 600 and last_keyb == "K":
        key       = "k"
        last_keyb = "k"
    elif pir_val == 1 and pir_val != last_pir_val:
        key = "B"
        last_pir_val = pir_val
    elif pir_val == 0 and pir_val != last_pir_val:
        key = "b"
        last_pir_val = pir_val
    elif pot_val != last_pot_val:
        last_key = "0"
        key = "P"
        last_pot_val = pot_val

    # Afsende sensor key og værdi hvis der er sket ændringer i sensor aflæsning

    if key != last_key:
        event = MB_ID+MB_TYPE+key      # unik event med MB ident,type og key der er aktiveret
        last_key=key
        send = True
        if key == "F":
            if fval1 != fval_old:
                event=event+str(fval1)     # tilføj værdi 1-5 for fugt aflæsning
                fval_old=fval1
                last_key = "0"
            else: send = False
        if key == "K":
            if kval != kval_old or last_keyb == "k":
                event=event+str(kval)      # Tilføj værdi 1-5 for aktiveret tast
                kval_old=kval
                last_keyb = "K"
            else: send = False
        if key == "P":
            event=event+str(pot_val)       # tilføj værdi 0-1023 for aktuel potentiometer aflæsning

        if send:
            print(event)                   # Send streng på USB   - OK selvom MB ikke er tilsluttet via USB
            radio.send(event)              # Send streng på radio - OK selvom MB er tilslutet via USB 
            if last_displayed_key != "P":  # hvis ikke potentiometer værdi ændring så lav feedback på display
                display.show(key)
                sleep(200)
            display.clear()
            last_displayed_key = key


    # Hvis der modtages noget på radio sendes det ufilteret/uændret videre på USB.
    #
    r = radio.receive()
    if r :
        print(r)

    sleep(50)
