# Monmatia - Piano tutorial
# Created by: Veronika Gjoreva

import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 940
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
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, MEDIUMFONT, BACKGROUND_IMAGE, startRect, helpRect, quitRect
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 80)
    MEDIUMFONT = pygame.font.Font('freesansbold.ttf', 25)
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

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

    C_NOTE = pygame.mixer.Sound('sounds/do.wav')
    D_NOTE = pygame.mixer.Sound('sounds/re.wav')
    E_NOTE = pygame.mixer.Sound('sounds/mi.wav')
    F_NOTE = pygame.mixer.Sound('sounds/fa.wav')
    G_NOTE = pygame.mixer.Sound('sounds/sol.wav')
    A_NOTE = pygame.mixer.Sound('sounds/la.wav')
    H_NOTE = pygame.mixer.Sound('sounds/si.wav')
    C_O_NOTE = pygame.mixer.Sound('sounds/do_octave.wav')

    note_position = -300
    for notes in range(1, 9):
        back = pygame.sprite.Sprite()
        back.image = pygame.image.load('items/normal_key.png')
        back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT/5)))
        back.rect = back.image.get_rect()
        back.rect.center = (int(WINDOWWIDTH / 2) + note_position, int(WINDOWHEIGHT / 2) + 100)
        DISPLAYSURF.blit(back.image, back.rect)

        note_position += 100

    painoKeyNoteNames()

    songFile = open('songs/odetojoy.txt', 'r')
    content = songFile.readlines() + ['\r\n']
    songFile.close()

    songNoteLines = []
    songNote = []

    pressed_note = -300
    while True:

        pygame.display.update()
        FPSCLOCK.tick()

        for event in pygame.event.get():

            back = pygame.sprite.Sprite()
            back.image = pygame.image.load('items/normal_key.png')
            back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT / 5)))
            back.rect = back.image.get_rect()
            back.rect.center = (int(WINDOWWIDTH / 2) + pressed_note, int(WINDOWHEIGHT / 2) + 100)
            DISPLAYSURF.blit(back.image, back.rect)

            painoKeyNoteNames()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:

                if event.key == K_a:

                    pressed_note = -300
                    back = pygame.sprite.Sprite()
                    back.image = pygame.image.load('items/pressed_key.png')
                    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT / 5)))
                    back.rect = back.image.get_rect()
                    back.rect.center = (int(WINDOWWIDTH / 2) + pressed_note, int(WINDOWHEIGHT / 2) + 100)
                    DISPLAYSURF.blit(back.image, back.rect)
                    C_NOTE.play()

                    # Draw the text drop shadow
                    titleSurf, titleRect = makeTextObjs('C', MEDIUMFONT, TEXTSHADOWCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) - 300, int(WINDOWHEIGHT / 2) + 95)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    # Draw the text
                    titleSurf, titleRect = makeTextObjs('C', MEDIUMFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) - 303, int(WINDOWHEIGHT / 2) + 98)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                elif event.key == K_s:

                    pressed_note = -200
                    back = pygame.sprite.Sprite()
                    back.image = pygame.image.load('items/pressed_key.png')
                    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT / 5)))
                    back.rect = back.image.get_rect()
                    back.rect.center = (int(WINDOWWIDTH / 2) + pressed_note, int(WINDOWHEIGHT / 2) + 100)
                    DISPLAYSURF.blit(back.image, back.rect)
                    D_NOTE.play()

                    # Draw the text drop shadow
                    titleSurf, titleRect = makeTextObjs('D', MEDIUMFONT, TEXTSHADOWCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) - 200, int(WINDOWHEIGHT / 2) + 95)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    # Draw the text
                    titleSurf, titleRect = makeTextObjs('D', MEDIUMFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) - 203, int(WINDOWHEIGHT / 2) + 98)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                elif event.key == K_d:

                    pressed_note = -100
                    back = pygame.sprite.Sprite()
                    back.image = pygame.image.load('items/pressed_key.png')
                    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT / 5)))
                    back.rect = back.image.get_rect()
                    back.rect.center = (int(WINDOWWIDTH / 2) + pressed_note, int(WINDOWHEIGHT / 2) + 100)
                    DISPLAYSURF.blit(back.image, back.rect)
                    E_NOTE.play()


                    # Draw the text drop shadow
                    titleSurf, titleRect = makeTextObjs('E', MEDIUMFONT, TEXTSHADOWCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) - 100, int(WINDOWHEIGHT / 2) + 95)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    # Draw the text
                    titleSurf, titleRect = makeTextObjs('E', MEDIUMFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) - 103, int(WINDOWHEIGHT / 2) + 98)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                elif event.key == K_f:

                    pressed_note = 0
                    back = pygame.sprite.Sprite()
                    back.image = pygame.image.load('items/pressed_key.png')
                    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT / 5)))
                    back.rect = back.image.get_rect()
                    back.rect.center = (int(WINDOWWIDTH / 2) + pressed_note, int(WINDOWHEIGHT / 2) + 100)
                    DISPLAYSURF.blit(back.image, back.rect)
                    F_NOTE.play()


                    # Draw the text drop shadow
                    titleSurf, titleRect = makeTextObjs('F', MEDIUMFONT, TEXTSHADOWCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 95)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    # Draw the text
                    titleSurf, titleRect = makeTextObjs('F', MEDIUMFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) + 98)
                    DISPLAYSURF.blit(titleSurf, titleRect)


                elif event.key == K_g:

                    pressed_note = 100
                    back = pygame.sprite.Sprite()
                    back.image = pygame.image.load('items/pressed_key.png')
                    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT / 5)))
                    back.rect = back.image.get_rect()
                    back.rect.center = (int(WINDOWWIDTH / 2) + pressed_note, int(WINDOWHEIGHT / 2) + 100)
                    DISPLAYSURF.blit(back.image, back.rect)
                    G_NOTE.play()


                    # Draw the text drop shadow
                    titleSurf, titleRect = makeTextObjs('G', MEDIUMFONT, TEXTSHADOWCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) + 100, int(WINDOWHEIGHT / 2) + 95)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    # Draw the text
                    titleSurf, titleRect = makeTextObjs('G', MEDIUMFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) + 103, int(WINDOWHEIGHT / 2) + 98)
                    DISPLAYSURF.blit(titleSurf, titleRect)


                elif event.key == K_h:

                    pressed_note = 200
                    back = pygame.sprite.Sprite()
                    back.image = pygame.image.load('items/pressed_key.png')
                    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT / 5)))
                    back.rect = back.image.get_rect()
                    back.rect.center = (int(WINDOWWIDTH / 2) + pressed_note, int(WINDOWHEIGHT / 2) + 100)
                    DISPLAYSURF.blit(back.image, back.rect)
                    A_NOTE.play()

                    # Draw the text drop shadow
                    titleSurf, titleRect = makeTextObjs('A', MEDIUMFONT, TEXTSHADOWCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) + 200, int(WINDOWHEIGHT / 2) + 95)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    # Draw the text
                    titleSurf, titleRect = makeTextObjs('A', MEDIUMFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) + 203, int(WINDOWHEIGHT / 2) + 98)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                elif event.key == K_j:

                    pressed_note = 300
                    back = pygame.sprite.Sprite()
                    back.image = pygame.image.load('items/pressed_key.png')
                    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT / 5)))
                    back.rect = back.image.get_rect()
                    back.rect.center = (int(WINDOWWIDTH / 2) + pressed_note, int(WINDOWHEIGHT / 2) + 100)
                    DISPLAYSURF.blit(back.image, back.rect)
                    H_NOTE.play()


                    # Draw the text drop shadow
                    titleSurf, titleRect = makeTextObjs('H', MEDIUMFONT, TEXTSHADOWCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) + 300, int(WINDOWHEIGHT / 2) + 95)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    # Draw the text
                    titleSurf, titleRect = makeTextObjs('H', MEDIUMFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) + 303, int(WINDOWHEIGHT / 2) + 98)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                elif event.key == K_k:

                    pressed_note = 400
                    back = pygame.sprite.Sprite()
                    back.image = pygame.image.load('items/pressed_key.png')
                    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / 10), int(WINDOWHEIGHT / 5)))
                    back.rect = back.image.get_rect()
                    back.rect.center = (int(WINDOWWIDTH / 2) + pressed_note, int(WINDOWHEIGHT / 2) + 100)
                    DISPLAYSURF.blit(back.image, back.rect)
                    C_O_NOTE.play()

                    # Draw the text drop shadow
                    titleSurf, titleRect = makeTextObjs('C', MEDIUMFONT, TEXTSHADOWCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) + 400, int(WINDOWHEIGHT / 2) + 95)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    # Draw the text
                    titleSurf, titleRect = makeTextObjs('C', MEDIUMFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2) + 403, int(WINDOWHEIGHT / 2) + 98)
                    DISPLAYSURF.blit(titleSurf, titleRect)


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def painoKeyNoteNames():

    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs('C', MEDIUMFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 300, int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs('C', MEDIUMFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 303, int(WINDOWHEIGHT / 2) + 98)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs('D', MEDIUMFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 200, int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs('D', MEDIUMFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 203, int(WINDOWHEIGHT / 2) + 98)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs('E', MEDIUMFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 100, int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs('E', MEDIUMFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 103, int(WINDOWHEIGHT / 2) + 98)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs('F', MEDIUMFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs('F', MEDIUMFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) + 98)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs('G', MEDIUMFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) + 100, int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs('G', MEDIUMFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) + 103, int(WINDOWHEIGHT / 2) + 98)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs('A', MEDIUMFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) + 200, int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs('A', MEDIUMFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) + 203, int(WINDOWHEIGHT / 2) + 98)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs('H', MEDIUMFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) + 300, int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs('H', MEDIUMFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) + 303, int(WINDOWHEIGHT / 2) + 98)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs('C', MEDIUMFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) + 400, int(WINDOWHEIGHT / 2) + 95)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs('C', MEDIUMFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) + 403, int(WINDOWHEIGHT / 2) + 98)
    DISPLAYSURF.blit(titleSurf, titleRect)


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

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
