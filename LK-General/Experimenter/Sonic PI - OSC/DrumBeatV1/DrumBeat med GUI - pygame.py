from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import pygame as pg
from pygame.locals import *

def blit_sub_beat():
    sub_txt1 = font.render("1              2              3             4",True,black)
    sub_txt2 = font.render("1              2              3             4",True,black)
    sub_txt3 = font.render("1              2              3             4",True,black)
    sub_txt4 = font.render("1              2              3             4",True,black)
    
    beat_txt1 = font.render("1",True,black)
    beat_txt2 = font.render("2",True,black)
    beat_txt3 = font.render("3",True,black)
    beat_txt4 = font.render("4",True,black)
    
    
    screen.blit(sub_txt1,(110,195))
    screen.blit(sub_txt2,(110+110*4,195))
    screen.blit(sub_txt3,(110+110*8,195))
    screen.blit(sub_txt4,(110+110*12,195))
    
    screen.blit(beat_txt1,(110,135))
    screen.blit(beat_txt2,(110+110*4,135))
    screen.blit(beat_txt3,(110+110*8,135))
    screen.blit(beat_txt4,(110+110*12,135))

def do_lists():
    for i in status_dict:
        if status_dict[i] == True:
            # kigger på status_dict og kigger efter True values. hvis en True value bliver fundet, bliver key på den value sat ind i status_list
            # (alle keys i status/kords dict er "koordinater" eks 3,8 er række 3 kolonne 8)
            if i not in status_list:
                # hvis key ikke er i status_list bliver den sat i status_list
                status_list.append(i)
                # hvis value bliver ændret til False og key er i status_list bliver key fjernet fra status_list
        if status_dict[i] == False and i in status_list:
            status_list.remove(i)
            
    for b in status_list:
        for h in kords_dict:
            # hvis key er i kords_dict og koordinaten ikke allerede er i kords_list bliver den sat i kords_list
            if b == h and kords_dict[h] not in kords_list:
                kords_list.append(kords_dict[h])
            # hvis koordinat er i kords_list og key ikke i status_list bliver koordinaten fjernet
            if kords_dict[h] in kords_list and h not in status_list:
                kords_list.remove(kords_dict[h])
            
# Skal være enten i while loop eller her pga tempo skal "opdateres", hvis ikke, ændres tempo skriften ikke
# tempo_on bruges til at kunne vise om tempo er 0
def tempo_txt_skift():
    global tempo_txt
    if tempo_on == "0":
        tempo_txt = font.render("Tempo = " + tempo_on,True,black)
    else:
        tempo_txt = font.render("Tempo = " + tempo,True,black)

# de forskællige rækker med rects
row1 = [pg.Rect(75,260,80,80),pg.Rect(75+110,260,80,80),pg.Rect(75+110*2,260,80,80),pg.Rect(75+110*3,260,80,80),pg.Rect(75+110*4,260,80,80),pg.Rect(75+110*5,260,80,80),
        pg.Rect(75+110*6,260,80,80),pg.Rect(75+110*7,260,80,80),pg.Rect(75+110*8,260,80,80),pg.Rect(75+110*9,260,80,80),pg.Rect(75+110*10,260,80,80),pg.Rect(75+110*11,260,80,80),
        pg.Rect(75+110*12,260,80,80),pg.Rect(75+110*13,260,80,80),pg.Rect(75+110*14,260,80,80),pg.Rect(75+110*15,260,80,80)]
row2 = [pg.Rect(75,370,80,80),pg.Rect(75+110,370,80,80),pg.Rect(75+110*2,370,80,80),pg.Rect(75+110*3,370,80,80),pg.Rect(75+110*4,370,80,80),pg.Rect(75+110*5,370,80,80),
        pg.Rect(75+110*6,370,80,80),pg.Rect(75+110*7,370,80,80),pg.Rect(75+110*8,370,80,80),pg.Rect(75+110*9,370,80,80),pg.Rect(75+110*10,370,80,80),pg.Rect(75+110*11,370,80,80),
        pg.Rect(75+110*12,370,80,80),pg.Rect(75+110*13,370,80,80),pg.Rect(75+110*14,370,80,80),pg.Rect(75+110*15,370,80,80)]
