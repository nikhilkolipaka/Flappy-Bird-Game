# ///////// Required Modules //////////
import random
import pygame
import sys
from pygame.locals import *
import time

#////////// Welcome Screen funtion ///////////
def Intial_Screen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return
            else:
                Screen.blit(game_images['background'],(0,0))
                Screen.blit(game_images['title'],(0,0))
                pygame.display.update()
                FPSCLOCK.tick(Fps)
#//////// Main Game funtion //////////////
def Main_Game():
    score           = 0
    screen_width    = 1300
    screen_height   = 647
    base_height     = screen_height*0.75
    player_height   = game_images['bird'].get_height()
    pipe_width      = game_images['pipe'][0].get_width()
    playerx         = screen_width*0.05
    playery         = screen_height*0.3
    y1              = screen_height*0.1
    PipeVel         = -4 # velocity of pipe
    playervel       = -9 # velocity of bird while falpping 
    playermaxvel    = 10 # maximium velocity of bird while falpping
    playerminvel    = -8 # minimium velocity of bird while falpping
    playerAcc       = 0.8 # velocity of bird falling down (or) Acceleration due to gravity
    playerflapped   = False # True only when bird is flapping
    pipe_height     = game_images['pipe'][0].get_height()
    #///////////// Creating random pipes ///////////////////////
    new_pipe1  = Get_Random()
    new_pipe2  = Get_Random()
    new_pipe3  = Get_Random()
    new_pipe4  = Get_Random()
    new_pipe5  = Get_Random()
    new_pipe6  = Get_Random() 
    new_pipe7  = Get_Random()
    #///////////////// Creating Random upper pipes and lower pipes /////////////////////
    upper_pipe = [{'x': 500,'y': new_pipe1[0]['y']},{'x': 500+200,'y': new_pipe2[0]['y']},
                  {'x': 500+200+200,'y': new_pipe3[0]['y']},{'x': 500+200+200+200,'y': new_pipe4[0]['y']},
                  {'x': 500+200+200+200+200,'y': new_pipe5[0]['y']},{'x': 500+200+200+200+200+200,'y': new_pipe6[0]['y']},
                  {'x': 500+200+200+200+200+200+200,'y': new_pipe7[0]['y']}]
    lower_pipe = [{'x': 500,'y': new_pipe1[1]['y']},{'x': 500+200,'y': new_pipe2[1]['y']},
                  {'x': 500+200+200,'y': new_pipe3[1]['y']},{'x': 500+200+200+200,'y': new_pipe4[1]['y']},
                  {'x': 500+200+200+200+200,'y': new_pipe5[1]['y']},{'x': 500+200+200+200+200+200,'y': new_pipe6[1]['y']},
                  {'x': 500+200+200+200+200+200+200,'y': new_pipe7[1]['y']}]
    #///////////// Game Loop //////////////////////////////////
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                game_sounds['wing'].play()
                if playery > 0:
                    playervel     = playerminvel
                    playerflapped = True
        # //////////// Crash test ////////////////
        crash = Iscollide(playerx,playery,upper_pipe,lower_pipe)
        #//////////// Velocity of bird falling down ///////////////
        if playervel < playermaxvel and not playerflapped:
            playervel+=playerAcc
        #//////////// Velocity of bird moving up while flapping ///////////////
        if playerflapped:
            playerflapped = False
        playery = playery + min(playervel,((base_height+20)-playery-player_height))
        #/////////// Velocity of pipe moving to the left /////////////
        for upperpipe,lowerpipe in zip(upper_pipe,lower_pipe):
            upperpipe['x'] += PipeVel
            lowerpipe['x'] += PipeVel
        #/////////// Adding pipes to th list //////////////////////
        if 0 < upper_pipe[0]['x'] < 5:
            newpipe = Get_Random()
            upper_pipe.append(newpipe[0])
            lower_pipe.append(newpipe[1])

        #//////////////// if the pipe is out of the screen, remove it /////////////////
        if upper_pipe[0]['x'] < - game_images['pipe'][0].get_width():
            upper_pipe.pop(0)
            lower_pipe.pop(0)
        #/////////////// Increment of Score ////////////////////
        playermidpos = playerx+(game_images['bird'].get_width()/2)
        for upper in upper_pipe:
            if playermidpos >= upper['x']+(pipe_width/2) and playermidpos < upper['x']+(pipe_width/2)+5 :
                score+=1
                game_sounds['point'].play()
        #///////// Bliting the imsges on Screen ////////////////////
        Screen.blit(game_images['background'],(0,0))
        Screen.blit(game_images['bird'],(Screen_Width*0.05,playery))
        for upperpipe,lowerpipe in zip(upper_pipe,lower_pipe):
            Screen.blit(game_images['pipe'][0],(upperpipe['x'],upperpipe['y']))
            Screen.blit(game_images['pipe'][1],(lowerpipe['x'],lowerpipe['y']))    
        Screen.blit(game_images['base'],(0,screen_height*0.75)) 
        Screen.blit(game_images['base1'],(0,screen_height*0.94)) 
        my_digits=[int(x) for x in list(str(score))]
        offset=screen_width/2
        for digit in my_digits:
            Screen.blit(game_images['numbers'][digit],(offset,screen_height*0.2))
            offset+=game_images['numbers'][digit].get_width()  
        if crash:
            time.sleep(0.1)
            Screen.blit(game_images['Gameover'],(0,0)) 
            offset=506+180
            for digit in my_digits:
                Screen.blit(game_images['numbers'][digit],(offset,443))
                offset+=game_images['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(Fps)
            return     
        pygame.display.update()
        FPSCLOCK.tick(Fps)
#////////////// Function to get Random  pipe //////////////////
def Get_Random():
    screen_width  = 1300
    screen_height = 647
    pipe_height   = game_images['pipe'][0].get_height()
    rand          = random.randrange(int(screen_height*0.1),int(screen_height*0.45))
    y1            = rand
    y2            = (pipe_height-y1)+150
    pipeX         = screen_width+100
    lst           = [{'x': pipeX,'y': -y1},{'x': pipeX,'y': y2}]
    return lst
#////////// Function to test the bird Crash //////////////////////
def Iscollide(playerx,playery,upperPipes,lowerPipes):
    if playery<-5 or (playery + game_images['bird'].get_height()) > (Screen_Height*0.75)+7:
        game_sounds['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = game_images['pipe'][0].get_height()
        if playery < (pipeHeight + pipe['y'])-10 and abs(playerx - pipe['x']) < game_images['bird'].get_width()-2:
            game_sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + game_images['bird'].get_height() > pipe['y']+5) and abs(playerx - pipe['x']) < game_images['bird'].get_width()-2:
            game_sounds['hit'].play()
            return True
    return False

if __name__ == "__main__":
    pygame.init() # Initialize all pygame's modules
    pygame.mixer.init() # Initialize mixer funtion
    Fps           = 32
    Screen_Width  = 1300
    Screen_Height = 647
    FPSCLOCK      = pygame.time.Clock()
    game_images   = {}
    game_sounds   = {}
    Screen        = pygame.display.set_mode((Screen_Width,Screen_Height)) # Creating a Screen for the Game
    pygame.display.set_caption('Flappy Bird Game By Nikhil') # Caption for the game
# ////////// Getting  Required Images //////////// 
    game_images['numbers']  =  (      
                                    pygame.image.load('gallery/images/0.png').convert_alpha(),
                                    pygame.image.load('gallery/images/1.png').convert_alpha(),
                                    pygame.image.load('gallery/images/2.png').convert_alpha(),
                                    pygame.image.load('gallery/images/3.png').convert_alpha(),
                                    pygame.image.load('gallery/images/4.png').convert_alpha(),
                                    pygame.image.load('gallery/images/5.png').convert_alpha(),
                                    pygame.image.load('gallery/images/6.png').convert_alpha(),
                                    pygame.image.load('gallery/images/7.png').convert_alpha(),
                                    pygame.image.load('gallery/images/8.png').convert_alpha(),
                                    pygame.image.load('gallery/images/9.png').convert_alpha()
                                )
    game_images['background'] = pygame.image.load('gallery/images/background.jpg').convert_alpha()
    game_images['title']      = pygame.image.load('gallery/images/title.png').convert_alpha()
    game_images['bird']       = pygame.image.load('gallery/images/bird.png').convert_alpha()
    game_images['pipe']       = ( pygame.transform.rotate(pygame.image.load('gallery/images/pipe.png').convert_alpha(),180),
                                  pygame.image.load('gallery/images/pipe.png').convert_alpha()
                                )
    game_images['base']       = pygame.image.load('gallery/images/base.jpg').convert_alpha()
    game_images['base1']      = pygame.image.load('gallery/images/base1.jpg').convert_alpha()
    game_images['Gameover']   = pygame.image.load('gallery/images/Gameover.png').convert_alpha()
# ////////// Getting  Required Sounds //////////// 
    game_sounds['die']    = pygame.mixer.Sound('gallery/sounds/die.wav')
    game_sounds['hit']    = pygame.mixer.Sound('gallery/sounds/hit.wav')
    game_sounds['point']  = pygame.mixer.Sound('gallery/sounds/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('gallery/sounds/swoosh.wav')
    game_sounds['wing']   = pygame.mixer.Sound('gallery/sounds/wing.wav')
    # //////////// Loop to Play Game //////////////
    while True:
        Intial_Screen()
        Main_Game()