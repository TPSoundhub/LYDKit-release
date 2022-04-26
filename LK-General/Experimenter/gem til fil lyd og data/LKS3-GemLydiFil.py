# LKS3-GemLydiFil.py
# 26JAN2022
#
from LKlib import *
import wave         # importer basis bibliotek til at læse/skrive wav filer - Der er andre Ex Scipy

init_mixer()

sig = exp_decay(generate_amp_modulated_fmsine(440,amf=8,ami=0.2,fmi=10),-4)
play_signal(sig)
#
# Nedenstående gemmer signal som en wav fil - kunne/burde laves til en funktion som blev tilføjet i LKlib
# som man kunne kalde write_signal(sig).
#
fil = wave.open('eksempel.wav','w')
fil.setnchannels(1)                 # Da genereret signal er i mono - det laves om til stereo i play_signal
fil.setsampwidth(2)                 # Hver værdi skal fylde 2 bytes - passer med de 16 bit signal laves i.
fil.setframerate(SAMPLERATE)        # Den sample rate der benyttes til at generere signal - konstant i LKlib
fil.writeframes(sig)                # Skriv signalet som frames til fil.
fil.close()                         # Luk filen så den kan læses af andet program ex. audacity eller en medie player..