row3 = [pg.Rect(75,480,80,80),pg.Rect(75+110,480,80,80),pg.Rect(75+110*2,480,80,80),pg.Rect(75+110*3,480,80,80),pg.Rect(75+110*4,480,80,80),pg.Rect(75+110*5,480,80,80),
        pg.Rect(75+110*6,480,80,80),pg.Rect(75+110*7,480,80,80),pg.Rect(75+110*8,480,80,80),pg.Rect(75+110*9,480,80,80),pg.Rect(75+110*10,480,80,80),pg.Rect(75+110*11,480,80,80),
        pg.Rect(75+110*12,480,80,80),pg.Rect(75+110*13,480,80,80),pg.Rect(75+110*14,480,80,80),pg.Rect(75+110*15,480,80,80)]
row4 = [pg.Rect(75,590,80,80),pg.Rect(75+110,590,80,80),pg.Rect(75+110*2,590,80,80),pg.Rect(75+110*3,590,80,80),pg.Rect(75+110*4,590,80,80),pg.Rect(75+110*5,590,80,80),
        pg.Rect(75+110*6,590,80,80),pg.Rect(75+110*7,590,80,80),pg.Rect(75+110*8,590,80,80),pg.Rect(75+110*9,590,80,80),pg.Rect(75+110*10,590,80,80),pg.Rect(75+110*11,590,80,80),
        pg.Rect(75+110*12,590,80,80),pg.Rect(75+110*13,590,80,80),pg.Rect(75+110*14,590,80,80),pg.Rect(75+110*15,590,80,80)]


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((2200,800))
dark_blue = (20,80,255)
grey = (150,150,150)
black = (0,0,0)
# selector rect bliver brugt til at vise hvilken firkant man er ved
selector = pg.Rect(70,255,90,90)
# selector_pos hjælper med at holde styr på hvor selector er
selector_pos = [70,255]
x = 0
y = 0
on = True
# tempo_on bruges til at kunne vise om tempo er 0
tempo_on = "1"
tempo = "60"

# de forskellige instrumenter der bliver brugt
samples = {"open_sample1" : "drum_cymbal_open",
           "open_sample2" : "drum_cymbal_pedal",
           "closed_sample1" : "drum_cymbal_closed",
           "closed_sample2" : "drum_cymbal_soft",
           "snare_sample1" : "sn_zome",
           "snare_sample2" : "drum_cowbell",
           "kick_sample1" : "drum_heavy_kick",
           "kick_sample2" : "drum_bass_hard"}


music_note = pg.image.load("music_note_use.png")


sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

# laver font
font = pg.font.SysFont("arial",30,True)
# laver surface med tekst
kick_sample_txt = font.render(samples["kick_sample1"],True,black)
snare_sample_txt = font.render(samples["snare_sample1"],True,black)
open_sample_txt = font.render(samples["open_sample1"],True,black)
closed_sample_txt = font.render(samples["closed_sample1"],True,black)

# hvis en value bliver true vil der blive vist en musik node og musikken ændres
status_list = []
status_dict = {(0,0):False,(0,1):False,(0,2):False,(0,3):False,(0,4):False,(0,5):False,(0,6):False,(0,7):False,(0,8):False,(0,9):False,(0,10):False,(0,11):False,
              (0,12):False,(0,13):False,(0,14):True,(0,15):False,
               
              (1,0):True,(1,1):True,(1,2):True,(1,3):True,(1,4):True,(1,5):True,(1,6):True,(1,7):True,(1,8):True,(1,9):True,(1,10):True,(1,11):True,
              (1,12):True,(1,13):True,(1,14):False,(1,15):False,
               
              (2,0):False,(2,1):False,(2,2):False,(2,3):False,(2,4):True,(2,5):False,(2,6):False,(2,7):False,(2,8):False,(2,9):False,(2,10):False,(2,11):False,
              (2,12):True,(2,13):False,(2,14):False,(2,15):False,
               
              (3,0):True,(3,1):True,(3,2):False,(3,3):False,(3,4):False,(3,5):False,(3,6):True,(3,7):False,(3,8):True,(3,9):True,(3,10):False,(3,11):True,
              (3,12):False,(3,13):False,(3,14):False,(3,15):False}

