# MBType-B.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt og kombineres med et program på PC/PI/MAC
#             - Husk at det skal være med lille m i main.py ellers duer det ikke!
#
# Version 1.3 - 03 nov 2021 - Rettet fejl med forkert værdi for Z
# Version 1.2 - 26 aug 2021 - Udgave til frigivelse/spredning i efteråret 2021.
#                           - Ændret navngivning incl type, og lidt ekstra kommentarer.
# Version 1.1 - 26 apr 2021 - Tilføjet initiel udskrift af radio kanal aht identifikation ved opstart.
# Version 1.0 - 18 jan 2021 - Udgave brugt ved test i 1x SSG vinter 2021. LYD-KIT Region MidtJylland
#
# Type B:
# Program der løbende checker acceleration og sender værdi på radio hhv seriel når ændring i værdi er stor nok.
# Kan med ændring af konstant sættes til at checke for hhv x,y,z værdi eller en kombination.
# Er det tilfældet sendes tegnene: "X","Y","Z","V" efterfulgt af en værdi på USB og Radio,
# sammen med MB-id og Type identifikation for at gøre det til et unikt event med flere MB i opstilling.
# Værdier sendes løbende med 50 msec interval, men kun hvis der er een tilstrækkelig stor ændring i aflæst værdi siden sidst.
# styret af konstanten THRESHOLD som man kan ændre efter behov.
# Det betyder så at hvis der kommer een værdi så er MB'en blevet bevæget.
# Omvendt vil det at der ikke kommer nogen værdi ikke nødvendigvis betyde at den ligger stille
# - det kan jo være der ikke er strøm på eller at den er udenfor rækkevidde....
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
MB_TYPE = "B"     # identificerer denne MB som een type B (acc med værdier) SKAL ikke ændres
MB_ID   = "0"     # nummer på MB når i bruger flere af dem i opstilling for at kunne skelne dem ad
CH      = 60      # Den radio kanal I benytter til jeres opstilling/produkt

#
# Hvis I vil ændre hvilken akse der måles på kan nedenstående konstant sættes til een af følgende:
#        "X" - for måling i x aksen
#        "Y" - for måling i y aksen
#        "Z" - for måling i z aksen
#        "V" - for kombineret måling fra de 3 akser. V for vektor = math.sqrt(x**2 + y**2 + z**2)

RETNING  = "X"     
THRESHOLD = 30
#
# Variabler til at holde styr på input og hvor stor en ændring. Hvis forskel mellem value og last value er mindre end TRESHOLD
# så sendes der ingen værdi. 

value      = 0
last_value = 0

#
# Tænde for radio med fuld sende styrke men på specifik kanal som benyttes i opstillingen
#
radio.config(channel=CH)     # samme kanal i alle MB's i samme opstilling. 
radio.on()
#
# For at identificere MB på USB (hvis den er tilsluttet via USB) samt kokalt på MB display
#
print("MicroBit på kanal : "+str(CH)+" med ID: "+MB_ID+" og af Typen: "+MB_TYPE)
display.show("K:"+str(CH)+"I:"+MB_ID+"T:"+MB_TYPE)
sleep(1000)
display.clear()


key = RETNING
    
while True:                        # Forever - genererer events på radio og USB 
                                                                      
    acc_x,acc_y,acc_z = accelerometer.get_values()
 
    if   RETNING == "X": value = acc_x
    elif RETNING == "Y": value = acc_y
    elif RETNING == "Z": value = acc_z
    elif RETNING == "V": value = math.sqrt(acc_x**2 + acc_y**2 + acc_z**2)

    if abs(value-last_value) > THRESHOLD:          # sender kun hvis ændring i værdi er stor nok
        event = MB_ID+MB_TYPE+key+str(int(value))  # unik event med MB ident,type og key der er aktiveret
        print(event)                               # Send streng på USB   - OK selvom MB ikke er tilsluttet via USB
        radio.send(event)                          # Send streng på radio - OK selvom MB er tilslutet via USB 
        display.show(key)                          # Local feedback på Micro:Bit display. Kan fjernes for at spare strøm.
        last_value=value
    else: display.clear()
    #
    # Hvis der modtages noget på radio sendes det ufilteret/uændret videre på USB.
    #
    r = radio.receive()
    if r :
        print(r)

    sleep(50)

