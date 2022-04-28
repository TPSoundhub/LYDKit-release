# LKS3-Ex10-Amplitude-Modulation.py
#
# Version 1.0 - 21-Okt-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Demo af simpel amplitude modulation.
# Eksperimenter med parameterværdierne. Med de angivne kan man i plot se hvad der sker med signal.
# Med andre kan man mest høre det.

from LKlib import *
from LKSEElib import *

init_mixer()

sound_1 = generate_amp_modulated_sine(440,amf=3,ami=0.5)           

plot_signal(sound_1,time_to_plot=1000)
play_signal(sound_1,forever=True)

