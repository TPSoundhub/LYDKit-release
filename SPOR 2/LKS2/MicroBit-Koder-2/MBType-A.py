# MBType-A.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt og kombineres med et program på PC/PI/MAC
#             - Husk at det skal være med lille m i main.py ellers duer det ikke!
#
# Version 1.1 - 27 aug 2021 - Udgave til frigivelse/spredning i efteråret 2021.
#                           - Ændret navngivning incl type, og lidt ekstra kommentarer.
# Version 1.0 - 22 mar 2021 - 1. Udgave. LYD-KIT Region MidtJylland
#
# Type A:
# Program der løbende checker analog værdi på pin og sender værdi på radio hhv seriel når ændring i værdi er over en
# given tærskelværdi. Kan ex. bruges sammen med et potentiometer, men også andre analoge målinger herunder fugtighedsmåler.
#
# Er det tilfældet sendes tegn: "P" efterfulgt af en værdi på USB og Radio,
# sammen med MB-id og Type identifikation for at gøre det til et unikt event med flere MB i opstilling.
#
# Værdier sendes løbende med 50 msec interval, men kun hvis der er een tilstrækkelig stor ændring i aflæst værdi siden sidst.
# styret af konstanten TRESHOLD som man kan ændre efter behov.
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
MB_TYPE = "A"     # identificerer denne MB som een der sender analog input værdi fra valg pin. SKAL ikke ændres
MB_ID   = "0"     # nummer på MB når i bruger flere af dem i opstilling for at kunne skelne dem ad
CH      = 63      # Den radio kanal I benytter til jeres opstilling/produkt

#
# Konstant til at definere den PIN som bruges (brug kun 0,1 eller 2 som analog. Hvis andre skal bruges så skal der gøres mere
# Check https://microbit-micropython.readthedocs.io/en/v2-docs/pin.html
# TRESHOLD værdi bestemmer hvor stor en ændring der skal være for at værdi sendes. Så kan jitter undgås.
# Afhænger af kredsløb som er tilsluttet. Et potentiometer er typisk så stabilt mht modstand at der kun er behov for 1 i TRESHOLD.
#
ANALOGPIN = pin1
THRESHOLD = 1      

#
# Variabler til at holde styr på input og hvor stor en ændring. Hvis forskel mellem value og last value er mindre end TRESHOLD
# så sendes der ingen værdi.

value      = 0
last_value = 0

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
# Hoved program der løbende checker om analog værdi er ændret tilstrækkeligt siden sidst aflæsning.
# Hvis det er tilfældet sendes værdi på seriel og radio.
# Desuden checkes for modtaget telegram på radio som så videresendes på seriel.
#

key = "P"
    
while True:                        # Forever - genererer events på radio og USB 
                                                                      
    value = ANALOGPIN.read_analog()
 
    if abs(value-last_value) > THRESHOLD:      # sender kun hvis ændring i værdi er stor nok
        event = MB_ID+MB_TYPE+key+str(value)  # unik event med MB ident,type og key der er aktiveret
        print(event)                          # Send streng på USB   - OK selvom MB ikke er tilsluttet via USB
        radio.send(event)                     # Send streng på radio - OK selvom MB er tilslutet via USB 
        display.show(key)                     # Local feedback på Micro:Bit display. Kan fjernes for at spare strøm.
        last_value=value                      # Her venter vi ikke da aflæsing og afsendelse af værdi ikke skal sløves 
    else: display.clear()                     # så clearer kun display når der IKKE er ændringer i værdi.
    #
    # Hvis der modtages noget på radio sendes det ufilteret/uændret videre på USB.
    #
    r = radio.receive()
    if r :
        print(r)

    sleep(50)                                 # Vent 50 Ms i hoved løkke, så så bliver 'normal' takten for test af sensor input.

