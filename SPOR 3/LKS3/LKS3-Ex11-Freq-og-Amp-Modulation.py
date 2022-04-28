# LKS3-Ex11-Freq-og-Amp-Modulation.py
#
# Version 1.0 - 21-Okt-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Demo af amplitude modulation af et frekvens moduleret signal.
# Eksperimenter med parameterværdierne. Med de angivne kan man i plot se hvad der sker med signal.
# Med andre kan man mest høre det.
#
from LKlib import *
from LKSEElib import *

init_mixer()

sig = generate_amp_modulated_fmsine(440,amf=8,ami=0.2,fmi=10)
plot_signal(sig,time_to_plot=1000)
play_signal(sig)

time.sleep(2)

sig = exp_decay(generate_amp_modulated_fmsine(440,amf=8,ami=0.2,fmi=10),-4)
plot_signal(sig,time_to_plot=1000)
play_signal(sig,forever=True)
