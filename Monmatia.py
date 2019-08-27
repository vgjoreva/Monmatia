# Monmatia - Piano tutorial
# Created by: Veronika Gjoreva

import random, time, pygame, sys, math, os
from pygame.locals import *

FPS = 50
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
         'PRESSED_KEY': pygame.image.load('items/pressed_key.png'),
         'STAR_BADGE': pygame.image.load('items/success.png'),
         'NORMAL_BADGE': pygame.image.load('items/pending.png'),
         'BACK_BUTTON': pygame.image.load('items/go_back.png'),
         'NEXT': pygame.image.load('items/next.png'),
         'PREV': pygame.image.load('items/prev.png')}

SPEED = {'CURRENT': pygame.image.load('items/speed_up.png'),
         'OTHER': pygame.image.load('items/slow_down.png')}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, MEDIUMFONT, BACKGROUND_IMAGE, POINTS, startRect, helpRect, exitRect, optionsRect, slow, normal, speedUp
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
    optionsRect = None
    exitRect = None
    slow = None
    normal = None
    speedUp = None

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
                    chooseASong()
                elif helpRect.collidepoint(mouse_position):
                    helpScreen()
                elif optionsRect.collidepoint(mouse_position):
                    updateOptions()
                elif exitRect.collidepoint(mouse_position):
                    pygame.quit()
                    sys.exit()


def menuScreen(screen_name):
    global startRect, helpRect, exitRect, optionsRect

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    addTitleToScreen('Monmatia')

    if screen_name == 'init' or screen_name == 'start':
        # Start menu music
        pygame.mixer.music.play(-1, 0.0)

    # Draw the "START" button
    startRect = displayTextToScreen('START', BASICFONT, TEXTCOLOR, -150, 0)

    # Draw the "HELP" button
    helpRect = displayTextToScreen('HELP', BASICFONT, TEXTCOLOR, -50, 0)

    # Draw the "OPTIONS" button
    optionsRect = displayTextToScreen('OPTIONS', BASICFONT, TEXTCOLOR, 50, 0)

    # Draw the "EXIT" button
    exitRect = displayTextToScreen('EXIT', BASICFONT, TEXTCOLOR, 150, 0)


def chooseASong():
    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])

    # Draw the text drop shadow
    displayTextToScreen('Pick a song', BIGFONT, TEXTSHADOWCOLOR, 0, -150)

    # Draw the text
    displayTextToScreen('Pick a song', BIGFONT, TEXTCOLOR, -3, -153)

    songs = os.listdir('songs')
    songRects = []
    song_urls = []

    position = -50
    for song in songs:
        song_url = 'songs/' + song 
        songFile = open(song_url, 'r')
        title = songFile.readline()
        title = title[:-1]
        songFile.close()
        print(title)
        song_urls.append(song_url)
        song_rect = displayTextToScreen(title, BASICFONT, TEXTCOLOR, 0, position)
        songRects.append(song_rect)
        position += 50

    # Draw back button
    buttonRect = makeSpriteObject(ITEMS['BACK_BUTTON'], -350, -200, 15, 10)

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

                if buttonRect.collidepoint(mouse_position):
                    menuScreen('song_pick')
                    menuFlag = True
                else:
                    for rect in songRects:
                        if rect.collidepoint(mouse_position):
                            pygame.mixer.music.stop()
                            startGame(song_urls[songRects.index(rect)])
                            menuFlag = True


def drawPianoKeys():
    note_position = -300
    for notes in range(1, 9):
        # Create initial keyboard
        makeSpriteObject(ITEMS['NORMAL_KEY'], note_position, 100, 10, 5)
        note_position += 100

    painoKeyNoteNames()


