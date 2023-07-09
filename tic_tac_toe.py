import math
import random

player1 = "X"
player2 = "O"

def newBoard():
    return [[" " for _ in range(3)] for _ in range(3)]

def isGameOver(board):
    if isBoardFull(board):
        return True
    
    # Check horizontal lines
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return True
    
    # Check vertical lines
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return True
    
    # Check diagonal lines
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    
    return False

def isBoardFull(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def player(board):
    xcount = sum(row.count(player1) for row in board)
    ocount = sum(row.count(player2) for row in board)
    
    if xcount == ocount:
        return player1
    else:
        return player2

def Utility(board):
    if isBoardFull(board):
        return 0
    
    if isGameOver(board):
        turn = player(board)
        if turn == player1:
            return -1
        else:
            return 1
    
    return None

def Actions(board):
    result = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                result.append([i, j])
    return result

def Result(board, action, player):
    new_board = [row[:] for row in board]  # Create a new copy of the board
    new_board[action[0]][action[1]] = player
    return new_board

def removeAction(board, action):
    new_board = [row[:] for row in board]  # Create a new copy of the board
    new_board[action[0]][action[1]] = " "
    return new_board

def minValue(board):
    if isGameOver(board):
        return Utility(board)
    
    v = float('inf')
    for action in Actions(board):
        v = min(v, maxValue(Result(board, action, player1)))
        removeAction(board, action)
    return v

def maxValue(board):
    if isGameOver(board):
        return Utility(board)
    
    v = -float('inf')
    for action in Actions(board):
        v = max(v, minValue(Result(board, action, player2)))
        removeAction(board, action)
    return v

def AI(board):
    actions = Actions(board)
    if len(actions) == 9:
        a = random.choice(actions)
        return Result(board, a, player1)
    
    tempboard = newBoard()

    for i in range(3):
        for j in range(3):
            tempboard[i][j] = board[i][j]

    max_value = -math.inf
    max_action = None
    for action in actions:
        m = maxValue(Result(board, action, player1))
        if m > max_value:
            max_value = m
            max_action = action
    return Result(tempboard, max_action, player1)

def getCoordinates():
    while True:
        try:
            coordinates = list(map(int, input("Enter the row and column (space-separated): ").split()))
            if len(coordinates) != 2:
                raise ValueError
            row, col = coordinates
            if row < 1 or row > 3 or col < 1 or col > 3:
                raise ValueError
            return row - 1, col - 1
        except ValueError:
            print("Invalid input. Please enter valid coordinates.")

def play(player, board):
    print(player, "Turn")
    if player == player1:
        return AI(board)
    
    while True:
        row, col = getCoordinates()
        if board[row][col] == " ":
            board[row][col] = player
            return board
        else:
            print("Invalid move. Please select an empty cell.")

def printBoard(board):
    print()
    for i in range(3):
        print(board[i][0] + '|' + board[i][1] + '|' + board[i][2])
        if i < 2:
            print("------")

def printWinner(utility):
    if utility == 0:
        print("It's a tie")
    elif utility == 1:
        print(player1 + " is the winner")
    elif utility == -1:
        print(player2 + " is the winner")

def startGame():
    board = newBoard()
    printBoard(board)
    turn = player(board)

    while not isGameOver(board):
        board = play(turn, board)
        printBoard(board)
        turn = player(board)

    printWinner(Utility(board))

startGame()

