# Udlæsnig af magnetometer værdier
from microbit import *

# I dokumentatin står der at værdi som returneres er i nano tesla, men hvilke værdier kommer der?
# Minimum og maximum?
# Prøv med magnet tæt på/langt fra sensoren, og se hvad der kommer tilbage.

while True:
    x = compass.get_field_strength()
    print(x)
    sleep(100)