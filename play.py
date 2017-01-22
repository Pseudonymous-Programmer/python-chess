'''
Runs the chess board and has high-level logic for
promotion and en passant 
'''
#from chesslogic import *
from textio import *
dispBoard(STARTINGBOARD,True)
castle(False,True,STARTINGBOARD)
dispBoard(STARTINGBOARD,True)
