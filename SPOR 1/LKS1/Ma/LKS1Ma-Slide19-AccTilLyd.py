# Konvertering af g-kraftspåvirknings værdier fra MB's indbyggede accelerometer til til lyd (pitch/frekvens)
# afspillet på MB's indbyggede højtaler (V2 af MB) eller på ekstern højtaler/hovedtelefon
# koblet til PIN 0 og GND.
#
# Benytter funktionen/metoden get_values() fra accelerometer i modulet/biblioteket microbit
# til at aflæse kraftpåvirkningen, og pitch funktionen/metoden til at spille en frekvens/lyd fra biblioteket
# music, hvorfor de 2 (microbit og music) importeres.
#
# Værdierne fra accelerometer i x-aksen er ifølge specifikationen +/- 2000, men kan måle værdier over 2000 ved
# kraftig påvirkning. Ved 'normal' vip højre/venstre får man ca. værdier i området +/- 1100.
# For at få det til at blive en 'fornuftig' (hørbar) frekvens skal det først og fremmest være positivt. Det kan
# man få det til at blive med abs() funktionen, men så kan man ikke skelne højre versus ventre vip. Derfor
# adderes istedet 1500 og så for at være sikre på at det kommer indenfor en fornuftig ranege testes på værdi inden
# kaldet til music.pitch() - MEN det kan laves på andre måder!! De 3907 kommer fra at version 1 af MB går ned hvis
# man bruger en frekvens der er 3907 eller større. Det er ikke tilfældet for version 2!!
#
from microbit import *
import music

while True:
    acc_x,acc_y,acc_z = accelerometer.get_values()
    print(acc_x)                                   
#    music.pitch(abs(acc_x))    # den hurtige løsning - abs() laver neg til pos (istedet for de 3 linier nedenfor)

    freq = acc_x+1500           # adderer tilstrækkelig stor værdi
    if freq>50 and freq<3907:   # tester at det er i området for at være sikker
        music.pitch(freq)
    sleep(50)                   # Venter kun 50msek (hvor der i andre eksempler har stået 100
                                # Det er for at give en lidt mere 'flydende' oplevelse - Prøv forskellen!