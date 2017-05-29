'''
Runs the chess game and has high-level logic for
promotion
'''
from GUIio import *
from chesslogic import * #not needed, but makes dependencies clear
def playChess():
    board = STARTINGBOARD
    currentPlayer = WHITE
    while(True):
        if(isCheckmated(board,currentPlayer)):
            return(not currentPlayer)
        elif(isStalemated(board,currentPlayer)):
            return(None)
        move = getPlayerMove(board,currentPlayer)
        board = do(move,board)
        if(checkPromotion(board,currentPlayer)):
            location = checkPromotion(board,currentPlayer)
            piece = getPieceType()
            board = promote(board,location,piece)
        if(checkEnPassant(board,move)):
            passants = checkEnPassant(board,move)
            choice = promptEnPassant(passants)
            if(choice is not None):
                board = doEnPassant(board,move,choice,not currentPlayer)
                continue
        currentPlayer = not currentPlayer
if(__name__ == '__main__'):
    result = playChess()
    if(result is not None):
        print("Congradulations {} player!".format(["black","white"][result]))
    else:
        print("Tie! Good game!")
    quit()