# her er koordinater der bruges til at vise musik noden det rigtige sted
kords_list = []
kords_dict = {(0,0):(75,260),(0,1):(75+110,260),(0,2):(75+110*2,260),(0,3):(75+110*3,260),(0,4):(75+110*4,260),(0,5):(75+110*5,260),(0,6):(75+110*6,260),
             (0,7):(75+110*7,260),(0,8):(75+110*8,260),(0,9):(75+110*9,260),(0,10):(75+110*10,260),(0,11):(75+110*11,260),(0,12):(75+110*12,260),
             (0,13):(75+110*13,260),(0,14):(75+110*14,260),(0,15):(75+110*15,260),
              
             (1,0):(75,370),(1,1):(75+110,370),(1,2):(75+110*2,370),(1,3):(75+110*3,370),(1,4):(75+110*4,370),(1,5):(75+110*5,370),(1,6):(75+110*6,370),
             (1,7):(75+110*7,370),(1,8):(75+110*8,370),(1,9):(75+110*9,370),(1,10):(75+110*10,370),(1,11):(75+110*11,370),(1,12):(75+110*12,370),
             (1,13):(75+110*13,370),(1,14):(75+110*14,370),(1,15):(75+110*15,370),
              
             (2,0):(75,480),(2,1):(75+110,480),(2,2):(75+110*2,480),(2,3):(75+110*3,480),(2,4):(75+110*4,480),(2,5):(75+110*5,480),(2,6):(75+110*6,480),
             (2,7):(75+110*7,480),(2,8):(75+110*8,480),(2,9):(75+110*9,480),(2,10):(75+110*10,480),(2,11):(75+110*11,480),(2,12):(75+110*12,480),
             (2,13):(75+110*13,480),(2,14):(75+110*14,480),(2,15):(75+110*15,480),
              
             (3,0):(75,590),(3,1):(75+110,590),(3,2):(75+110*2,590),(3,3):(75+110*3,590),(3,4):(75+110*4,590),(3,5):(75+110*5,590),(3,6):(75+110*6,590),
             (3,7):(75+110*7,590),(3,8):(75+110*8,590),(3,9):(75+110*9,590),(3,10):(75+110*10,590),(3,11):(75+110*11,590),(3,12):(75+110*12,590),
             (3,13):(75+110*13,590),(3,14):(75+110*14,590),(3,15):(75+110*15,590)}

# de her list bliver ændret i forhold til status_dict og bliver sendt til sonic pi for at ændre musikken
beat0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
beat1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
beat2 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
beat3 = [1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0]

do_lists()
tempo_txt_skift()

