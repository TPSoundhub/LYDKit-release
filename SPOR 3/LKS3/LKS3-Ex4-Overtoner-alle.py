# LKS3-Ex4-Overtoner-alle.py
#
# Version 2.0 - 21-okt-2021 - Justeret til frigivelse
# Version 1.0 - 25-Nov-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Opbyging af en serie af alle overtoner summeret med den fundamentale frekvens.
# Kan bruges ifm snak om bølger i åbne rør, og om Fourier serier. Se ex:
# https://www.youtube.com/watch?v=YUBe-ro89I4
#
from LKlib import *
from LKSEElib import *

init_mixer()

bf = 440        
ba = 8000

f1  = generate_sine(bf,ba)          # fundamental frekvens

o2  = generate_sine(2*bf,1/2*ba)    # n'th overtone med n*(fundamental frekvens) og 1/n * (fundamental amplitude) 
o3  = generate_sine(3*bf,1/3*ba)      
o4  = generate_sine(4*bf,1/4*ba)
o5  = generate_sine(5*bf,1/5*ba)
o6  = generate_sine(6*bf,1/6*ba)
o7  = generate_sine(7*bf,1/7*ba)
o8  = generate_sine(8*bf,1/8*ba)
o9  = generate_sine(9*bf,1/9*ba)
o10 = generate_sine(10*bf,1/10*ba)
o11 = generate_sine(11*bf,1/11*ba)
o12 = generate_sine(12*bf,1/12*ba)
o13 = generate_sine(13*bf,1/13*ba)
o15 = generate_sine(15*bf,1/15*ba)

all_overtones = [o2,o3,o4,o5,o6,o7,o8,o9,o10,o11,o12,o13]  # Saw

#
# Adder alle overtoner (lige og ulige) til den fundamentale
# Se og hør at der opbygges et sav takket signal - se fourier serie video eksempel
#

sig = f1
plot_all = plot_signal(sig)
plot_all.add_title("Fundamental")
play_signal(sig)

ot = 2

for i in all_overtones:
    plot_all.clear_curve()
    sig=sig+i
    plot_all.add_title("Fundamental plus alle overtoner til og med: "+str(ot))
    plot_all.update(sig)
    play_signal(sig)    
    ot=ot+1   
