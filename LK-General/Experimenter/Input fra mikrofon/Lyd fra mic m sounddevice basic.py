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
import sounddevice as sd  

init_mixer()              # kun for at teste om play_sound kan afspille det optagne

print(sd.query_devices())

sd.default.samplerate = SAMPLERATE
sd.default.channels = 2     # ser ud til at virke med både 1 og 2 (når device har 2 !!)
sd.default.dtype = 'int16'  # for at kunne bruge play_sound() dvs. pygame sd.play() default er elles 'float32' som sd kan håndtere
sd.default.device = 3,5     # SKAL BRUGE NUMMERET FOR REALTEK INPUT find med sd.query_devices()
sound = sd.rec(int(DURATION*SAMPLERATE))
sd.wait()

sd.play(sound)
sd.wait()
play_sound(sound) # Blot for at vise at funktionen fra LKlib (pygame baseret) fungerer med lyd optaget med sd.rec


