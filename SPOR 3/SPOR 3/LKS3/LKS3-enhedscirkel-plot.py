# LKS3-enhedscirkel-plot.py
#
# Program til at plotte enhedscirkel og sin/cos i tid. Til grundlæggende 'åben bog' forklaring omkring generering af signaler.
#
# Version 2.0 - 21-okt-2021 både med radianer og tid i x-aksen
# Version 1.0 - 25-Nov-2020 - Knud Funch, Soundhub danmark - LYDKit til undervisningsbrug - Region MidtJylland
#
# Først med radianer i x-aksen, så med tid, så snak frekvens (antag tid i x svarer til 1 sek.) ændring i frekvens
# ændring i antal datapunkter for at kunne få tegnet kurven -> snak om interpolation -> D/A konvertering etc .. digital lyd ..
# sampling rate (Nyquist), .. Amplitude lydkort 'opløsning' ..
#

import numpy as np
import matplotlib.pyplot as plt

RAD_IN_X = True                            # False medfører tid i x fremfor radianer 

R = 1  # Radius, som jo så altid er 1 i enhedscirklen           -> Amplituden
F = 1  # Antal gange rundt                                      -> Frekvens hvis indenfor en tidsenhed der svarer til 1sek.
N = 30 # Antal datapunkter indenfor een rundgang/ een tidsblok (sample frekvens)
T = 1  # Slutpunkt i x-aksen (tid)                              -> Tid i sekunder 

if RAD_IN_X:                                # Vinkel i radianer i x-aksen
    t = np.linspace(0,F*2*np.pi,(F*N),endpoint=False)  # Værdier fra 0 til F gange rundt i enhedscirkel med (F*N) datapunkter (sampels) jævn fordelt
    cosinus = R*np.cos(t)                              # Cos på alle datapunkter på een gang - Har vinklen i radianer som værdi i t  (indeholder F*2PI) 
    sinus   = R*np.sin(t)                              # Sin på alle datapunkter på een gang
else:                                       # Tid i x aksen             
    t = np.arange(0,T,1/N)                             # T stk 'tidsblokke' fra 0 til T med N datapunkter (samples) per tidsblok (samle frekvens)
    cosinus = R*np.cos(F*2*np.pi*t)                    # Cos på alle datapunkter på een gang - Har tid i forhold til T som værdi i t
    sinus   = R*np.sin(F*2*np.pi*t)                    # Sin på alle datapunkter på een gang

#
# plot cirklen  x = cosinus, y = sinus
#
plt.subplot(211)
plt.axis("equal")
plt.grid()
plt.plot(cosinus,sinus)
plt.plot(cosinus,sinus,"+b")
#
# Plot sin og cos i forhold til vinkel i radianer eller til tid (T i sekunder) - Bemærk første/sidste værdi (ikke dobbelt op)
# Når 
#
plt.subplot(212)
if RAD_IN_X:
    plt.xlabel("x = Vinkel i radianer")            # Når vi har brugt linspace med F*2*np.sin - Altså med vinklen i radianer i tabel
else:
    plt.xlabel("x = værdier mellem 0 og "+str(T))  # Når vi har brugt arrange med 0,T         - Altså med tid relativt til T i tabel
plt.ylabel("sin(x) i rød,cos(x) i blå")
plt.grid()
plt.plot(t,sinus,"+r")
plt.plot(t,cosinus,"+b")
plt.show()                   
                                       
                     

