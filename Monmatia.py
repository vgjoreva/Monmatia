# Monmatia - Piano tutorial
# Created by: Veronika Gjoreva

import random, time, pygame, sys
from pygame.locals import *

FPS = 40
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
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, MEDIUMFONT, BACKGROUND_IMAGE, POINTS, startRect, helpRect, exitRect
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 80)
    MEDIUMFONT = pygame.font.Font('freesansbold.ttf', 25)
    pygame.display.set_caption('Monmatia')
    POINTS = 0

    startRect = None
    helpRect = None
    exitRect = None

    # Load menu background music
    pygame.mixer.music.load('sounds/background_music.mp3')

    menuScreen('init')

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
                elif exitRect.collidepoint(mouse_position):
                    pygame.quit()
                    sys.exit()


def menuScreen(screen_name):
    global startRect, helpRect, exitRect

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    addTitleToScreen('Monmatia')

    if screen_name == 'init' or screen_name == 'start':
        # Start menu music
        pygame.mixer.music.play(-1, 0.0)

    # Draw the "START" button
    startRect = displayTextToScreen('START', BASICFONT, TEXTCOLOR, -100, 0)

    # Draw the "HELP" button
    helpRect = displayTextToScreen('HELP', BASICFONT, TEXTCOLOR, 0, 0)

    # Draw the "EXIT" button
    exitRect = displayTextToScreen('EXIT', BASICFONT, TEXTCOLOR, 100, 0)


def drawPainoKeys():
    note_position = -300
    for notes in range(1, 9):
        # Create initial keyboard
        makeSpriteObject('items/normal_key.png', note_position, 100, 10, 5)
        note_position += 100

    painoKeyNoteNames()


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

    drawPainoKeys()

    songFile = open('songs/odetojoy.txt', 'r')
    content = songFile.readlines() + ['\r\n']
    songFile.close()

    songNoteLines = []
    songNote = []

    for note in content:
        offset = -300
        for dots in note:
            if dots == '.':
                offset += 100
            elif dots == '0':
                songNote.append(offset)
                break

    songNote.reverse()

    pressed_note = -300

    nextNote = -300
    noteNumber = 0
    play = True
    pressedKey = False

    while play:

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        hasNotePassed = checkIfNoteHasPassed(nextNote)
        if hasNotePassed:
            nextNote = -300
            noteNumber += 1

        if noteNumber == len(songNote):
            play = False
            break

        for event in pygame.event.get():

            # Return key to normal state
            makeSpriteObject('items/normal_key.png', pressed_note, 100, 10, 5)

            # Make sure key labels remain on all the keys
            painoKeyNoteNames()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:

                if event.key == K_p:
                    play = pauseGame()
                    if play:
                        DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
                        drawPainoKeys()

                elif event.key == K_a:
                    pressed_note = -300
                    C_NOTE.play()
                    pressedKey = True

                elif event.key == K_s:
                    pressed_note = -200
                    D_NOTE.play()
                    pressedKey = True

                elif event.key == K_d:
                    pressed_note = -100
                    E_NOTE.play()
                    pressedKey = True

                elif event.key == K_f:
                    pressed_note = 0
                    F_NOTE.play()
                    pressedKey = True

                elif event.key == K_g:
                    pressed_note = 100
                    G_NOTE.play()
                    pressedKey = True

                elif event.key == K_h:
                    pressed_note = 200
                    A_NOTE.play()
                    pressedKey = True

                elif event.key == K_j:
                    pressed_note = 300
                    H_NOTE.play()
                    pressedKey = True

                elif event.key == K_k:
                    pressed_note = 400
                    C_O_NOTE.play()
                    pressedKey = True

        DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
        drawPainoKeys()

        if pressedKey:
            makeSpriteObject('items/pressed_key.png', pressed_note, 100, 10, 5)
            addPoints(pressed_note, songNote[noteNumber], nextNote)

        painoKeyNoteNames()

        # Current note
        makeSpriteObject('items/normal_tile.png', songNote[noteNumber], nextNote, 10, 5)

        if pressedKey:
            nextNote = 100
            pressedKey = False
        else:
            nextNote += 100

    if not play:
        finishGame(len(songNote))


def finishGame(total_notes):
    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])

    # Draw the text drop shadow
    displayTextToScreen('Game Over', BIGFONT, TEXTSHADOWCOLOR, 0, -150)

    # Draw the text
    displayTextToScreen('Game Over', BIGFONT, TEXTCOLOR, -3, -153)

    if total_notes >= POINTS > 0.8 * total_notes:
        makeSpriteObject('items/success.png', -75, -50, 10, 5)
        makeSpriteObject('items/success.png', 0, -50, 10, 5)
        makeSpriteObject('items/success.png', 75, -50, 10, 5)
    elif 0.8 * total_notes >= POINTS > 0.6 * total_notes:
        makeSpriteObject('items/success.png', -75, -50, 10, 5)
        makeSpriteObject('items/success.png', 0, -50, 10, 5)
        makeSpriteObject('items/pending.png', 75, -50, 10, 5)
    elif 0.6 * total_notes >= POINTS > 0.4 * total_notes:
        makeSpriteObject('items/success.png', -75, -50, 10, 5)
        makeSpriteObject('items/pending.png', 0, -50, 10, 5)
        makeSpriteObject('items/pending.png', 75, -50, 10, 5)
    else:
        makeSpriteObject('items/pending.png', -75, -50, 10, 5)
        makeSpriteObject('items/pending.png', 0, -50, 10, 5)
        makeSpriteObject('items/pending.png', 75, -50, 10, 5)

    displayTextToScreen('Score: ' + str(POINTS), MEDIUMFONT, TEXTCOLOR, 0, 50)

    # Draw the "RESUME" button
    playAgainRect = displayTextToScreen('PLAY AGAIN', BASICFONT, TEXTCOLOR, -100, 100)

    # Draw the "QUIT" button
    quitRect = displayTextToScreen('QUIT', BASICFONT, TEXTCOLOR, 100, 100)

    menuFlag = False
    continuePlaying = False

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

                if playAgainRect.collidepoint(mouse_position):
                    menuFlag = True
                    startGame()

                elif quitRect.collidepoint(mouse_position):
                    menuFlag = True
                    menuScreen('start')


