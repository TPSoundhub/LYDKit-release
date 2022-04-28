# MBType-6.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt og kombineres med et program på PC/PI/MAC
#             - Husk at det skal være med lille m i main.py ellers duer det ikke!
#
# Version 1.1 - 26 aug 2021 - Udgave til frigivelse/spredning i efteråret 2021.
#                           - Ændret navngivning, og rettet kommentarer.
# Version 1.0 - 22 Mar 2021, Knud Funch Sound Hub Danmark. LYD-KIT Region MidtJylland - Oprettet og første test
#
# Type 6: 
#
# Program der løbende checker lyd niveau fra microfon på MicroBit v2. 
# Er lyd niveau over en tærskel værdi sendes "S", og er den under sendes "s" (hvis den inden har været modsat)
# "S" og "s" sendes sammen med MB-id og Type identifikation for at gøre det til et unikt event med flere MB i opstilling.
#
# Modtages noget på radio sendes det videre på USB.
# Derved kan man sætte een MB til PC/MAC/PI og have flere andre der sender på radio og få
# input events fra alle overført til PC/MAC/PI
#
from microbit import *
import radio
import math
#
# Konstanter til at identificere MB, som I skal rette til jeres opstilling
#
MB_TYPE = "6"     # identificerer denne MB som een der sender vippe 'kommandoer' SKAL ikke ændres
MB_ID   = "0"     # nummer på MB når i bruger flere af dem i opstilling for at kunne skelne dem ad
CH      = 60      # Den radio kanal I benytter til jeres opstilling/produkt

# TRESHOLD værdi bestemmer hvor meget 'lyd' der skal være inden den betragtes som høj.
# Den kan I justere (mellem 1 og 255).
#
THRESHOLD = 40      

#
# Variabler til at holde styr på input og sidste ditto så der kun sendes ved ændring.
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
display.show("K:"+str(CH)+"T:"+MB_TYPE+"I:"+MB_ID)
sleep(1000)
display.clear()

microphone.set_threshold(SoundEvent.LOUD,THRESHOLD)
sleep(100)
dummy = microphone.was_event(SoundEvent.LOUD)  # For at fjerne første....
sleep(100)

# Hoved program der løbende checker lyd niveau og sender ændring over/under threshold
   
while True:                        # Forever - genererer events på radio og USB 
                                                                      
    if microphone.was_event(SoundEvent.LOUD):
        key = "S"
    else:
        key="s"
 
    if key != last_key:            # sender kun een gang hvis samme knap/PIN er aktiveret gentagne gange i loop
        event = MB_ID+MB_TYPE+key  # unik event med MB ident,type og key der er aktiveret
        print(event)               # Send streng på USB   - OK selvom MB ikke er tilsluttet via USB
        radio.send(event)          # Send streng på radio - OK selvom MB er tilslutet via USB 
        display.show(key)          # Local feedback på Micro:Bit display.
        sleep(200)
        display.clear()
        last_key=key

   #
    # Hvis der modtages noget på radio sendes det ufilteret/uændret videre på USB.
    #
    r = radio.receive()
    if r :
        print(r)

    sleep(50)                                 # Vent 50 Ms i hoved løkke, så så bliver 'normal' takten for test af sensor input.

