'''
simple printing functions for console-based testing
'''
from chesslogic import *
def printLocation(location):
    chars = 'ABCDEFGH'
    return(chars[location[0]] + str(location[1]+1))


def dispBoard(board,perspective): 
    chars = [['■','□'],['♚','♔'],['♛','♕'],['♜','♖'],['♝','♗'],['♞','♘'],['♟','♙']]#most normal people have light-on-dark consoles. Just NOT the color operations if I'm wrong though
    direction = -1 if perspective else 1
    for y in range(len(board)-1 if perspective else 0, #flips board if you're white because it's at the "top" of the array
                   -1 if perspective else len(board),
                   -1 if perspective else 1):
        column = board[y]
        pending = ''
        for x,piece in enumerate(column):
            if(isinstance(piece,King)):
                pending += chars[1][not piece.white]
            elif(isinstance(piece,Queen)):
                pending += chars[2][not piece.white]
            elif(isinstance(piece,Rook)):
                pending += chars[3][not piece.white]
            elif(isinstance(piece,Bishop)):
                pending += chars[4][not piece.white]
            elif(isinstance(piece,Knight)):
                pending += chars[5][not piece.white]
            elif(isinstance(piece,Pawn)):
                pending += chars[6][not piece.white]
            else:
                pending += chars[0][(x+y)%2==0]
            pending += ' '
        print(pending)
