# LKS1Mb-DigServo-Modtager.py
# Modtager en key fra LKS1Mb-3Key-Sender.py og sætter servo motor på PIN0 i en
# position der matcher key. Hvis key = "0" eller sender slukkes returneres til
# center position (med 360 servo - stoppes motor)
#
from microbit import pin0,display,sleep
import radio

display.show("DSM")      # Udskriver på MB display for at identificere funktion
                         # som 'Digital Servo Modtager' når MB kører med batteri (svært at se ellers).
radio.on()
radio.config(channel=44) # Brug kanalnummer der er udleveret/aftalt (0-83)

nof_nones = 0

center_pulse_val = 77   # svarer til 1500 microsek ved periode på 20 msek.
min_pulse_val    = 30   # svarer til 500 microsek  - ret hvis anden spec.!
max_pulse_val    = 122  # svarer til 2500 microsek - ret hvis anden spec.!
min_vinkel       = 0    
max_vinkel       = 180  # ret hvis anden spec.!

# Dictionary med key som nøgle (til opslag) - Key som tegn derfor i ""
# og servo vinkel som det man får retur     - Vinkel som tal derfor ikke i ""
key_til_vinkel = { # key:  Vinkel:
                    "0":   90,   # Bemærk center position ved 120 graders motor er 60 og IKKE 90!
                    "1":  180,     
                    "2":   70,       
                    "4":   40     
    }

# Funktion der tager værdier i en range og laver om til en anden range
# Svarer til arduino c's map() funktion! MEN i python er map() noget andet - se dokumentation
# Derfor kalder vi den her for convert_range
#
def convert_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

vinkel_0    = int((max_vinkel-min_vinkel)/2)  # Svarer til center position og stopped med 360 graders servo.
ny_vinkel_0 = vinkel_0
pin0.set_analog_period(20)

while True:
    key_str = radio.receive()
    if key_str:                      # noget modtaget
        nof_nones = 0
        print(key_str)               # som testudskrift i shell når koblet til PC/MAC
        if key_str in key_til_vinkel: ny_vinkel_0 = key_til_vinkel[key_str]
    else: nof_nones = nof_nones+1
    if nof_nones > 20 :              # sender er slukket eller udenfor rækkevidde. Sæt motor i center!
        ny_vinkel_0 = int((max_vinkel-min_vinkel)/2)         
        nof_nones = 0
    if (vinkel_0 != ny_vinkel_0):    # Behøver kun at sætte værdi ved ændring. PWM kører i baggrund.
        pulse_val = convert_range(ny_vinkel_0,min_vinkel,max_vinkel,min_pulse_val,max_pulse_val)
        print("pulse_val",pulse_val) # test udskrift
        pin0.write_analog(pulse_val)  # sender PWM til servo
        vinkel_0 = ny_vinkel_0
    sleep(50)