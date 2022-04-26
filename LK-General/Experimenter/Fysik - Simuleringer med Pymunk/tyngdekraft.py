# Tyngdekraft.py
#
# fra: https://www.youtube.com/watch?v=YrNpkuVIFdg
# Faldende æbler
#
import pygame,sys,pymunk

def create_apple(space,pos):
    body = pymunk.Body(1,100,body_type = pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body,68)
    space.add(body,shape)
    return shape

def draw_apples(apples):
    for apple in apples:
        pos_x = int(apple.body.position.x)
        pos_y = int(apple.body.position.y)
#        pygame.draw.circle(screen,(0,0,0),(pos_x,pos_y),80)
        apple_rect = apple_surface.get_rect(center = (pos_x,pos_y))
        screen.blit(apple_surface,apple_rect)
    
def static_ball(space,pos):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body,50)
    space.add(body,shape)
    return shape

def draw_static_ball(balls):
    for ball in balls:
        pos_x = int(ball.body.position.x)
        pos_y = int(ball.body.position.y)
        pygame.draw.circle(screen,(0,0,0),(pos_x,pos_y),50)

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

# definer et 'space' og sæt tyngdekraft
space = pymunk.Space()
space.gravity = (0,500)

apples = []


balls  = []
balls.append(static_ball(space,(500,500)))
balls.append(static_ball(space,(250,600)))

# billede til æblet, så det bliver til andet end en sort fyldt cirkel - kombineret med at draw-apple funktionen
# ændres fra draw circle til de efterfølgende linier apple_rect.... og screen.blit...
# billede i samme direktorie som programmet og billedet hentet fra https://www.iconsdb.com/red-icons/apple-icon.html
# I den størrelse som hedder 128 i dette tilfælde!!

apple_surface = pygame.image.load("apple_red.png")

# Modificeret ift youtube video så den tager højde for ESC og en pænere exit, svarende til
# det vi gør ifm keyboard input til piano
#
run = True
while run:
    # Tøm event kø og lav passende handlinger for indkomne events
    for event in pygame.event.get():
        if (event.type == pygame.QUIT): run = False
        elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)
            if event.key == pygame.K_ESCAPE: run = False
            # Her kan man så tilføje nye7andre 'handlinger på keys - EX ændring i gravity setting
            # Kan ex lave vind med pil tl højre og venstre etc ....
            # eller indsætte static balls på random/faste positioner når bestemte taster aktiveres etc .... .. . .
            # Kan vi så måske også tilføje noget med lyd ..
            # Og kunne man tage MicroBit input ind istedet etc .... 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            apples.append(create_apple(space,event.pos))
            
            
    # opdater skærm
    screen.fill((217,217,217))  # sæt baggrundsfarve - hvordfor hvergang rundt ?? hmm
    draw_apples(apples)
    draw_static_ball(balls)
    
    space.step(1/50)
    pygame.display.update()
    clock.tick(120)         # Vent passende tid til en fornuftig frame rate (Frames pr sec.)
    
# Exit program når run er False pga ESC eller X'ed window
# Oprydning:
pygame.quit()
sys.exit()
