# LKS1Mb-Krypt-Sender.py
# Ved hjælp af et dictionary kan man lave en simpel kryptering ved
# at udskifte tegn med andre tegn lagt ud i dictionary.
# Læser input fra shell og sender krypteret besked på valgt kanal - En gang!
# OBS - importerer IKKE microbit modul, da det giver memory fejl på V1 af MicroBitten. OK på V2!
import radio

radio.on()
radio.config(channel=10,length=83) # Brug kanalnummer der er udleveret/aftalt
                                   # Length sat op til 83 for at kunne håndtere en tekst på op til 80 tegn plus afslutning
cipher = {
# Tegn (nøgle - key) mappet til encodingsværdi (value) - Man kan lave koden om ved at udskifte value
# SKAL være:
#  - Ens i både sender og modtager for at kunne dekryptere.
#  - Entydige (kun indgå een gang) både som key og som value (da den inverse bruger value som key)
#    til at lave det modsatte opslag.
   'a':'c','b':'d','c':'e','d':'f','e':'g','f':'h','g':'i','h':'j','i':'k','j':'l','k':'m','l':'n','m':'o',
   'n':'p','o':'q','p':'r','q':'s','r':'t','s':'u','t':'v','u':'w','v':'x','w':'y','x':'z','y':'a','z':'b',
   '0':'2','1':'3','2':'4','3':'5','4':'6','5':'7','6':'8','7':'9','8':'0','9':'1',
   ' ':' '
}

inp_tekst = input("Input tekst til encodning(a til z små og ikke øæå) Max 80 tegn: ")
print("Input tekst: ",inp_tekst)

# Encodning (Krytptering) af input tekst/streng ved at udskifte alle tegn een for een vha opslag i cipher
enc_tekst = ""
for i in range(0,len(inp_tekst)):
    if inp_tekst[i] in cipher.keys(): enc_tekst=enc_tekst+cipher[inp_tekst[i]]    # udelader tegn der ikke er med i dictionary
radio.send(enc_tekst)
print("Sendt tekst: ",enc_tekst)