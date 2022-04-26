# "M2SEElib.py"
#
# Plot funktionalitet til at lave simple (overskuelige) programmer med plot som er sammenlignelige med tilsvarende
# HEAR eksempler
#
# Version 0.2 Knud - SHD - 04 dec. 2020 - Simplifisering ud fra første udgave. Kun brug for at plotte en curve. 
#
import matplotlib.pyplot as plt
import time  
import pygame
import numpy as np

#
# Globale konstanter - skal være de samme som i HEAR biblioteket...
#
SAMPLERATE = 44100  # Sampling frequence! samples pr second. Twice the highest freq you want to reproduce as minimum (nyquist)
                    # 44100/48000 is a widely used and match with sound card and pygame sound default settings typically.  
DURATION   = 1.0    # Lenght of tone generated in seconds.

SPEED_OF_SOUND = 343       # m/s i luft ved 20 grader celsius

class plot_signal:     # Full means the full signal in plot eg lenght equals DURATION, If False only 10ms is shown
#
# initialiseringer med hensyn til plot og figur


#
    def __init__(self,signal,time_to_plot=10,amp_max=15000,duration=DURATION):
        plt.ion()                          # sætter plot funktionen til at tegne på skærm direkte så hvert kald får effekt med det samme
                                           # Hvis den ikke er kaldt så laver man tegning/plot i baggrunden og den bliver først vist når man kalder plt.show()
        plt.figure(figsize=[7,3.5])        # Laver plot vindue lidt større end default som er [6.4,4.8]
        self.splot = plt.subplot(111)      # husk plot så kurven kan genfindes - bruges i clear curves og update
        plt.title("\n")                    # for at overskrift skal være synlig når kode kører på PI
        plt.xlabel("Tid - "+str(time_to_plot)+" ms udsnit\nDet der er i plot bevæger sig ca. "+str(SPEED_OF_SOUND*time_to_plot/1000)+" meter i luft ved 20 grader celsius")         
        plt.ylabel("amplitude (int16)")
        plt.axis([0,time_to_plot,-amp_max,amp_max])    # Plot 0-time_to_plot ms og sæt (amplitude) y-aksen til at gå fra - til + MAX_AMP - time_to_plot=10 ms hvis ikke angivet i kald
        plt.tight_layout()
        self.time = np.linspace(0,1000*duration,int(duration*SAMPLERATE))   # alternativ x-akse med tid i millisekunder (ms)     
        self.curve,     = self.splot.plot(self.time,signal)                
            
        #
        # For at få tegnet plot færdigt inden der sker andet i koden skal der ventes lidt 
        #
        plt.pause(0.05)

    def update(self,signal):
        self.curve,     = self.splot.plot(self.time,signal)                
        # For at få tegnet plot færdigt inden der sker andet i koden skal der ventes lidt 
        #
        plt.pause(0.05)

    def add_freq_title(self,freq):   # Only to be used when signal is 'pure' that is with only one freq.
        if freq!=0:
            blv = round(SPEED_OF_SOUND*100/freq,2)
            plt.title("Freq: "+str(freq)+" Hz Bølgelængden: "+"%.2f" % blv+" cm "+"Svingningstid: "+"%.4f" % (1000/freq)+" ms")                
        # For at få tegnet plot færdigt inden der sker andet i koden skal der ventes lidt 
        #     
        plt.pause(0.05)

    def add_title(self,text=" "):   
        plt.title(text)                
        # For at få tegnet plot færdigt inden der sker andet i koden skal der ventes lidt 
        #     
        plt.pause(0.05)

    def clear_curve(self):
        self.splot.lines.remove(self.curve)          
        plt.draw() 