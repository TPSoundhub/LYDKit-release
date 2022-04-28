# LKS3-Ex5-Overtoner.py
#
# Version 2.0 - 21-okt-2021 - Justeret til frigivelse
# Version 1.0 - 25-Nov-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Afspiller både en med alle og en med kun de ulige overtoner så de kan sammenlignes
#
from LKlib import *
from LKSEElib import *

init_mixer()
        

bf = 440        
ba = 8000

f1  = generate_sine(bf,ba)          # fundamental

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

addall = f1+o2+o3+o4+o5+o6+o7+o8+o9+o10+o11+o12+o13  # saw
addodd = f1+o3+o5+o7+o9+o11+o13                      # square

plot=plot_signal(addall)
plot.add_title("Alle overtoner -> saw")
play_signal(addall)

plot.clear_curve()
plot.update(addodd)
plot.add_title("Ulige overtoner -> square")
play_signal(addodd)
