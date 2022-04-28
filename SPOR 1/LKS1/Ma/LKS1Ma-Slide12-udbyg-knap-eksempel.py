# Udbygget button eksempel med lyd - spiller kammertonen ved tryk på a
# importer både det generelle microbit bibliotek og det med music funktionerne
from microbit import *
import music
import speech

while True:
    if button_a.is_pressed():
        display.show(Image.HAPPY)
        music.pitch(440)           # bliver ved med at spille til det stoppes når ingen anden parameter angives
#        speech.say("Hello world") # Prøv denne istedet
    elif button_b.is_pressed():
        break
    else:
        display.show(Image.SAD)
        music.stop()               # stop music når knap a ikke er nedtrykket/aktiveret

# Her kommer vi til når der er en break i while løkken - når knap b bliver aktiveret
# Der stopper vi også music og rydder op i display
display.clear()
music.stop()