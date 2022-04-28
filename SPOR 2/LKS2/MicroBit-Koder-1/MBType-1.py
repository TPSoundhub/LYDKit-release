# MBType-1.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt og kombineres med et program på PC/PI/MAC
#             - Husk at det skal være med lille m i main.py ellers duer det ikke!
#
# Version 1.2 - 26 aug 2021 - Udgave til frigivelse/spredning i efteråret 2021.
#                           - Ændret navngivning, og lidt ekstra kommentarer.
# Version 1.1 - 26 apr 2021 - Tilføjet initiel udskrft af radio kanal aht identifikation ved opstart.
# Version 1.0 - 18 jan 2021 - Udgave brugt ved test i 1x SSG vinter 2021. LYD-KIT Region MidtJylland
#
# Type 1:
# Program der løbende checker om MB er vippet i een af 4 retninger (eller bare accelereret i een retning)
# Er det tilfældet sendes tegnene: "H","V","F","T" på USB og Radio
# sammen med MB id og Type identifikation for at gøre det til et unikt event med flere MB i opstilling.
# Har MB været vippet og er kommet tilbage til 'vandret' så sendes et "0"
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
MB_TYPE = "1"     # identificerer denne MB som een der sender vippe 'kommandoer' SKAL ikke ændres
MB_ID   = "0"     # nummer på MB når i bruger flere af dem i opstilling for at kunne skelne dem ad
CH      = 60      # Den radio kanal I benytter til jeres opstilling/produkt (0-83)

#
# Hvis I vil ændre 'følsomhed' for hvornår MB er i vandret verus vippet i de 4 retninger så juster nedenstående

LIM_HV = 300
LIM_FT = 700

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
# Hoved program der løbende checker om accelerometer i bestemt retning er over/uner en given værdi
# er modtaget på radio.
#
while True:                        # Forever - genererer events på radio og USB 
                                                                      
    acc_x,acc_y,acc_z = accelerometer.get_values()

    if ((acc_x<LIM_HV) and (acc_x>-LIM_HV)) and ((acc_y<LIM_FT) and (acc_y>-LIM_FT)):
        key ="0"
    else:
        if acc_x>LIM_HV:
            key="H"
        elif acc_x<-LIM_HV:
            key="V"   
        if acc_y>LIM_FT:
            key="T"
        elif acc_y<-LIM_FT:
            key="F"

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

    sleep(50)

