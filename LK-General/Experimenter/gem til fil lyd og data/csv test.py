# Demo af at man kan skrive til en kommasepareret fil.
# Det kan bruges til at skive sensor værdier til fil og efterfølgende importere det i excel
# og bruge excels funktioner til at tegne grafer og lave analyse etc..
# testet på PC
#
#

import csv

with open ('mycsv.txt', 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(['col1','col2','col3'])
    write.writerow(['2','1','3'])
    write.writerow(['4','2','6'])
    write.writerow(['8','3','9'])