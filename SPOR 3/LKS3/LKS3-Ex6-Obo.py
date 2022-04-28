# LKS3-Ex6-Obo.py
#
# Version 2,1 - 07-Dec-2021 - Mgl o6 i sum rettet.
# Version 2.0 - 21-okt-2021 - Justeret til frigivelse
# Version 1.0 - 25-Nov-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# En serie af signaler der forsøger at emulere lyden af en Obo der spiller kammertonen (440Hz)
#
# Hvad mangler der for at det lyder som en Obo?
#
from LKlib import *

init_mixer()
# ------------------------------------------------------------------------------------------------------------------------------
#
#         

bf = 440          
ba = 32000        

f1  = generate_sine(bf,ba*0.1122)      # fundamental

o2  = generate_sine(2*bf,0.3890*ba)    # n'th overtone med n*(fundamental frekvens) og forholdstal til amplitude som set i måling på Obo 
o3  = generate_sine(3*bf,0.0316*ba)    
o4  = generate_sine(4*bf,0.0398*ba)
o5  = generate_sine(5*bf,0.0354*ba)
o6  = generate_sine(6*bf,0.0298*ba)
o7  = generate_sine(7*bf,0.0119*ba)

s1 = f1+o2+o3+o4+o5+o6+o7

play_signal(s1,forever=True)

# Hvad mangler der for at det lyder som en rigtig Obo?