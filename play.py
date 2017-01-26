'''
Runs the chess board and has high-level logic for
promotion and en passant 
'''
from textio import *
from chesslogic import * #not needed, but makes dependencies clear
blankBoard = [[Square((i,j)) for i in range(8)] for j in range(8)]
blankBoard[0][E] = King((E,0),WHITE)
blankBoard[0][A] = Rook((A,0),WHITE)
blankBoard[0][H] = Rook((H,0),WHITE)
blankBoard[7][G] = Queen((G,7),BLACK)
dispBoard(blankBoard,WHITE)
choosePiece(blankBoard,WHITE)
