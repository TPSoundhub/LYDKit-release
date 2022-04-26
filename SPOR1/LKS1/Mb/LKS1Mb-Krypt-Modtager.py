# LKS1Mb-Krypt-Modtager.py
# Står og lytter efter beskeder på bestemt kanal og decoding modtaget besked og udskriver den i shell
# Decryptering ved hjælp af det inverse (omvendte) disctionary fra value til key i forhold til oprindeligt.
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

# Det omvendte distionary til dekryptering (value bliver til key og key til value for alle elemeter (items)
invers_cipher = dict((v, k) for k, v in cipher.items())

while True:
    enc_tekst = radio.receive()
    if enc_tekst != None:       # Der modtages noget forskelligt fra None. altså en besked på kanalen!
        # Decodning ved udskiftning af tegn i det omvendte distionary
        dec_tekst = ""
        for i in range(0,len(enc_tekst)):   # For alle tegn i teksten 
            dec_tekst=dec_tekst+invers_cipher[enc_tekst[i]]
        print("Modtaget: ",enc_tekst)
        print("Decodet: ", dec_tekst)