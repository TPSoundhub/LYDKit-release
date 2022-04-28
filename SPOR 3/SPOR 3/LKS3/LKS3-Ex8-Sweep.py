# LKS3-Ex8-Sweep.py
#
# Version 2.0 - 21-Okt-2021 - Justeret til LKlib, og med 2 udgaver samlet.
# Version 1.0 - 21-Okt-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Opbygning af et simpelt frekvens sweep på 2 forskellige måder. Stepvis med nye signaler med ny frekvens eller som eet signal
#
from LKlib import *
from LKSEElib import *

init_mixer()
#---------------------------------------------------------------------------------------------------------------------------
#  Build and play back sounds by simple modification of the below. Listen, measure, experiment and reflect..
#
# super simpel sweep med de givne funktioner - her med plot
# Ikke brugbar da der er ticks i lyden og lydkort/basis funktion kan ikke følge med så derfor skal sweep laves på anden måde. 

first_round = True
for freq in range (400,3000,50):    # sidste parameter giver step størrelsen i frekvens
    sig = generate_sine(freq)
    ch = play_signal(sig,forever=True)
    if first_round:
        p1 = plot_signal(sig)
        p1.add_freq_title(freq)
        first_round= False
    else:
        p1.update(sig)
        p1.add_freq_title(freq)
    p1.clear_curve()
    stop_sound(ch)

# Alternativ - Kik ind i LKlib for hvordan
#
sig = generate_sweep_by_power(duration=6,power=2)           
plot_signal(sig,time_to_plot=500,duration=6)
play_signal(sig)
