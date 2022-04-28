# LKS3-Ex9-Freq-Modulation.py
#
# Version 1.0 - 21-Okt-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Demo af simpel frekvens modulation.
# Eksperimenter med parameterværdierne. Med de angivne kan man i plot se hvad der sker med signal.
# Med andre kan man mest høre det.

from LKlib import *
from LKSEElib import *

init_mixer()
# Bud på argumenter der lyder 'interessant' Brug evt. https://aatishb.com/synthesine/examples/fm/index.html
#                                          fmf = 1 fmi = 1   - Det samme som ren sinus
#                                          fmf = 1 fmi = 200 - står og svinger 
#                                          fmf = 591 fmi= 1  - 
#                                          fmf = 8 fmi= 200

sound_2 = generate_freq_modulated_sine(400,fmf=8,fmi=200)           

plot_signal(sound_2,time_to_plot=200)
play_signal(sound_2,forever=True)