def startGame(url):
    global POINTS, FPS

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    POINTS = 0

    container_image = pygame.image.load('background/container.png')
    makeSpriteObject(container_image, 0, -300, 1.2, 2)

    # Regular keys
    C_NOTE = pygame.mixer.Sound('sounds/do.wav')
    D_NOTE = pygame.mixer.Sound('sounds/re.wav')
    E_NOTE = pygame.mixer.Sound('sounds/mi.wav')
    F_NOTE = pygame.mixer.Sound('sounds/fa.wav')
    G_NOTE = pygame.mixer.Sound('sounds/sol.wav')
    A_NOTE = pygame.mixer.Sound('sounds/la.wav')
    H_NOTE = pygame.mixer.Sound('sounds/si.wav')
    C_O_NOTE = pygame.mixer.Sound('sounds/do_octave.wav')

    # Streched keys
    C_S_NOTE = pygame.mixer.Sound('sounds/do_stretched.wav')
    D_S_NOTE = pygame.mixer.Sound('sounds/re_stretched.wav')
    E_S_NOTE = pygame.mixer.Sound('sounds/mi_stretched.wav')
    F_S_NOTE = pygame.mixer.Sound('sounds/fa_stretched.wav')
    G_S_NOTE = pygame.mixer.Sound('sounds/sol_stretched.wav')
    A_S_NOTE = pygame.mixer.Sound('sounds/la_stretched.wav')
    H_S_NOTE = pygame.mixer.Sound('sounds/si_stretched.wav')
    C_O_S_NOTE = pygame.mixer.Sound('sounds/do_stretched_octave.wav')

    drawPianoKeys()

    songFile = open(url, 'r')
    content = songFile.readlines() + ['\r\n']
    songFile.close()

    songNote = []
    noteType = []

    for note in content:
        offset = -300
        for dots in note:
            if dots == '.':
                offset += 100
            elif dots == '0':
                songNote.append(offset)
                noteType.append('normal')
                break
            elif dots == '1':
                songNote.append(offset)
                noteType.append('faster')
                break
            elif dots == '2':
                songNote.append(offset)
                noteType.append('slower')
                break

    songNote.reverse()
    noteType.reverse()

    pressed_note = -300

    nextNote = -300
    noteNumber = 0
    play = True
    pressedKey = False
    previousNote = -1

    while play:

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        hasNotePassed = checkIfNoteHasPassed(nextNote)
        if hasNotePassed or pressedKey:
            pressedKey = False
            nextNote = -200
            noteNumber += 1

        if noteNumber == len(songNote):
            play = False
            break

        for event in pygame.event.get():

            # Return key to normal state
            makeSpriteObject(ITEMS['NORMAL_KEY'], pressed_note, 100, 10, 5)

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
                        drawPianoKeys()

                elif event.key == K_a:
                    pressed_note = -300
                    if noteType[noteNumber] == 'slower':
                        C_S_NOTE.play()
                    else:
                        C_NOTE.play()
                    pressedKey = True

                elif event.key == K_s:
                    pressed_note = -200
                    if noteType[noteNumber] == 'slower':
                        D_S_NOTE.play()
                    else:
                        D_NOTE.play()
                    pressedKey = True

                elif event.key == K_d:
                    pressed_note = -100
                    if noteType[noteNumber] == 'slower':
                        E_S_NOTE.play()
                    else:
                        E_NOTE.play()
                    pressedKey = True

                elif event.key == K_f:
                    pressed_note = 0
                    if noteType[noteNumber] == 'slower':
                        F_S_NOTE.play()
                    else:
                        F_NOTE.play()
                    pressedKey = True

                elif event.key == K_g:
                    pressed_note = 100
                    if noteType[noteNumber] == 'slower':
                        G_S_NOTE.play()
                    else:
                        G_NOTE.play()
                    pressedKey = True

                elif event.key == K_h:
                    pressed_note = 200
                    if noteType[noteNumber] == 'slower':
                        A_S_NOTE.play()
                    else:
                        A_NOTE.play()
                    pressedKey = True

                elif event.key == K_j:
                    pressed_note = 300
                    if noteType[noteNumber] == 'slower':
                        H_S_NOTE.play()
                    else:
                        H_NOTE.play()
                    pressedKey = True

                elif event.key == K_k:
                    pressed_note = 400
                    if noteType[noteNumber] == 'slower':
                        C_O_S_NOTE.play()
                    else:
                        C_O_NOTE.play()
                    pressedKey = True

        DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
        drawPianoKeys()

        if pressedKey:
            makeSpriteObject(ITEMS['PRESSED_KEY'], pressed_note, 100, 10, 5)
            addPoints(pressed_note, songNote[noteNumber], nextNote)

        painoKeyNoteNames()

        # Current note
        if noteType[noteNumber] == 'normal':
            makeSpriteObject(TILES['NORMAL_TILE'], songNote[noteNumber], nextNote, 10, 5)
        elif noteType[noteNumber] == 'slower':
            makeSpriteObject(TILES['SLOW_TILE'], songNote[noteNumber], nextNote, 10, 5)
        elif noteType[noteNumber] == 'faster':
            makeSpriteObject(TILES['FAST_TILE'], songNote[noteNumber], nextNote, 10, 5)

        if not pressedKey:
            if noteType[noteNumber] == 'faster':
                nextNote += 10
            else:
                nextNote += 5
        
        makeSpriteObject(container_image, 0, -300, 1.05, 2)

    if not play:

        if noteNumber < len(songNote)-1:
            finishGame(1)
        else:
            finishGame(len(songNote))


