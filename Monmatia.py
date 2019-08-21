# Monmatia - Piano tutorial
# Created by: Veronika Gjoreva

import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 1040
WINDOWHEIGHT = 580

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)

BACKGROUND_IMAGE = pygame.image.load('background/game_background.png')
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY


TILES = {'NORMAL_TILE': pygame.image.load('items/normal_tile.png'),
         'FAST_TILE': pygame.image.load('items/fast_tile.png'),
         'SLOW_TILE': pygame.image.load('items/slow_tile.png')}

ITEMS = {'SPEED_UP': pygame.image.load('items/speed_up.png'),
         'SLOW_DOWN': pygame.image.load('items/slow_down.png'),
         'NORMAL_KEY': pygame.image.load('items/normal_key.png'),
         'PRESSED_KEY': pygame.image.load('items/pressed_key.png')}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, BACKGROUND_IMAGE, startRect, helpRect, quitRect
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 80)
    pygame.display.set_caption('Monmatia')
    startRect = None
    helpRect = None
    quitRect = None

    menuScreen()

    # Load menu background music
    pygame.mixer.music.load('sounds/background_music.mp3')
    pygame.mixer.music.play(-1, 0.0)

    while True:
        pygame.display.update()
        FPSCLOCK.tick()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_position = event.pos

                if startRect.collidepoint(mouse_position):
                    pygame.mixer.music.stop()
                    startGame()
                elif helpRect.collidepoint(mouse_position):
                    helpScreen()
                elif quitRect.collidepoint(mouse_position):
                    pygame.quit()
                    sys.exit()


def menuScreen():
    global startRect, helpRect, quitRect

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    addTitleToScreen('Monmatia')

    # Draw the "START" text.
    startSurf, startRect = makeTextObjs('START', BASICFONT, TEXTCOLOR)
    startRect.center = (int(WINDOWWIDTH / 2) - 100, int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(startSurf, startRect)

    # Draw the "HELP" text.
    helpSurf, helpRect = makeTextObjs('HELP', BASICFONT, TEXTCOLOR)
    helpRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(helpSurf, helpRect)

    # Draw the "QUIT" text.
    quitSurf, quitRect = makeTextObjs('QUIT', BASICFONT, TEXTCOLOR)
    quitRect.center = (int(WINDOWWIDTH / 2) + 100, int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(quitSurf, quitRect)


def startGame():

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    print('start game')
    


def helpScreen():

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    addTitleToScreen('Help')

    # Draw back button
    back = pygame.sprite.Sprite()
    back.image = pygame.image.load('items/go_back.png')
    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH/15), int(WINDOWHEIGHT/10)))
    back.rect = back.image.get_rect()
    back.rect.center = (int(WINDOWWIDTH / 2) - 350, int(WINDOWHEIGHT / 2) - 200)
    DISPLAYSURF.blit(back.image, back.rect)

    menuFlag = False

    while True:

        if menuFlag:
            break

        pygame.display.update()
        FPSCLOCK.tick()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_position = event.pos

                if back.rect.collidepoint(mouse_position):
                    menuScreen()
                    menuFlag = True


def makeTextObjs(text, font, color):

    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def addTitleToScreen(text):

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])

    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 100)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 103)
    DISPLAYSURF.blit(titleSurf, titleRect)


if __name__ == '__main__':
    main()
