# LKS3-Ex7-FormEnvelope.py
#
# Version 1.0 - 21-Okt-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Demo af en overordnet form på det samlede signal - Envelope (ADSR) eller bare Decay.
#
from LKlib import *
from LKSEElib import *

init_mixer()

sig = generate_sine(440)

plot_signal(sig,time_to_plot=1000)
play_signal(sig)

sig1 = env(sig)
plot_signal(sig1,time_to_plot=1000)
play_signal(sig1,forever=False)

sig2 = exp_decay(sig)
plot_signal(sig2,time_to_plot=1000)
play_signal(sig2,forever=False)