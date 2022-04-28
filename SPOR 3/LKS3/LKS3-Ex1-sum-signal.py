# LKS3-Ex1-sum-signal.py
#
# Program der viser og afspiller summering af signaler. 
#
# Version 2.0 - 21-okt-2021 - Justeret til frigivelse
# Version 1.0 - 25-Nov-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Til at vise hvad der sker når tingene foregår i selve signal til sammenligning med Ex2 hvor det foregår i mediet (luften).
#
#
from LKlib import *
from LKSEElib import *

F1 = 440   # 440Hz giver kammertonen
F2 = 443   # Vælg en frekvens der er nogle få HZ større eller mindre end F1

init_mixer()

sig_1 = generate_sine(F1)           
sig_2 = -sig_1
sig_3 = sig_1+sig_2
sig_4 = generate_sine(F2)
sig_5 = sig_1+sig_4

plot1=plot_signal(sig_1)
plot1.add_freq_title(F1)
play_signal(sig_1)

plot1.update(sig_2)
plot1.add_title("Negeret signal - lyder ens")
play_signal(sig_2)

plot1.update(sig_3)
plot1.add_title("De 2 signaler lagt sammen udligner hinanden -> ingen lyd")
play_signal(sig_3)

plot2=plot_signal(sig_5,time_to_plot=1000)
plot2.add_title("Næsten ens signaler lagt sammen giver stødtoner i selve signalet")
play_signal(sig_5,forever=True)

