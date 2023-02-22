"""
Tic Tac Toe Player
"""

from ast import Or
import math
from queue import Empty
from re import A
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    playerX=0
    playerO=0
    for i in range(3):
        for j in range(3):
            if board[i][j] is not None:
                if board[i][j] == "X":
                    playerX = playerX + 1
                if board[i][j] == "O":
                    playerO = playerO + 1    
    if playerO < playerX:
        return "O"
    else:
        return "X"            


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                t = (i,j)
                moves.add(t)
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid move")
    boardcopy= copy.deepcopy(board)
    boardcopy[action[0]][action[1]] = player(board)

    return boardcopy



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        sign = board[i][0]
        if sign is None:
            continue
        for j in range(3):
            if sign == None:
                break
            if board[i][j] != sign:
                break
            if j == 2 and board[i][j] == sign:
                return sign
    for j in range(3):
        sign = board[0][j]
        if sign is None:
            continue
        for i in range(3):
            if sign == None:
                break
            if board[i][j] != sign:
                break
            if i == 2 and board[i][j] == sign:
                return sign
    if board[0][0] is not None:
       if board[1][1] is not None:
           if board[2][2] is not None:
               if board[0][0] == board [1][1] and board[0][0] == board [2][2]:
                    return board[0][0]
    if board[0][2] is not None:
       if board[1][1] is not None:
           if board[2][0] is not None:
               if board[0][2] == board [1][1] and board[0][2] == board [2][0]:
                    return board[1][1]
    return None    
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    if actions(board) is None:
        return True
    return False    



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    if winner(board) == "O":
        return -1
    return 0       
def minimax(board):
   """
   Returns the optimal action for the current player on the board.
   """ 
   auxiliaryBoard = board
   print(auxiliaryBoard)
   if terminal(auxiliaryBoard):
       return None   
   if player(auxiliaryBoard) == "O" and not terminal(auxiliaryBoard):
       for action in actions(auxiliaryBoard):
           print("new try")
           minvalue = math.inf
           value = minimaxCalculate(result(auxiliaryBoard,action), 0, False)
           if value < minvalue:
               bestMove = action      
               
   else:
       for action in actions(board):
           maxvalue = -math.inf
           value = minimaxCalculate(result(auxiliaryBoard,action), 0, True)
           if value > maxvalue:
               bestMove = action        
   return bestMove  
 
def minimaxCalculate(auxiliaryBoard, depth, isMaximizingPlayer):
   if terminal(auxiliaryBoard):
       return utility(auxiliaryBoard)
   elif isMaximizingPlayer and not terminal(auxiliaryBoard):
       bestVal = -math.inf
       for action in actions(auxiliaryBoard):
           currentBoard = auxiliaryBoard
           value = minimaxCalculate(result(currentBoard,action), depth+1, False)
           bestVal = max(bestVal, value)
       return bestVal
   else:
       bestVal = math.inf
       for action in actions(auxiliaryBoard):
           currentBoard = auxiliaryBoard
           value = minimaxCalculate(result(currentBoard,action), depth+1, True)
           bestVal = min(bestVal, value)
       return bestVal

