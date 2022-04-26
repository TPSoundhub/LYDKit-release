# En for løkke, som løber igennem det hørbare frekvensområde fra 20 til 20000Hz i steps af 100Hz
# og afspiller hver frekvens i 100msek.
# Prøv at ændre på tallene og forhold jer til hvad der lyder fornuftigt på MB'ens højtaler.

from microbit import *
import music

for x in range(20,20000,100):
    music.pitch(x)
    sleep(100)
    print(x)

music.stop()