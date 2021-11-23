import os, copy, math


n = 8 # board size (even)
board = [['+' for x in range(n)] for y in range(n)]
# 8 directions
dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
diry = [-1, -1, -1, 0, 0, 1, 1, 1]

def InitBoard():
    if n % 2 == 0: # if board size is even
        z = (n - 2) / 2
        board[z][z] = '2'
        board[n - 1 - z][z] = '1'
        board[z][n - 1 - z] = '1'
        board[n - 1 - z][n - 1 - z] = '2'
        
def PrintBoard():
    m = len(str(n - 1))
    for y in range(n):
        row = ''
        for x in range(n):
            row += board[y][x]
            row += ' ' * m
        print row + ' ' + str(y)
    print
    row = ''
    for x in range(n):
        row += str(x).zfill(m) + ' '
    print row + '\n'

def MakeMove(board, x, y, player): # assuming valid move
    totctr = 0 # total number of opponent pieces taken
    board[y][x] = player
    for d in range(8): # 8 directions
        ctr = 0
        for i in range(n):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            if dx < 0 or dx > n - 1 or dy < 0 or dy > n - 1:
                ctr = 0; break
            elif board[dy][dx] == player:
                break
            elif board[dy][dx] == '+':
                ctr = 0; break
            else:
                ctr += 1
        for i in range(ctr):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            board[dy][dx] = player
        totctr += ctr
    return (board, totctr)

def ValidMove(board, x, y, player):
    if x < 0 or x > n - 1 or y < 0 or y > n - 1:
        return False
    if board[y][x] != '+':
        return False
    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
    if totctr == 0:
        return False
    return True

minEvalBoard = -1 
maxEvalBoard = n * n + 4 * n + 4 + 1
def EvalBoard(board, player):
    tot = 0
    for y in range(n):
        for x in range(n):
            if board[y][x] == player:
                #corner
                if (x == 0 and y == 0):
                    tot += 1000
                elif (x == 0 and y == n - 1):
                    tot += 1000
                elif (x == n - 1 and y == 0):
                    tot += 1000
                elif (x == n - 1 and y == n - 1):
                    tot += 1000
                #arround corner 1 
                elif (x == 1 and y == 0):
                    tot -= 10
                elif (x == 1 and y == 1):
                    tot -= 10
                elif (x == 0 and y == 1):
                    tot -= 10
                #arround corner 2
                elif (x == 6 and y == 0):
                    tot -= 10
                elif (x == 6 and y == 1):
                    tot -= 10
                elif (x == n - 1 and y == 1):
                    tot -= 10
                #arround corner 3
                elif (x == 0 and y == 6):
                    tot -= 10
                elif (x == 1 and y == 6):
                    tot -= 10
                elif (x == 1 and y == n - 1):
                    tot -= 10
                #arround corner 4
                elif (x == n - 1 and y == 6):
                    tot -= 10
                elif (x == 6 and y == 6):
                    tot -= 10
                elif (x == 6 and y == n - 1):
                    tot -= 10
                #up side
                elif (x == 2 and y == 0):
                    tot += 10
                elif (x == 3 and y == 0):
                    tot += 10
                elif (x == 4 and y == 0):
                    tot += 10
                elif (x == 5 and y == 0):
                    tot += 10
                #down side
                elif (x == 2 and y == n - 1):
                    tot += 10
                elif (x == 3 and y == n - 1):
                    tot += 10
                elif (x == 4 and y == n - 1):
                    tot += 10
                elif (x == 5 and y == n - 1):
                    tot += 10
                #left side
                elif (x == 0 and y == 2):
                    tot += 10
                elif (x == 0 and y == 3):
                    tot += 10
                elif (x == 0 and y == 4):
                    tot += 10
                elif (x == 0 and y == 5):
                    tot += 10
                #rigth side
                elif (x == n - 1 and y == 2):
                    tot += 10
                elif (x == n - 1 and y == 3):
                    tot += 10
                elif (x == n - 1 and y == 4):
                    tot += 10
                elif (x == n - 1 and y == 5):
                    tot += 10
                else:
                    tot += 1
    return tot

# if no valid move(s) possible then True
def IsTerminalNode(board, player):
    for y in range(n):
        for x in range(n):
            if ValidMove(board, x, y, player):
                return False
    return True

def Minimax(board, player, depth, maximizingPlayer):
    if depth == 0 or IsTerminalNode(board, player):
        return EvalBoard(board, player)
    if maximizingPlayer:
        bestValue = minEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = Minimax(boardTemp, player, depth - 1, False)
                    bestValue = max(bestValue, v)
    else: # minimizingPlayer
        bestValue = maxEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = Minimax(boardTemp, player, depth - 1, True)
                    bestValue = min(bestValue, v)
    return bestValue

def AlphaBeta(board, player, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or IsTerminalNode(board, player):
        return EvalBoard(board, player)
    if maximizingPlayer:
        v = minEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = max(v, AlphaBeta(boardTemp, player, depth - 1, alpha, beta, False))
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        break # beta cut-off
        return v
    else: # minimizingPlayer
        v = maxEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player):
                    (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                    v = min(v, AlphaBeta(boardTemp, player, depth - 1, alpha, beta, True))
                    beta = min(beta, v)
                    if beta <= alpha:
                        break # alpha cut-off
        return v

def BestMove(board, player):
    maxPoints = 0
    mx = -1; my = -1
    for y in range(n):
        for x in range(n):
            if ValidMove(board, x, y, player):
                (boardTemp, totctr) = MakeMove(copy.deepcopy(board), x, y, player)
                if opt == 0:
                    points = AlphaBeta(board, player, depth, minEvalBoard, maxEvalBoard, True)
                elif opt == 1:
                    points = Minimax(boardTemp, player, depth, True)
                if points > maxPoints:
                    maxPoints = points
                    mx = x; my = y
    return (mx, my)

print 'REVERSI/OTHELLO BOARD GAME'
print '0: Minimax w/ Alpha-Beta Pruning'
print '1: Minimax'
opt = int(raw_input('Select AI Algorithm: '))
if opt >= 0 and opt < 2:
    depth = 4
    depthStr = raw_input('Select Search Depth (DEFAULT: 4): ')
    if depthStr != '': depth = int(depth)
print '\n1: User 2: AI (Just press Enter for Exit!)'
InitBoard()
while True:
    for p in range(2):
        print '-------------------------'
        print
        PrintBoard()
        player = str(p + 1)
        print 'PLAYER: ' + player
        if IsTerminalNode(board, player):
            print 'Player cannot play! Game ended!'
            print 'Score User: ' + str(EvalBoard(board, '1'))
            print 'Score AI  : ' + str(EvalBoard(board, '2'))
            os._exit(0)            
        if player == '1': # user's turn
            while True:
                xy = raw_input('X Y: ')
                if xy == '': os._exit(0)
                (x, y) = xy.split()
                x = int(x); y = int(y)
                if ValidMove(board, x, y, player):
                    (board, totctr) = MakeMove(board, x, y, player)
                    print 'Piezas Tomadas: ' + str(totctr)
                    break
                else:
                    print 'Movimiento invalido, Intenta de nuevo.'
        else: # AI's turn
            (x, y) = BestMove(board, player)
            if not (x == -1 and y == -1):
                (board, totctr) = MakeMove(board, x, y, player)
                print 'AI played (X Y): ' + str(x) + ' ' + str(y)
                print 'Piezas Tomadas: ' + str(totctr)