'''
Runs the chess board and has high-level logic for
promotion
'''
from textio import *
from chesslogic import * #not needed, but makes dependencies clear
def getPlayerMove(board,color):
    location = choosePiece(board,color)
    move = getMove(board,location)
    return(move)
blankBoard = [[ Square((i,j)) for i in range(8)]for j in range(8)]
blankBoard[6][E] = Pawn((E,6),BLACK)
blankBoard[0][E] = King((E,0),BLACK)
blankBoard[4][D] = Pawn((D,4),WHITE)
blankBoard[4][F] = Pawn((F,4),WHITE)
move = getPlayerMove(blankBoard,BLACK)
dispBoard(checkEnPassant(blankBoard,move)[0][1],BLACK)
dispBoard(checkEnPassant(blankBoard,move)[1][1],BLACK)
