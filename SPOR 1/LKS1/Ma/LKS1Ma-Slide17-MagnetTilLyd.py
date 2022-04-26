# Konvertering af magnetfelts værdier fra MB's indbyggede magnetometer til til lyd (pitch/frekvens)
# afspillet på MB's indbyggede højtaler (V2 af MB) eller på ekstern højtaler/hovedtelefon
# koblet til PIN 0 og GND.
#
# Benytter funktionen/metoden get_field_strength() fra compass i modulet/biblioteket microbit
# til at aflæse magnet feltets styrke, og pitch funktionen/metoden til at spille en frekvens/lyd fra biblioteket
# music, hvorfor de 2 (microbit og music) importeres.
#
# Værdierne fra magnetometer er altid positive og kan gå op til ihvertilfælde 2.5 mill.
# For at få det til at blive en 'fornuftig' (hørbar) frekvens divideres med 1000, og adderer 50.
# MEN skal desuden få det til at være et heltal' og ved normal division (/) får vi decimaler.
# - derfor bruges funktionen int() til at konvertere til heltal!
#
from microbit import *
import music

# Da felt styrken ser ud til at kunne nå op til ca. 2.5 mill og altid er positiv

while True:
    x = compass.get_field_strength()
    print(x)
    music.pitch(int(x/1000)+50)      # Kan også bruge floor division // - Se python aritmetiske operatorer
    sleep(100)