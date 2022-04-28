# LKS3-Ex2-interferens-luft.py
#
# Program til at eksperimentere med konstrruktiv og destruktiv interferens i luft. 
#
# Version 2.0 - 21-okt-2021 - Justeret til frigivelse
# Version 1.0 - 25-Nov-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Ved at ændre i argumenterne til de 2 play_signal kald kan man lave eksperimenter og forsøg med
# - Lyd tryk fra een hhv 2 højtalere (der hver har samme udgang)
# - Destruktiv interferens med modsat signal i een højtaler (og sammenligne med Ex. 1)
# - Stød toner med 2 rene toner i de 2 højtalere, og dermed noget der opstår i mediet (luften) fremfor i selve signalet (Ex1)
# - Konstruktiv og destruktiv interferens forskellige steder i rummet mellem de 2 højtalere.
#
# A:
#    play_signal(sig_1,1,0,forever=True)   # starter lyd fra sig_1 i venstre udgang 
#    play_signal(sig_1,0,1,forever=True)   # starter lyd fra sig_1 i højre udgang (samtidigt med den ovenfor)
#    -> Når højtalerne står ved siden af hinanden bliver lyd tryk væsentlig højere end hvis man kun spiller lyden i een højtaler!
# B:
#    play_signal(sig_1,1,0,forever=True)   # starter lyd fra sig_1 i venstre udgang 
#    play_signal(sig_2,0,1,forever=True)   # starter lyd fra sig_2 i højre udgang (samtidigt med den ovenfor)
#    -> Når højtalerne står ved siden af hinanden bliver lyd tryk væsentlig lavere end hvis man kun spiller lyden i een højtaler!
#       MEN forsvinder ikke helt!
# C:
#    play_signal(sig_1,1,0,forever=True)   # starter lyd fra sig_1 i venstre udgang 
#    play_signal(sig_4,0,1,forever=True)   # starter lyd fra sig_4 i højre udgang (samtidigt med den ovenfor)
#    -> Man oplever stødtoner selvom det er rene lyde fra hver højtaler! Noget andet end stødtonen i Ex. 1
#
# Man opnår her bedst/tydeligst resultat for A/B med de højtalere der kommer med HW delen af Lyd-kit, men det kan også fungere med
# andre højtalere, men vigtigt at kunne flytte med dem.
#
# Det går ikke så godt med hovedtelefoner! Men selv der kan man opleve ex. stødtoner men her er det ikke pga interferens i luften!!!
                                  
from LKlib import *

init_mixer()

sig_1 = generate_sine(440)           
sig_2 = -sig_1
sig_3 = sig_1+sig_2
sig_4 = generate_sine(443)
      
play_signal(sig_1,1,0,forever=True)                  
play_signal(sig_1,0,0,forever=True)                                          