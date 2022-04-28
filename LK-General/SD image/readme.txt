Seneste version

Ikke tilgængelig på GItHUb eller USB stick. Kun via adgang til ERFA tams kanalen på Struer Statsgymnasium.
Der er alt materialet samt mulighed for dialog med andre der benytter LYD-kit.
For at få adgang kan man kontakte Jesper Nørgaard Andersen på jna@stgym.dk fra Struer Statsskole
eller Knud Funch på via tp@soundhub.dk

LK02MAR2022.img

Spor 1 filer til microbit er tilføjet så man også har dem på PI.

Desuden er der lagt nogle flere eksempler på Sonic-PI - Bl.a eksempel med Drumbeat som kan styres over OSC

Spor 4 eksempel med scamp både med keyboard og MicroBit som input. 
Keyboard version tilføjet for at kunne komme hurtigt igang den vej uden brug af Micro:Bit.
Keyboard version har en pitch bend feature som MB versionen ikke har. Lagt på pil op/ned.
MicroBit version har fået tydeliggjort at man kan bruge andre sensor typer 
(potentiometer,magnetometer, accelerometer,lyssensor) til at generere midi noder - En anden oplevelse end 'knapper'.


Tidligere version
LK07JAN2022.img

Et disk image af et SD kort med Raspberry OS, og det SW som hører til Lyd-Kit. 
Det kan køre umiddelbart på en Raspberry PI 3 eller 4 med et IQaudio-DAC+ forstærker HAT monteret.

Downloader man det kan man brænde et SD kort (16GB), som så vil fungere sammen med PI og have SW til 
Spor2, 3 og 4 liggende klar.

(Hvis man ikke ønsker at alle filer ligger klar kan man fjerne dem, og istedet for give eleverne dem drypvis) 

Man kan eksempelvis brænde SD kort med Balena Etcher som man finder på:
https://www.balena.io/etcher/

Ekstra info: 

Filen: /etc/rc.loal er forberedt til at man let kan få ex. Case3 (Quiz) eksemplet til at køre headless.

Filen: /Boot/config.txt er sat op til at bruge IQaudio HAT, men indeholder også information om hvordan man kan:
- Bruge alternative forstærkler moduler
- Få PI til at virke sådan at man kan skifte mellem headphone, HDMI og IQaudio 
  (Kan bruges til at køre med PI uden IQaudio forstærker monteret) 


  