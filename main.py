import pygame
from pygame import mixer
from fighter import Fighter
pygame.init()
pygame.font.init()
mixer.init()

#Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#set framerate
clock = pygame.time.Clock()
FPS = 60
#define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] #player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000


#define fighter variables
EDISON_SIZE = 80
EDISON_SCALE = 4
#remember to experiment with offsets
EDISON_OFFSET = [30, 34]
EDISON_DATA = [EDISON_SIZE, EDISON_SCALE, EDISON_OFFSET]
ALEX_SIZE = 80
ALEX_SCALE = 4
ALEX_OFFSET = [30, 34]
ALEX_DATA = [ALEX_SIZE, ALEX_SCALE,ALEX_OFFSET]


#LOAD MUSIC AND SOUNDS
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)


strike_fx = pygame.mixer.Sound("assets/audio/Punch.mp3")
strike_fx.set_volume(0.3)

#add images before game loop
#load background image (allocate memory)
bg_image = pygame.image.load("assets/images/background/background.png").convert_alpha()

#load spritesheets
edison_sheet = pygame.image.load("assets/images/edison/sprites/CenteredRed.png").convert_alpha()
alex_sheet = pygame.image.load("assets/images/alex/sprites/CenteredBlue.png").convert_alpha()

#load win screen
#victory_img = pygame.image.load()
victory_img = pygame.image.load("assets/images/symbols/victory.png").convert_alpha()
victory_img = pygame.transform.scale(victory_img, (1000, 600))
#Define number of steps in each animation
EDISON_ANIMATION_STEPS = [8, 8, 1, 5, 16, 3, 13]
ALEX_ANIMATION_STEPS = [8, 8, 1, 5, 16, 3, 13]



#define font
count_font = pygame.font.Font("assets/fonts/Unbounded-VariableFont_wght.ttf", 80)
score_font = pygame.font.Font("assets/fonts/Unbounded-VariableFont_wght.ttf", 20)
#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))




#function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#function for drawing health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))



#create two instances of fighters
fighter_1 = Fighter(1, 200, 385, False, EDISON_DATA, edison_sheet, EDISON_ANIMATION_STEPS, strike_fx)
fighter_2 = Fighter(2, 700, 385, True, ALEX_DATA, alex_sheet, ALEX_ANIMATION_STEPS, strike_fx)




#GAME LOOP
run = True
while run == True:
    #framerate
    clock.tick(FPS)

    #draw background
    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    # Update countdown
    if intro_count <= 0:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
    else:
        #display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH/2.1, SCREEN_HEIGHT/3)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()


    #update fighters
    fighter_1.update()
    fighter_2.update()


    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            print(score[1])
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        #display victory image
        screen.blit(victory_img, (0, 0))
        #PLAY SOUND HERE
        #IF ROUND OVER, RELOAD HEALTH TIMER AND PLAYERS
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 385, False, EDISON_DATA, edison_sheet, EDISON_ANIMATION_STEPS, strike_fx)
            fighter_2 = Fighter(2, 700, 385, True, ALEX_DATA, alex_sheet, ALEX_ANIMATION_STEPS, strike_fx)


        #event handler
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run = False


    #update display to changes
    pygame.display.update()

#exit pygame
pygame.quit()