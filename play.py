'''
Runs the chess board and has high-level logic for
promotion and en passant
'''
from textio import *
from chesslogic import * #not needed, but makes dependencies clear
def doPlayerMove(board,color):
    location = choosePiece(board,color)
    move = getMove(board,location)
    return(do(move,board))
newboard = doPlayerMove(STARTINGBOARD,WHITE)
dispBoard(newboard,WHITE)
