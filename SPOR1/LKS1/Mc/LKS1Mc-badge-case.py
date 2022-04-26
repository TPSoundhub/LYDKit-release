# LKS1Mc-badge-case.py
# Et eksempel på hvordan badge kan laves. 
# Tilpas evt. funktionalitet.
# Andre lyde og billeder. Evt anden værdi for TÆRSKEL
#
# Først import af nødvendige moduler/funktioner:
#
from microbit import sleep,display,Image
import radio
import music

# Sæt radio op til at kommunikere på bestemt kanal - og tænd for radio så MB kan sende/modtage
radio.config(channel=80,power=0)   # Brug kanal som I har til den enkelte gruppe og sæt power til
radio.on()                         # svageste sendestyrke med power = 0. Tænd for radio'en
#
# Antal omgange i een trigger undersøgelses periode, samt tærskel værdi for at sige nogen er tæt på.
#
ANTAL_OMGANGE = 20
TÆRSKEL       = 14  # Det antal ud af ANTAL_OMGANGE som bruges til at sige der er nu er nok til at sige der er nogen nærved
#
# Tilstande
ALARM = 0
OK    = 1
tilstand = OK # initielt er vi i OK tilstand.
#
# Til at styre en testudskrift i shell med en MB koblet via USB
TEST_UDSKRIFT = False
#
# Trigger funktion, der returnerer True hvis der er nogen for tæt på. Og som udsender 'heart beat'
# Betingelsen er 'bare' at der er modtaget mere end TÆRSKEL 'heart_beats' (post i postkassen)
# ud af det antal gange der checkes post (ANTAL_OMGANGE). 
#
def trigger():
    nof_heart_beats = 0
    for x in range(0,ANTAL_OMGANGE):
        sleep(100)
        radio.send("Heart beat")                  # Hver gang der checkes for besked sendes en (ens funktion i 'begge ender')
        heart_beat = radio.receive()
        if heart_beat:                            # Betingelse "noget modtaget" vs "ingenting modtaget"
            nof_heart_beats = nof_heart_beats + 1       
    if TEST_UDSKRIFT:
        print("Heart Beats, Omg: ",nof_heart_beats,ANTAL_OMGANGE)  # test udskrift i shell
        sleep(100)
    if nof_heart_beats>TÆRSKEL:  
        t = True  # Tæt på
    else:
        t = False # Langt nok fra
    return t
 
def lav_alarm():
    # Lav evt. anden lyd/billed
    # Test udskrift i shell
    if TEST_UDSKRIFT: print("Alarm - Der er een som er kommet for tæt på")
    # Her vises sur smiley og en et lille beep (800Hz, 1/2 sek), som kører i baggrund
    display.show(Image.SAD)
    music.pitch(800,500,wait=True)
    
def gentag_alarm():
    # Lav evt. anden lyd/billed
    # Test udskrift i shell
    if TEST_UDSKRIFT: print("Der er fortsat een for tæt på")
    # Her laver vi bare et lille beep (1800Hz,1/2 sek), som kører i baggrund
    music.pitch(3000,500,wait=True)       
    
def stop_alarm():
    # tilpas med lyd og billed/animation i MicroBit display som I synes det skal være.
    # Her evt. en positiv kvittering, men Alarm stoppes - så det er nok tilstrækkeligt
    # Test udskrift i shell
    if TEST_UDSKRIFT: print("Den der var for tæt på er nu kommet på afstand")
    # Her cleares display og evt lyd stoppes
    display.clear()
    music.stop()

def alt_ok():
    # tilpas med lyd og billed/animation i MicroBit display som I synes det skal være.
    # Test udskrift i shell 
    if TEST_UDSKRIFT: print("Alt OK ingen for tæt på")
    # Her sætter vi midterste pixel til lav intensitet for at indikere badge er i live
    display.set_pixel(2,2,3)         

#
# Hoved program løkke
# Tilstandsmakine Se slide:
#   - Tilstand OK eller ALARM. Event/trigger: close (nærved) eller ikke close (nærved).

while True:
    close = trigger()
    if  close and tilstand == OK:
        lav_alarm()
        tilstand = ALARM
    elif close and tilstand == ALARM:
        gentag_alarm()
    elif not close and tilstand == ALARM:
        stop_alarm()
        tilstand = OK
    else:               
        alt_ok()
