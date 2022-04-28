# MBType-M.py - Gem i main.py på Micro:Bit når den skal køre selvstændigt og kombineres med et program på PC/PI/MAC
#             - Husk at det skal være med lille m i main.py ellers duer det ikke!
#             - Bruges til at koble til MB sendere som er lavet i makecode
#
# Version 1.0 - 21 Sept 2021 - Lavet modtager som kan bygge bro til sendere lavet i MakeCode - blok programmering.
#
# Type M:
# Program der løbende checer for modtagne indhold på radio kanal 7 (default) gruppe 0 (default) fra MB's der sender strenge
# lavet i blok programmering (Makecode) og piller streng ud - som er kompatibel med Lyd-Kit projektets protokol.
# Når der sendes strenge fra blokprogrammeringen er der diverse andre informationer med og længden af telegram varierer.
# Lagt op til at man sender 3 tegn (ident,type og key). 
#
# Modtages noget på radio sendes det videre på USB.
#
from microbit import *
import radio
#
# Konstanter til at identificere MB, som I skal rette til jeres opstilling
#
MB_TYPE = "M"     # identificerer denne MB som een type M (Modtager fra makecode)... SKAL ikke ændres
CH      =  7      # Den radio kanal I benytter til jeres opstilling/produkt  7 er default og den som bruges i blokprogrammering
                  # hvor kanal ikke kan ændres. Tilgengæld kan de ændre i gruppe nummer, men det bruges ikke i LYD-Kit projektet.
GR      = 0       # Så blokprogrammerings delen SKAL bruge gruppe 0. MEN KAN ÆNDRE GR hvis man vil og bruge det til at skelne!!

#
# Tænde for radio med fuld sende styrke men på specifik kanal som benyttes i opstillingen
#
radio.config(channel=CH,group=GR)    # samme kanal i alle MB's i samme opstilling. 
radio.on()                           # Når der modtages fra MB programmeret i Make kode skal det være kanal 7 (default)
                                     # KAN ændre i group nummer fra makecode så mulighed for at lave forskellige grupper ved at
                                     # ændre i gruppe nummeret!!
#
# For at identificere MB på USB (hvis den er tilsluttet via USB) samt lokalt på MB display
#
print("MicroBit på kanal : "+str(CH)+" med GR!!: "+str(GR)+" og af Typen: "+MB_TYPE)
display.show("K:"+str(CH)+"G:"+str(GR)+"T:"+MB_TYPE)
sleep(1000)
display.clear()
#
# Hoved program der løbende checker om noget er modtaget på radio.
# Er der det forsøger den at pille en streng ud og sende videre på USB/Seriel
#
while True:        # Forever - læse telegrammer fra MB med blokprogrammer og pille sendt streng ud og sende den videre på USB                                                         
 #
    # Hvis der modtages noget på radio sendes det ufilteret/uændret videre på USB.
    #
    r = radio.receive()
    if r :
        # Med test udskrift "print(len(r))" kan det ses at længden varierer og der er forskel på hvilken position
        # de 3 forventede tegn de kommer på, men det passer altid med at de står samme sted fra afslutningen.
        # Kan placering med testudskrift "for i in range(0,len(r)): print(i,"  ",r[i])"
        # Nedenfor pilles de 3 forventede tegn ud og sendes på USB/Seriel til PC/PI/MAC. Se slice i W3Schools.
        if len(r)>20:  # indikation på at det er fra blokprogram og så kan vi lave slice nedenfor uden fejl
            print(r[(len(r)-19):(len(r)-16)])
    sleep(50)
