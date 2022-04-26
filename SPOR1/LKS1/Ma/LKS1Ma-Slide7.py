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

# En for løkke der for alle navne i listen navne kalder funktionen hmd
for n in (navne):
    hmd(n)
    
# Det samme i modsat rækkefølge vha indexering i listen - man udpeger selv index i listen med navne
print("Længden af listen er: "+str(len(navne)))   # Kan sammensætte tekster med + str() funktionen laver tal om til tekst.
for i in range(len(navne)):
    hmd(navne[len(navne)-i-1])                    # Der er 5 navne, men index går fra 0 til 4.