def finishGame(total_notes):
    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])

    # Draw the text drop shadow
    displayTextToScreen('Game Over', BIGFONT, TEXTSHADOWCOLOR, 0, -150)

    # Draw the text
    displayTextToScreen('Game Over', BIGFONT, TEXTCOLOR, -3, -153)

    if total_notes >= POINTS > 0.8 * total_notes:
        makeSpriteObject(ITEMS['STAR_BADGE'], -75, -50, 10, 5)
        makeSpriteObject(ITEMS['STAR_BADGE'], 0, -50, 10, 5)
        makeSpriteObject(ITEMS['STAR_BADGE'], 75, -50, 10, 5)
    elif 0.8 * total_notes >= POINTS > 0.6 * total_notes:
        makeSpriteObject(ITEMS['STAR_BADGE'], -75, -50, 10, 5)
        makeSpriteObject(ITEMS['STAR_BADGE'], 0, -50, 10, 5)
        makeSpriteObject(ITEMS['NORMAL_BADGE'], 75, -50, 10, 5)
    elif 0.6 * total_notes >= POINTS > 0.4 * total_notes:
        makeSpriteObject(ITEMS['STAR_BADGE'], -75, -50, 10, 5)
        makeSpriteObject(ITEMS['NORMAL_BADGE'], 0, -50, 10, 5)
        makeSpriteObject(ITEMS['NORMAL_BADGE'], 75, -50, 10, 5)
    else:
        makeSpriteObject(ITEMS['NORMAL_BADGE'], -75, -50, 10, 5)
        makeSpriteObject(ITEMS['NORMAL_BADGE'], 0, -50, 10, 5)
        makeSpriteObject(ITEMS['NORMAL_BADGE'], 75, -50, 10, 5)

    displayTextToScreen('Player accuracy: ' + str(math.ceil(POINTS/(total_notes/100))) + '%', MEDIUMFONT, TEXTCOLOR, 0, 50)

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
                    pygame.mixer.music.play()
                    chooseASong()

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
    if nextNote > 125:
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
    
    # Draw the text drop shadow
    displayTextToScreen('Help', BIGFONT, TEXTSHADOWCOLOR, 0, -175)

    # Draw the text
    displayTextToScreen('Help', BIGFONT, TEXTCOLOR, -3, -178)

    displayTextToScreen('Note - Key', MEDIUMFONT, TEXTCOLOR, -125, -100)
    displayTextToScreen('C1(DO) - a', BASICFONT, TEXTCOLOR, -200, -50)
    displayTextToScreen('D(RE) - s', BASICFONT, TEXTCOLOR, -200, -25)
    displayTextToScreen('E(MI) - d', BASICFONT, TEXTCOLOR, -200, 0)
    displayTextToScreen('F(FA) - f', BASICFONT, TEXTCOLOR, -200, 25)
    displayTextToScreen('G(SOL) - g', BASICFONT, TEXTCOLOR, -200, 50)
    displayTextToScreen('A(LA) - h', BASICFONT, TEXTCOLOR, -25, -50)
    displayTextToScreen('H(SI) - j', BASICFONT, TEXTCOLOR, -25, -25)
    displayTextToScreen('C2(DO) - k', BASICFONT, TEXTCOLOR, -25, 0)
    displayTextToScreen('p - pause', BASICFONT, TEXTCOLOR, -25, 25)

    makeSpriteObject(TILES['NORMAL_TILE'], 100, -100, 10, 5)
    displayTextToScreen('Quarter note', BASICFONT, TEXTCOLOR, 215, -100)
    makeSpriteObject(TILES['FAST_TILE'], 100, 0, 10, 5)
    displayTextToScreen('Eighth note (faster note)', BASICFONT, TEXTCOLOR, 275, 0)
    makeSpriteObject(TILES['SLOW_TILE'], 100, 100, 10, 5)
    displayTextToScreen('Half note (longer note)', BASICFONT, TEXTCOLOR, 275, 100)

    # Draw back button
    rect = makeSpriteObject(ITEMS['BACK_BUTTON'], -350, -200, 15, 10)

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


