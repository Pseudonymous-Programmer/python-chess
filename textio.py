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

def choosePiece(board,color):
    '''
    takes hooman input to choose a piece with valid moves
    '''
    dispBoard(board,color)
    colorLambda = lambda piece: piece.occupied and piece.white == color
    pieces = filterPieces(board,colorLambda)
    validMoves = lambda piece: findLegalMoves(piece.location,board) != []
    pieces = list(filter(validMoves,pieces))
    squares = [printLocation(i.location) for i in pieces]
    print("Movable Pieces:")
    for i in squares:
        print(i)
    valid = False
    while(not valid):
        choice = input('Choose a valid piece: ')
        if(choice in squares):
            valid = True
    location = pieces[squares.index(choice)].location
    return(location)

def getMove(board,coords):
    piece = board[coords[1]][coords[0]]
    castles = []
    if(isinstance(piece,King)):
        color = piece.white
        castles = validCastles(color,board)
        for castle in castles:
            print(["Queenside castle available (type Q)","Kingside castle available (type K)"][castle])
    print("Valid squares:")
    moves = findLegalMoves(piece)
    for move in moves:
        printLocation(move)
    valid = False
