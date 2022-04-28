# MBType-5.py - Gem i main.py på Micro:Bit. - Husk at det skal være med lille m i main.py ellers duer det ikke!
#
# Version 1.0 - 22 Mar 2021, Knud Funch Sound Hub Danmark. LYD-KIT Region MidtJylland - Oprettet og første test
#
# Type 5: Analog aflæsning på een PIN og når værdi overstiger TRESHOLD sendes "F" - er den under sendes "f"
# sammen med MB-id og Type identifikation for at gøre det til et unikt event med flere MB i opstilling.
#
# Det kunne ex. være en fugtighedsmåler (elektrisk- ledningsevne mellem 2 poler - eg 2 søm på krokodillenæb)
#
# Modtages noget på radio sendes det videre på USB.
# Derved kan man sætte een MB til PC/MAC/PI og have flere andre der sender på radio og få
# input events fra alle overført til PC/MAC/PI
#
# En opgave kunne være at lave en ny MB type ud fra denne som kan levere 5 forskellige tegn ud fra forskellige
# input niveauer.
#
from microbit import *
import radio
import math
#
# Konstanter til at identificere MB, som I skal rette til jeres opstilling
#
MB_TYPE = "5"     # identificerer denne MB som een type 5 (analog værdi over/under given værdi). SKAL ikke ændres
MB_ID   = "0"     # nummer på MB når i bruger flere af dem i opstilling for at kunne skelne dem ad
CH      = 60      # Den radio kanal I benytter til jeres opstilling/produkt

#
# Konstanter.
# ANALOGPIN til at definere den PIN som bruges (brug kun 0,1 eller 2 som analog).
# Hvis andre skal bruges så læs mere på:
# https://microbit-micropython.readthedocs.io/en/v2-docs/pin.html
# TRIGGER_LEVEL = den værdi man skal være over for at der sendes et "F" og under for at der sendes et "f"
#
# Værdi fra sensor midles da den kan variere fra gang til gang og vi ønsker en mere stabil aflæsning
# Antal gange der midles over bestemmes af konstanten NOF_LIM samt variablen nof_val.
# Dem kan man justere hvis man ønsker 

ANALOGPIN     = pin1
TRIGGER_LEVEL = 300      
NOF_LIM       = 20
#
# Variabler til at holde styr på input og sidste ditto så kun ændret sensor værdi sendes.
key        = "0"
last_key   = "0"

nof_val    = 0
val        = 0

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

    
while True:                        # Forever - genererer events på radio og USB 
                                                                      
    val_new = ANALOGPIN.read_analog()
    val = val+val_new
    # værdi fra sensor midles da den kan vaierer fra gang til gang og vi ønsker en mere stabil aflæsning
    # ud over at midle skal der to ens til inden vi 'anerkender' det som een stabil værdi.

    nof_val+=1
    if nof_val == NOF_LIM:
        nof_val=0
        val_midlet = val//NOF_LIM
        print("m: ",val_midlet) # KUN ved test koblet til PC så værdi kan checkes i shell!!
        val=0
        if val_midlet<=TRIGGER_LEVEL:
            key = "f"
        else:
            key = "F"

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

