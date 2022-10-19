import sys

sys.path.append("/modules/")

import pygame
import random
import time

from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_m,
    K_a,
    K_d,
    K_h,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
)

pygame.mixer.init()
pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def new_button(buttonColor,x,y,buttonWidth,buttonHeight,buttonText,textFont,textColor):
    pygame.draw.rect(screen, buttonColor, [x, y, buttonWidth, buttonHeight])
    buttonFont = pygame.font.SysFont(textFont,buttonHeight-10)
    text = buttonFont.render(buttonText, True, textColor)

    screen.blit(text, (x + 18, y))

def new_button_cord(buttonColor,x,y,buttonWidth,buttonHeight,buttonText,textFont,TextSize,textColor,TextX,TextY):
    pygame.draw.rect(screen, buttonColor, [x, y, buttonWidth, buttonHeight])
    buttonFont = pygame.font.SysFont(textFont,TextSize)
    text = buttonFont.render(buttonText, True, textColor)

    screen.blit(text, (TextX,TextY))

def main_menu(menuRunning):
    main_menu.running = True
    main_menu.startGame = False

    menu_font = pygame.font.SysFont("arialblack",40)
    menu_color = (255,255,255)

    pygame.display.set_caption("Menu")

    while menuRunning:
        screen.fill((52,78,91))

        menu_mouse_pos = pygame.mouse.get_pos()

        playColor = (52,78,120)
        playTextColor = (255,255,255)

        quitColor = (52,78,120)
        quitTextColor = (255,255,255)

        new_button(playColor, 350, 220, 100, 50, "Play", "arial", playTextColor)

        new_button(quitColor, 350, 440, 100, 50, "Quit", "arial", quitTextColor)

        draw_text("Rocketeer", menu_font, menu_color, 290,40)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if 350 <= menu_mouse_pos[0] <= 450 and 220 <= menu_mouse_pos[1] <= 270:
                    main_menu.startGame = True
                    menuRunning = False
                if 350 <= menu_mouse_pos[0] <= 450 and 440 <= menu_mouse_pos[1] <= 490:
                    exit()
            if event.type == QUIT:
                menuRunning = False
            if event.type == KEYDOWN:
                if event.key == K_h:
                    main_menu.startGame = True
                    menuRunning = False

        pygame.display.update()

def game(gameRunning):

    pygame.display.set_caption("Game")

    cloudbool = 1

    class Background(pygame.sprite.Sprite):
        def __init__(self, image_file, location):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load("Rocketeer/assets/player2.png").convert()
            self.surf.set_colorkey((255,255,255), RLEACCEL)
            self.rect = self.surf.get_rect(
                center = (
                    (SCREEN_WIDTH-self.surf.get_width()/2)/2,
                    (SCREEN_HEIGHT-100)
                )
            )
        
        def update(self,pressed_keys):
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.rect.move_ip(-5,0)
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.rect.move_ip(5,0)
            
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH

    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load("Rocketeer/assets/cloud.png").convert()
            self.surf.set_colorkey((255,255,255), RLEACCEL)
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(20,SCREEN_WIDTH-20),
                    random.randint(20,SCREEN_HEIGHT-220)
                )
            )
        
        def update(self, cloudmvmt):
            if (cloudbool == 1):
                self.rect.move_ip(0,cloudmvmt)

    class Rocket(pygame.sprite.Sprite):
        def __init__(self):
            super(Rocket, self).__init__()
            self.surf = pygame.image.load("Rocketeer/assets/rocket.png").convert()
            self.surf.set_colorkey((255,255,255), RLEACCEL)
            self.rect = self.surf.get_rect(
                center = (
                    player.rect.right - 21,
                    player.rect.top - 20
                )
            )
        
        def update(self):
            self.rect.move_ip(0,-7)
            if self.rect.top < -50:
                self.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pygame.image.load("Rocketeer/assets/enemy.png").convert()
            self.surf.set_colorkey((255,255,255), RLEACCEL)
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(80,SCREEN_WIDTH-80),
                    -165
                )
            )
        
        def update(self,speed):
            self.rect.move_ip(0,speed)
            if self.rect.bottom > SCREEN_HEIGHT + 160:
                self.kill()
    
    player = Player()

    background = Background("Rocketeer/assets/background.png", [0,0])

    rocket_sound = pygame.mixer.Sound("Rocketeer/assets/rocketlauncher_sound.mp3")

    enemydeath_sound = pygame.mixer.Sound("Rocketeer/assets/explosion_sound.mp3")

    score = 0

    cloudmvmt = 1
    cloudspawn = 5
    cloudtimer = 0
    cloudint = 1

    enemyspawnrate = 1100
    enemyspeed = 2

    ADDROCKET = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDROCKET, 600)
    ADDENEMY = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDENEMY, enemyspawnrate)

    rockets = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    mute = False

    while gameRunning:
        cloudbool = random.randint(0,4)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.startMenu = True
                    gameRunning = False
                if event.key == K_m:
                    if mute == False:
                        mute = True
                    elif mute == True:
                        mute = False
            
            elif event.type == QUIT:
                gameRunning = False
            
            elif event.type == ADDROCKET:
                new_rocket = Rocket()
                rockets.add(new_rocket)
                all_sprites.add(new_rocket)
                if (mute == False):
                    rocket_sound.play()
            
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                if score >= 30:
                    enemyspeed = 3

                if score >= 50:
                    enemyRandom = random.randint(1,10)
                    if (enemyRandom == 10):
                        new_enemy1 = Enemy()
                        enemies.add(new_enemy1)
                        all_sprites.add(new_enemy1)

        while (cloudspawn > 0):
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
            cloudspawn -= 1

        if (cloudbool == 1):
            cloudtimer = cloudtimer + cloudint

            if (cloudtimer < 0):
                cloudint = 1
            elif (cloudtimer > 4):
                cloudint = -1
            
            if (cloudtimer == -1):
                cloudmvmt = 1
            elif (cloudtimer == 5):
                cloudmvmt = -1

        screen.fill((135, 206, 250))
        screen.blit(background.image, background.rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.groupcollide(enemies, rockets, True, True):
            if (mute == False):
                enemydeath_sound.play()
            score += 1

        pressed_keys = pygame.key.get_pressed()

        #scorefont = pygame.font.SysFont("arial",30)

        scoreButtonText = ("Score: " + str(score))
        scoreButtonColor = (255,255,255)
        scoreTextColor = (0,0,0)
        scoreButtonWidth = 110
        if (score >= 10):
            scoreButtonWidth = 120
        if (score >= 100):
            scoreButtonWidth = 132
        if (score >= 1000):
            scoreButtonWidth = 143
        if (score >= 10000):
            scoreButtonWidth = 154
        new_button_cord(scoreButtonColor,5,5,scoreButtonWidth,40,scoreButtonText,"sans",30,scoreTextColor,13,6)

        move_font = pygame.font.SysFont("arial",20)
        move_color = (0,0,0)
        draw_text("Use Arrow Keys or a/d to move.",move_font,move_color,10,SCREEN_HEIGHT-20)

        #showscore = scorefont.render(("Score: " + str(score)), 1, (0,0,0))
        #screen.blit(showscore, (10,10))

        clouds.update(cloudmvmt)
        player.update(pressed_keys)
        rockets.update()

        enemies.update(enemyspeed)

        pygame.display.flip()

        clock.tick(60)


main_menu(True)
while main_menu.running:
    if (main_menu.startGame == True):
        game(True)

    if (game.startMenu == True):
        main_menu(True)

pygame.quit()