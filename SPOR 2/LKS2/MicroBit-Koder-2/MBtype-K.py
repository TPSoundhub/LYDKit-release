# MBType-K.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt og kombineres med et program på PC/PI/MAC
#             - Husk at det skal være med lille m i main.py ellers duer det ikke!
#
# Version 1.4 - 15 Nov 2021 - Justeret mht timing og større queue (radio) efter test i forløb på SSG (tabte telegrammer med flere MBs)
# Version 1.3 - 27 aug 2021 - Udgave til frigivelse/spredning i efteråret 2021.
#                           - Ændret navngivning incl. type, og lidt ekstra kommentarer.
# Version 1.0 - 20 jul 2021 - Oprettet ud fra type 0 for at kunne lave klaver med individuelle tangenter. 
#
# Type K:
#
# Som type 0 og kompatibel med type 0. Dvs programmer på PI/PC/MAC der fungerer med type 0 også fungerer med Type K.
# Men med Type K kan man sikre at der er mulighed for at afgøre hvilken knap der er deaktiveret, samt få hurtigere respons.
#
# Program der løbende checker om knap a eller b, samt pin 0,1 og 2 på MB er ativeret
# Er det tilfældet sendes tegnene: "A","B","1","2" eller "4" på USB - hvis konstant ON_USB er sat til TRUE - og ellers på Radio
# sammen med MB id og Type identifikation for at gøre det til et unikt event med flere MB i opstilling.
# Har en eller flere af 'knapperne' været aktiveret og ingen længere er aktive så sendes et "0", men "0" efterfølges af
# en værdi, som indikerer hvilken knap der er blevet sluppet. Og der sendes "0" for alle der har været aktiveret.
# Værdien som sendes efter "0" er den værdi tegnet har i tegn tabel og findes med python funktionen ord().
# Den er ikke beskrevet her med vilje - Find den ved at se hvad der sendes :-)
#
# Modtages noget på radio sendes det videre på USB (KUN HVIS konstanten ON_USB er sat til TRUE!!!)
# Er konstanten ON_USB sat til FALSE sendes på radio, men ikke på USB og der checkes heller ikke på om der modtages noget på radio.
#
# Derved kan man sætte een MB til PC/MAC/PI og have flere andre der sender på radio og få
# input events fra alle overført til PC/MAC/PI
#
from microbit import *
import radio
#
# Konstanter til at identificere MB, som I kan rette til i jeres opstilling
#
MB_TYPE = "K"     # identificerer denne MB som type K - SKAL IKKE ÆNDRES
MB_ID   = "0"     # nummer på MB når I bruger flere af dem til flere tangenter på klaviatur
CH      = 65      # Den radio kanal I benytter til jeres opstilling/produkt
ON_USB  = True    # Sæt til True på den som er tilkoblet USB og False på de andre. Så står de ikke og sender på USB og læser på radio..
                  # Tilføjet for at optimere nu når der ikke ventes særlig længe og vi ønkser hurtig respons på tastetryk

#
# Variabler til at holde styr på input og sidste ditto så kun ny/ændrede knap tryk sendes.

last_key_active = [False,False,False,False,False]
display_on = False

#
# Tænde for radio med fuld sende styrke men på specifik kanal som benyttes i opstillingen
#
radio.config(channel=CH,queue=10)     # samme kanal i alle MB's i samme opstilling. Brug nummer som gruppe har fået tildelt
radio.on()                           # queue større end default da der ellers kan blive tabt telegrammer
#
# For at identificere MB på USB (hvis den er tilsluttet via USB) samt kokalt på MB display
#
print("MicroBit på kanal : "+str(CH)+" med ID: "+MB_ID+" og af Typen: "+MB_TYPE)
display.show("K:"+str(CH)+"I:"+MB_ID+"T:"+MB_TYPE)
if ON_USB: display.show("-modtager")
else: display.show("-sender")
sleep(1000)
display.clear()
#
# Hoved program der løbende checker om knap a eller b, samt pin 0,1 og 2 på MB er ativeret og om noget
# er modtaget på radio.
#
idx_to_key = ["1","2","4","B","A"]

def signal_key_state_change(idx,active):
    global display_on
    if active:
        key = idx_to_key[idx]
        val = 0
    else:
        key = "0"
        val = ord(idx_to_key[idx])
        
    event = MB_ID+MB_TYPE+key+str(val)
    if ON_USB: print(event)                         # Send streng på USB   - OK selvom MB ikke er tilsluttet via USB
    else:      radio.send(event)                    # Send streng på radio - OK selvom MB er tilslutet via USB 
    display.show(key)                               # Local feedback på Micro:Bit display viser key
    display_on=True

def no_active_key():
    global last_key_active
    if ((last_key_active[0] == False) and
        (last_key_active[1] == False) and
        (last_key_active[2] == False) and
        (last_key_active[3] == False) and
        (last_key_active[4] == False)):
        return True
    else:
        return False

def check_to_active(idx):
    global last_key_active
    if not last_key_active[idx]:              
        signal_key_state_change(idx,True)         
        last_key_active[idx] = True

def check_to_inactive(idx):
    global last_key_active
    if last_key_active[idx]:              
        signal_key_state_change(idx,False)         
        last_key_active[idx] = False

while True:                        # Forever - genererer events på radio og USB

    if no_active_key() and display_on:
        display.clear()
        display_on=False
                                                                      
    if pin0.is_touched():
        check_to_active(0)
    else:
        check_to_inactive(0)

    if pin1.is_touched():
        check_to_active(1)
    else:
        check_to_inactive(1)

    if pin2.is_touched():
        check_to_active(2)
    else:
        check_to_inactive(2)

    if button_b.is_pressed():
        check_to_active(3)
    else:
        check_to_inactive(3)
        
    if button_a.is_pressed():
        check_to_active(4)
    else:
        check_to_inactive(4)

 
    #
    # Hvis der modtages noget på radio sendes det ufilteret/uændret videre på USB. MEN KUN HVIS ON_USB for at fjerne unødvendig radio komm.
    # Tøm buffer for hurtigere respons (ingen ventetid imellem hvis flere)
    if ON_USB:
        r = radio.receive()
        while r :
            print(r)
            r =radio.receive()
            sleep(1)             # for at give tid til at den serielle bliver tømt

    #
    # For at få hurtigere respons går vi ned på 8 msec pause. Ved 50 msec. kan man fornemme lag/latency i knap respons
    # når det drejer sig om gentagne tryk ved ex. musik fra klaviatur.
    if ON_USB:
        sleep(2)
    else:
        sleep(8)