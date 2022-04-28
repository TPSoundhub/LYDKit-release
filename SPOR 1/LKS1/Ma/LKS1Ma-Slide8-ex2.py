# import af bibliotek/modul med random funktionaliteter.
import random

# Definition af funktion der sammenligner parameteren i med konstanten 3,
# og udskriver om i er mindre end, større end eller lig med 3
def lms(i):
    if i<3:
        print(str(i)+" er mindre end 3")  # Kan sammensætte tekster med + str() funktionen laver tal om til tekst.
    elif i>3:
        print(str(i)+" er større end 3")
    else:
        print(str(i)+" er lig med 3")

# metoden/funktionen randrange() fra modulet/biblioteket random finder et tal mellem 0 og 7
# returnerer det og gemmer det i variablen i.
# Efterfølgenden kaldes funktionen lms med i som argument.
i=random.randrange(7)                           # virker både i Python og MicroPython
lms(i)