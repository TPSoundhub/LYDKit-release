# Lyd fra mic m souddevice biblioteket.
# Fra :
# https://python-sounddevice.readthedocs.io/en/0.4.4/usage.html
# https://python-sounddevice.readthedocs.io/en/0.4.4/api/module-defaults.html#sounddevice.default.dtype
# Brug evt. sd.query_devices() bare i shell/på kommando linien for at se de devices som er tilgængelige
# https://python-sounddevice.readthedocs.io/en/0.4.4/api/checking-hardware.html#sounddevice.query_devices
#
# Virker fint på PC, men ..
#
# Der er et problem med sounddevice på PI via Thonny - mangler PortAudio bibliotek når man forsøger at
# installere sounddevice via tools>manage packages i Thonny.. Også selvom pyaudio er installeret!!
# Også selvom man kommer lidt længere med en "sudo apt-get install python3-pyaudio" ...
# Så der skal mere til for at bruge det/integrere det i LKlib (som skal fungere cross platform)
#

from LKlib import *           # kun for at teste om play_sound kan afspille det optagne
from LKSEElib import *        # kun for at teste om play_sound kan afspille det optagne
import sounddevice as sd  

init_mixer()              # kun for at teste om play_sound kan afspille det optagne

print(sd.query_devices())
print("sd.default.device = i,o nedenfor i koden skal have i værdi som matcher input device - en mikrofon i listen ovenfor!!")

sd.default.samplerate = SAMPLERATE
sd.default.channels = 1     # ser ud til at virke med både 1 og 2 (når device har 2 !!) SKAL kun være en aht plot ellers...
sd.default.dtype = 'int16'  # for at kunne bruge play_sound() dvs. pygame sd.play() default er elles 'float32' som sd kan håndtere
sd.default.device = 1,3     # SKAL BRUGE NUMMERET FOR REALTEK INPUT find med sd.query_devices()
sound = sd.rec(int(DURATION*SAMPLERATE))
sd.wait()


p1=plot_signal(sound,amp_max=32000,time_to_plot=1000)


#
# En løkke der står og optager lyd i DURATION (1) sek og putter det i et np.array hvorefter max værdi udskrives
# Vil med stor værdi altså vise en 'spike' i lyd - Der er så andre funtioner i numpy der kan bruges til at vurdere på
# støjen midlet etc ...
#
while True:
    sound = sd.rec(int(DURATION*SAMPLERATE))
    sd.wait()
    p1.clear_curve()
    p1.update(sound)
    print("Max: ",np.max(sound), "Gennemsnit: ",np.average(sound),"Middelværdi: ",np.mean(sound))
    
# Mere om Numpy funktionerne:
# https://numpy.org/doc/stable/reference/routines.statistics.html
# Der skal vist lidt mere til for at de kan bruges :-)
    
# Sammen med pianoputer kan det kombineres til en hvor man optager en lyd (kort) og så laver det om til forskellige pitches.
# så kan man lave en 'BOX' oplevelse uden at skulle omkring Sundfonts etc....