def updateOptions():
    global slow, normal, speedUp, FPS

    DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])
    
    # Draw the text drop shadow
    displayTextToScreen('Options', BIGFONT, TEXTSHADOWCOLOR, 0, -175)

    # Draw the text
    displayTextToScreen('Options', BIGFONT, TEXTCOLOR, -3, -178)

    if slow == None and normal == None and speedUp == None:
        slow = SPEED['OTHER']
        normal = SPEED['CURRENT']
        speedUp = SPEED['OTHER']

    prev = makeSpriteObject(ITEMS['PREV'], -230, 0, 10, 10)
    next = makeSpriteObject(ITEMS['NEXT'], 230, 0, 10, 10)
    
    slowDownRect = makeSpriteObject(slow, -100, 0, 10, 5)
    displayTextToScreen('Slower', BASICFONT, TEXTCOLOR, -100, 50)
    normalSpeedRect = makeSpriteObject(normal, 0, 0, 10, 5)
    displayTextToScreen('Normal', BASICFONT, TEXTCOLOR, 0, 50)
    speedUpRect = makeSpriteObject(speedUp, 100, 0, 10, 5)
    displayTextToScreen('Faster', BASICFONT, TEXTCOLOR, 100, 50)

    displayTextToScreen('Note Speed', MEDIUMFONT, TEXTCOLOR, 0, 100)


    # Draw back button
    rect = makeSpriteObject(ITEMS['BACK_BUTTON'], -350, -200, 15, 10)

    menuFlag = False
    clicked = False

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
                elif next.collidepoint(mouse_position):
                    FPS += 30
                    clicked = True
                    if normal == SPEED['CURRENT']:
                        normal = SPEED['OTHER']
                        speedUp = SPEED['CURRENT']
                    elif slow == SPEED['CURRENT']:
                        slow = SPEED['OTHER']
                        normal = SPEED['CURRENT']

                elif prev.collidepoint(mouse_position):
                    FPS -= 30
                    clicked = True
                    if speedUp == SPEED['CURRENT']:
                        normal = SPEED['CURRENT']
                        speedUp = SPEED['OTHER']
                    elif normal == SPEED['CURRENT']:
                        slow = SPEED['CURRENT']
                        normal = SPEED['OTHER']
                
            if clicked:
                clicked = False
                DISPLAYSURF.blit(BACKGROUND_IMAGE, [0, 0])

                # Draw the text drop shadow
                displayTextToScreen('Options', BIGFONT, TEXTSHADOWCOLOR, 0, -175)

                # Draw the text
                displayTextToScreen('Options', BIGFONT, TEXTCOLOR, -3, -178)

                prev = makeSpriteObject(ITEMS['PREV'], -230, 0, 10, 10)
                next = makeSpriteObject(ITEMS['NEXT'], 230, 0, 10, 10)
                
                slowDownRect = makeSpriteObject(slow, -100, 0, 10, 5)
                displayTextToScreen('Slower', BASICFONT, TEXTCOLOR, -100, 50)
                normalSpeedRect = makeSpriteObject(normal, 0, 0, 10, 5)
                displayTextToScreen('Normal', BASICFONT, TEXTCOLOR, 0, 50)
                speedUpRect = makeSpriteObject(speedUp, 100, 0, 10, 5)
                displayTextToScreen('Faster', BASICFONT, TEXTCOLOR, 100, 50)

                displayTextToScreen('Note Speed', MEDIUMFONT, TEXTCOLOR, 0, 100)

                # Draw back button
                rect = makeSpriteObject(ITEMS['BACK_BUTTON'], -350, -200, 15, 10)



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


def makeSpriteObject(image, position_width, position_height, scale_width, scale_height):
    back = pygame.sprite.Sprite()
    back.image = image
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