running = True
while running:
    # x og y er omvendt på grund af dictionaries ovenover, der står det som y,x - Jeg opdagede det for sent og gider ikke at skrive det om
    grid_pos = (y,x)
    clock.tick(60)
    
    event = pg.event.wait()
    
    if event.type == pg.QUIT: running = False
    else:
        if event.type in (pg.KEYDOWN, pg.KEYUP):
            key = pg.key.name(event.key)
            print(key)
            if event.key == pg.K_ESCAPE: running = False
            if (event.type == pg.KEYDOWN):
                # tast 1-6 ændrer tempo og viser i vinduet hvilket tempo der spilles på
                if key == "6":
                    sender.send_message('/trigger/drumbeat_control',["tempo",180])
                    tempo = "180"
                    tempo_txt_skift()
                if key == "5":
                    sender.send_message('/trigger/drumbeat_control',["tempo",150])
                    tempo = "150"
                    tempo_txt_skift()
                if key == "4":
                    sender.send_message('/trigger/drumbeat_control',["tempo",120])
                    tempo = "120"
                    tempo_txt_skift()
                if key == "3":
                    sender.send_message('/trigger/drumbeat_control',["tempo",90])
                    tempo = "90"
                    tempo_txt_skift()
                if key == "2":
                    sender.send_message('/trigger/drumbeat_control',["tempo",60])
                    tempo = "60"
                    tempo_txt_skift()
                if key == "1":
                    sender.send_message('/trigger/drumbeat_control',["tempo",30])
                    tempo = "30"
                    tempo_txt_skift()
                # spacebar slår musikken til og fra
                if key == "space":
                    if on == True:
                        on = False
                        sender.send_message('/trigger/drumbeat_control',["on_off",0])
                        tempo_on = "0"
                        tempo_txt_skift()
                    elif on == False:
                        on = True
                        sender.send_message('/trigger/drumbeat_control',["on_off",1])
                        tempo_on = "1"
                        tempo_txt_skift()
                        
                # a,s,d,f,g,h,j,k ændrer instrumenter
                if key == "a":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["open", "drum_cymbal_open"])
                    open_sample_txt = font.render(samples["open_sample1"],True,black)
                if key == "s":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["open", "drum_cymbal_pedal"])
                    open_sample_txt = font.render(samples["open_sample2"],True,black)
                # -------------
                if key == "d":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["closed", "drum_cymbal_closed"])
                    closed_sample_txt = font.render(samples["closed_sample1"],True,black)
                if key == "f":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["closed", "drum_cymbal_soft"])
                    closed_sample_txt = font.render(samples["closed_sample2"],True,black)
                # -------------
                if key == "g":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["snare", "sn_zome"])
                    snare_sample_txt = font.render(samples["snare_sample1"],True,black)
                if key == "h":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["snare", "drum_cowbell"])
                    snare_sample_txt = font.render(samples["snare_sample2"],True,black)
                # -------------
                if key == "j":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["kick", "drum_heavy_kick"])
                    kick_sample_txt = font.render(samples["kick_sample1"],True,black)
                if key == "k":
                    sender.send_message('/trigger/drumbeat_set_sample',  ["kick", "drum_bass_hard"])
                    kick_sample_txt = font.render(samples["kick_sample2"],True,black)
                # -------------
                # return/enter ændrer i status_dict og sender den rigtige list til sonic pi
                if key == "return":
                    if status_dict[grid_pos] == True:
                        status_dict[grid_pos] = False
                        do_lists()
                        
                        if grid_pos[0] == 0:
                            beat0[grid_pos[1]] = 0
                            sender.send_message('/trigger/drumbeat_patern_open', beat0)
                        if grid_pos[0] == 1:
                            beat1[grid_pos[1]] = 0
                            sender.send_message('/trigger/drumbeat_patern_closed', beat1)
                        if grid_pos[0] == 2:
                            beat2[grid_pos[1]] = 0
                            sender.send_message('/trigger/drumbeat_patern_snare', beat2)
                        if grid_pos[0] == 3:
                            beat3[grid_pos[1]] = 0
                        sender.send_message('/trigger/drumbeat_patern_kick', beat3)
                            
                    elif status_dict[grid_pos] == False:
                        status_dict[grid_pos] = True
                        do_lists()
                        
                        if grid_pos[0] == 0:
                            beat0[grid_pos[1]] = 1
                            sender.send_message('/trigger/drumbeat_patern_open', beat0) 
                        if grid_pos[0] == 1:
                            beat1[grid_pos[1]] = 1
                            sender.send_message('/trigger/drumbeat_patern_closed', beat1)
                        if grid_pos[0] == 2:
                            beat2[grid_pos[1]] = 1
                            sender.send_message('/trigger/drumbeat_patern_snare', beat2)
                        if grid_pos[0] == 3:
                            beat3[grid_pos[1]] = 1
                            sender.send_message('/trigger/drumbeat_patern_kick', beat3)
                # piletasterne bevæger selector rect
                if key == "left":
                    if selector.left <= 70:
                        selector.update(1720,selector_pos[1],90,90)
                        selector_pos[0] = 1720
                        x = 15
                    else:
                        selector.move_ip(-110,0)
                        selector_pos[0] += -110
                        x += -1
                if key == "right":
                    if selector.right >= 1720:
                        selector.update(70,selector_pos[1],90,90)
                        selector_pos[0] = 70
                        x = 0
                    else:
                        selector.move_ip(110,0)
                        selector_pos[0] += 110
                        x += 1
                if key == "down":
                    if selector.bottom >= 590:
                        selector.update(selector_pos[0],255,90,90)
                        selector_pos[1] = 255
                        y = 0
                    else:
                        selector.move_ip(0,110)
                        selector_pos[1] += 110
                        y += 1
                if key == "up":
                    if selector.top <= 255:
                        selector.update(selector_pos[0],585,90,90)
                        selector_pos[1] = 585
                        y = 3
                    else:
                        selector.move_ip(0,-110)
                        selector_pos[1] += -110
                        y += -1
                        
    
    screen.fill(grey)
    
    # tegner selector på skærmen
    pg.draw.rect(screen,black,selector,width=17,border_radius=1)
    # tegner alle rects i lists
    for pos in row1:
        pg.draw.rect(screen,dark_blue,pos)
    for pos in row2:
        pg.draw.rect(screen,dark_blue,pos)
    for pos in row3:
        pg.draw.rect(screen,dark_blue,pos)
    for pos in row4:
        pg.draw.rect(screen,dark_blue,pos)
    
    # tegner musik node ved alle koordinater i kords_list
    # hvis der ingenting er i status_list vil ingen node laves
    if len(status_list) > 0:
        for p in kords_list:
            screen.blit(music_note,(p))
            
    
    # tegner tekst på vinduet
    screen.blit(open_sample_txt,(1835,265))
    screen.blit(closed_sample_txt,(1835,375))
    screen.blit(snare_sample_txt,(1835,485))
    screen.blit(kick_sample_txt,(1835,595))
    screen.blit(tempo_txt,(1835,155))
    # function der skriver sub og beat på vinduet
    blit_sub_beat()
    
    # tegner alle linier på vinduet
    # linier der indeholder rects, sub og beat
    # (beat er øverste talrække, sub er nederste talrække)
    pg.draw.lines(screen,black,True,((50,125),(1825,125),(1825,690),(50,690)),width=3)
    # linier der indeholder tempo og instrumenter
    pg.draw.lines(screen,black,False,((1825,125),(2150,125),(2150,690),(1825,690)),width=3)
    # linie der skiller første række fra anden række
    pg.draw.line(screen,black,(50,355),(2150,355),width=3)
    # linie der skiller anden række fra tredje række
    pg.draw.line(screen,black,(50,245+220),(2150,245+220),width=3)
    # linie der skiller tredje række fra fjerde række
    pg.draw.line(screen,black,(50,245+330),(2150,245+330),width=3)
    # linie der skiller sub fra første række
    pg.draw.line(screen,black,(50,245),(2150,245),width=3)
    # linie der skiller beat fra sub
    pg.draw.line(screen,black,(50,185),(1825,185),width=3)
    #linier der skiller rects, beat og sub verticalt
    pg.draw.line(screen,black,(62.5+110*4,125),(62.5+110*4,690),width=3)
    pg.draw.line(screen,black,(62.5+110*8,125),(62.5+110*8,690),width=3)
    pg.draw.line(screen,black,(62.5+110*12,125),(62.5+110*12,690),width=3)
    
    pg.display.flip()

pg.quit()