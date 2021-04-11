import pygame, sys
from time import sleep

SCREEN = (600,600)
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
BG_COLOR = (28,170,156)
LINE_COLOR = (23,145,135)
CIRCLE_RADIUS = 60
CIRCLE_LINE = 15

game_board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']

def empty_cells(board):
    cells=[]
    for x, cell in enumerate(board):
        if cell == ' ':
            cells.append(x)
    return cells

def valid_move(x):
    return x in empty_cells(game_board)

def move(x, player):
    if valid_move(x):
        game_board[x] = player
        return True
    else:
        return False

def evaluate(board):
    if check_win(board,'X'):
        score = 1
    elif check_win(board,'O'):
        score = -1
    else:
        score = 0
    return score

def check_win(board, player):
    win_conf = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]],
    ]
    return [player,player,player] in win_conf

def game_over(board):
    return check_win(board,'X') or check_win(board,'O')

def minimax(board, depth, maxPlayer):
    pos = -1
    if depth == 0 or len(empty_cells(board)) == 0 or game_over(board):
        return -1, evaluate(board)

    if maxPlayer:
        value = -10000
        for p in empty_cells(board):
            board[p] = 'X'

            x, score = minimax(board, depth-1,False)
            board[p] = ' '
            if score > value:
                value = score
                pos = p
    else:
        value = +10000
        for p in empty_cells(board):
            board[p] = 'O'

            x, score = minimax(board, depth - 1, True)
            board[p] = ' '
            if score < value:
                value = score
                pos = p
    return pos, value

def drawLines():
    global screen
    pygame.draw.line(screen, LINE_COLOR,(200,0),(200,600),10)
    pygame.draw.line(screen, LINE_COLOR,(400,0),(400,600),10)
    pygame.draw.line(screen, LINE_COLOR,(0,200),(600,200),10)
    pygame.draw.line(screen, LINE_COLOR,(0,400),(600,400),10)

def drawPlayer(idx, player):
    global screen
    pygame.draw.circle(screen, player ,(200*(idx%3)+100 , 200*(idx//3)+100), CIRCLE_RADIUS,CIRCLE_LINE )

def dispMessage(text):
    global screen

    textfont = pygame.font.Font('freesansbold.ttf', 50)
    text = textfont.render(text, True, RED)
    textpos = text.get_rect()
    textpos.center = (300, 300)
    screen.blit(text, textpos)
    pygame.display.update()
    sleep(1.8)
    sys.exit()

def runGame():
    global screen
    global player

    endFlag = False
    node = 10

    while not endFlag:
        if len(empty_cells(game_board)) == 0 or game_over(game_board):
            endFlag = True
            break

        while player=='X':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    clickedRow = int(mouseY // 200)
                    clickedCol = int(mouseX // 200)
                    idx = clickedRow*3+clickedCol
                    if move(idx,player):
                        node-=2
                        player='O'
                        drawPlayer(idx,WHITE)
            pygame.display.update()

        i, v = minimax(game_board, node, False)
        move(i, player)
        player = 'X'
        drawPlayer(i, BLACK)
        pygame.display.update()

    if check_win(game_board, 'X'):
        print('당 신 승 리') #never
    elif check_win(game_board, 'O'):
        dispMessage("King!you can't beat me!")
    else:
        dispMessage("DRAW")

def initGame():
    global screen,player

    pygame.init()
    screen = pygame.display.set_mode(SCREEN)
    pygame.display.set_caption('TIC TAC TOE')
    screen.fill(BG_COLOR)
    drawLines()
    player='X'

initGame()
runGame()