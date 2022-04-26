# import af bibliotek/modul med random funktionaliteter.
import random
# Liste med navne som tekst strenge
# Index    0      1       2     3      4     - Der er 5 navne i listen - også kaldet længden af listen
navne =['Jens','Peter','Ole','Anne','Sofie']

# Definition af en funktion der bliver døbt til at hedde "hmd".
# Funktion tager et navn som argument og udskriver 4 liniers velkomst i shell
def hmd(n):
    print ('Hej med dig')
    print (n)
    print("Godt at se dig")    # bemærk at både ' og " kan bruges omkring en tekst.
    print()

# Et tilfældigt udvalgt navn fra listen med navne vha importeret random modul/bibliotek
hmd(random.choice(navne))      # virker både i Python og MicroPython