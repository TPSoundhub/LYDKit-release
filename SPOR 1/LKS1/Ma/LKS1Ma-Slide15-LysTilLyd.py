# Konvertering af lys intensitet fra MB's indbyggede lyssensor til til lyd (pitch/frekvens)
# afspillet på MB's indbyggede højtaler (V2 af MB) eller på ekstern højtaler/hovedtelefon
# koblet til PIN 0 og GND.
#
# Benytter funktionen/metoden read_light_level() fra display i modulet/biblioteket microbit
# til at aflæse lys niveau, og pitch funktionen/metoden til at spille en frekvens/lyd fra biblioteket
# music, hvorfor de 2 (microbit og music) skal importeres.
#
# Værdierne fra lysmåler er fra 0 til 255. For at få det til at blive en 'fornuftig' (hørbar) frekvens
# ganges lys intensitet med 15 (giver værdier mellem 0 og 15*255 = 3825) og adderer 50 for at komme til
# en frekvens der ligger mellem 50 og 3825+50 = 3875. Altså i det hørbare område og i et område som den indbyggede
# højtaler på MB'en kan reproducere.
#
# For at kunne følge lysintensiteten udskrives den til shell med den indbyggede print() funktion
# Og for at der skal være lidt tid til at høre lyden og se intensiteten udskrevet ventes der 100 msek mellem
# hver omgang i while løkken.
#
from microbit import *
import music

while True:
    x = display.read_light_level()
    music.pitch(x*15+50)            
    print(x)
    sleep(100)