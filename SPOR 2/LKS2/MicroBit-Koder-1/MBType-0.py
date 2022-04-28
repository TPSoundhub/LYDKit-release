# MBType-0.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt og kombineres med et program på PC/PI/MAC
#             - Husk at det skal være med lille m i main.py ellers duer det ikke!
#             - Bruges eksempelvis i Spor 2 Case 3 med et quiz eksempel.
#
# Version 1.3 - 23 aug 2021 - Udgave til frigivelse/spredning i efteråret 2021. Ændret navngivning og lidt ekstra kommentarer.
# Version 1.2 - 20 jul 2021 - Tilføjet vale = tegn for deaktiveret tast som værdi efterfulgt af "0" for at kunne differentiere. 
# Version 1.1 - 26 apr 2021 - Tilføjet initiel udskrift af radio kanal aht identifikation ved opstart.
# Version 1.0 - 18 jan 2021 - Udgave brugt ved test i 1x SSG vinter 2020/2021. LYD-KIT Region MidtJylland
#
# Type 0:
# Program der løbende checker om knap a eller b, samt pin 0,1 og 2 på MB er ativeret
# Er det tilfældet sendes tegnene: "A","B","1","2" eller "4" på USB og Radio, sammen
# med MB id og Type identifikation for at gøre det til et unikt event med flere MB i opstilling.
# Har en eller flere af 'knapperne' været aktiveret og ingen længere er aktive så sendes et "0"
#
# Modtages noget på radio sendes det videre på USB.
# Derved kan man sætte een MB til PC/MAC/PI og have flere andre der sender på radio og få
# input events fra alle overført til PC/MAC/PI
#
from microbit import *
import radio
#
# Konstanter til at identificere MB, som I skal rette til jeres opstilling
#
MB_TYPE = "0"     # identificerer denne MB som een type 0 (knapper)... SKAL ikke ændres
MB_ID   = "0"     # nummer på MB når i bruger flere af dem i ex en Quiz opstilling for at kunne skelne dem ad
CH      = 60      # Den radio kanal I benytter til jeres opstilling/produkt (0-83)

#
# Variabler til at holde styr på input og sidste ditto så kun ny/ændrede knap tryk sendes.
key        = "0"
last_key   = "0"

#
# Tænde for radio med fuld sende styrke men på specifik kanal som benyttes i opstillingen
#
radio.config(channel=CH)     # samme kanal i alle MB's i samme opstilling. Brug nummer som gruppe har fået tildelt
radio.on()
#
# For at identificere MB på USB (hvis den er tilsluttet via USB) samt kokalt på MB display
#
print("MicroBit på kanal : "+str(CH)+" med ID: "+MB_ID+" og af Typen: "+MB_TYPE)
display.show("K:"+str(CH)+"I:"+MB_ID+"T:"+MB_TYPE)
sleep(1000)
display.clear()
#
# Hoved program der løbende checker om knap a eller b, samt pin 0,1 og 2 på MB er ativeret og om noget
# er modtaget på radio.
#
while True:                        # Forever - genererer events på radio og USB 
                                                                      
    if button_a.is_pressed():
        key="A"
    elif button_b.is_pressed():
        key="B"   
    elif pin0.is_touched():
        key="1"
    elif pin1.is_touched():
        key="2"
    elif pin2.is_touched():
        key="4"
    else: key = "0"

    if key != last_key:            # sender kun een gang hvis samme knap/PIN er aktiveret gentagne gange i loop
        event = MB_ID+MB_TYPE+key  # unik event med MB ident,type og key der er aktiveret
        print(event)               # Send streng på USB   - OK selvom MB ikke er tilsluttet via USB
        radio.send(event)          # Send streng på radio - OK selvom MB er tilslutet via USB 
        display.show(key)          # Local feedback på Micro:Bit display viser key
        sleep(200)
        display.clear()
        last_key=key
    #
    # Hvis der modtages noget på radio sendes det ufilteret/uændret videre på USB.
    #
    r = radio.receive()
    if r :
        print(r)

    sleep(50)