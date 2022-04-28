# Udlæsnig af lyssensor værdier
from microbit import *

# Lys niveau kan have værdier mellem 0 og 255 i henhold til dokumentation
# Er det også det I oplever?

while True:
    x = display.read_light_level()
    print(x)
    sleep(100)