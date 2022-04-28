# Udlæsning af accelerometerværdier i x-aksen.
from microbit import *

while True:
    acc_x,acc_y,acc_z = accelerometer.get_values()
#    acc_all = accelerometer.get_values()          # alternativ - tuple/sæt af værdier
    print(acc_x)                                   
#    print(acc_all[0])                             # alternativ - udpeg i tuple
    sleep(100)