def addPoints(pressed_key, current_note, tile_position):
    global POINTS

    if pressed_key == current_note:
        if tile_position >= 75:
            POINTS += 1
        elif 75 > tile_position >= 50:
            POINTS += 0.5


def checkIfNoteHasPassed(nextNote):
    if nextNote > 150:
        return True
    return False


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def painoKeyNoteNames():

    # C key
    displayTextToScreen('C', MEDIUMFONT, TEXTSHADOWCOLOR, -300, 95)
    displayTextToScreen('C', MEDIUMFONT, TEXTCOLOR, -303, 98)

    # D key
    displayTextToScreen('D', MEDIUMFONT, TEXTSHADOWCOLOR, -200, 95)
    displayTextToScreen('D', MEDIUMFONT, TEXTCOLOR, -203, 98)

    # E key
    displayTextToScreen('E', MEDIUMFONT, TEXTSHADOWCOLOR, -100, 95)
    displayTextToScreen('E', MEDIUMFONT, TEXTCOLOR, -103, 98)

    # F key
    displayTextToScreen('F', MEDIUMFONT, TEXTSHADOWCOLOR, 0, 95)
    displayTextToScreen('F', MEDIUMFONT, TEXTCOLOR, -3, 98)

    # G key
    displayTextToScreen('G', MEDIUMFONT, TEXTSHADOWCOLOR, 100, 95)
    displayTextToScreen('G', MEDIUMFONT, TEXTCOLOR, 103, 98)

    # A key
    displayTextToScreen('A', MEDIUMFONT, TEXTSHADOWCOLOR, 200, 95)
    displayTextToScreen('A', MEDIUMFONT, TEXTCOLOR, 203, 98)

    # H key
    displayTextToScreen('H', MEDIUMFONT, TEXTSHADOWCOLOR, 300, 95)
    displayTextToScreen('H', MEDIUMFONT, TEXTCOLOR, 303, 98)

    # C octave key
    displayTextToScreen('C', MEDIUMFONT, TEXTSHADOWCOLOR, 400, 95)
    displayTextToScreen('C', MEDIUMFONT, TEXTCOLOR, 403, 98)


def helpScreen():

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    addTitleToScreen('Help')

    # Draw back button
    rect = makeSpriteObject('items/go_back.png', -350, -200, 15, 10)

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

                if rect.collidepoint(mouse_position):
                    menuScreen('help')
                    menuFlag = True


def pauseGame():

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    addTitleToScreen('Pause')

    # Draw the "RESUME" button
    resumeRect = displayTextToScreen('RESUME', BASICFONT, TEXTCOLOR, -100, 0)

    # Draw the "QUIT" button
    quitRect = displayTextToScreen('QUIT', BASICFONT, TEXTCOLOR, 100, 0)

    menuFlag = False
    continuePlaying = False

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

                if resumeRect.collidepoint(mouse_position):
                    menuFlag = True
                    continuePlaying = True

                elif quitRect.collidepoint(mouse_position):
                    menuFlag = True
                    continuePlaying = False

    return continuePlaying


def makeTextObjs(text, font, color):

    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def makeSpriteObject(image_url, position_width, position_height, scale_width, scale_height):
    back = pygame.sprite.Sprite()
    back.image = pygame.image.load(image_url)
    back.image = pygame.transform.scale(back.image, (int(WINDOWWIDTH / scale_width), int(WINDOWHEIGHT / scale_height)))
    back.rect = back.image.get_rect()
    back.rect.center = (int(WINDOWWIDTH / 2) + position_width, int(WINDOWHEIGHT / 2) + position_height)
    DISPLAYSURF.blit(back.image, back.rect)
    return back.rect


def displayTextToScreen(text, font, color, offset_width, offset_height):

    global startRect, helpRect, exitRect

    titleSurf, titleRect = makeTextObjs(text, font, color)
    titleRect.center = (int(WINDOWWIDTH / 2) + offset_width, int(WINDOWHEIGHT / 2) + offset_height)
    DISPLAYSURF.blit(titleSurf, titleRect)
    return titleRect


def addTitleToScreen(text):

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])

    # Draw the text drop shadow
    displayTextToScreen(text, BIGFONT, TEXTSHADOWCOLOR, 0, -100)

    # Draw the text
    displayTextToScreen(text, BIGFONT, TEXTCOLOR, -3, -103)


if __name__ == '__main__':
    main()
