"""
simple printing functions for console-based testing
"""
from chesslogic import *
import os

def printlocation(location):
    return 'ABCDEFGH'[location[0]] + str(location[1] + 1)


def dispboard(board, perspective):
    for y in range(len(board) - 1 if perspective else 0,
                   # flips board if you're white because it's at the "top" of the array
                   -1 if perspective else len(board),
                   -1 if perspective else 1):
        column = board[y]
        for piece in column:
            print(piece,end=" ")
        print()


def choosePiece(board, color):
    '''
    takes human input to choose a piece with valid moves
    '''
    dispboard(board, color)
    pieces = filterPieces(board, lambda piece: piece.occupied and piece.white == color)
    pieces = list(filter(lambda piece: findLegalMoves(piece.location, board) != [], pieces))
    squares = [printlocation(i.location) for i in pieces]
    print("Movable Pieces:")
    for i in squares:
        print(i)
    while True:
        choice = input('Choose a valid piece: ')
        if choice in squares:
            location = pieces[squares.index(choice)].location
            return location


def getMove(board, coords):
    piece = board[coords[1]][coords[0]]
    castles = []
    if (isinstance(piece, King)):
        color = piece.white
        castles = validCastles(color, board)
        for castle in castles:
            print(('Queenside castle available (type Q)', 'Kingside castle available (type K)')[castle])
    print('Valid squares:')
    moves = findLegalMoves(coords, board)
    squares = [printlocation(i) for i in moves]
    for square in squares:
        print(square)
    while True:
        inp = input("Choose a valid move: ")
        if inp == 'K' or inp == 'Q':
            return [-1, [piece.white, inp == 'Q']]
        elif inp in squares:
            return [coords, moves[squares.index(inp)]]


def getPlayerMove(board,color):
    os.system('clear')
    location = choosePiece(board,color)
    move = getMove(board,location)
    return(move)


def getPieceType():
    nameDict = {'Queen':Queen,'Bishop':Bishop,'Knight':Knight,'Rook':Rook}
    print("Choose one to promote to: (first letter is fine)")
    for key in nameDict:
        print(key)
    choice = ''
    keys = list(nameDict.keys())
    tokens = [i[0] for i in keys]
    while True:
        choice = input()
        symbol = choice[0].upper()
        if(symbol in tokens):
            return nameDict[keys[tokens.index(symbol)]]

def promptEnPassant(passants):
    print("Avaialable en passants (n for no): ")
    for passant in passants:
        print(["Left (l)","Right (r)"][passant])
    while True:
        choice = input()
        if(choice == 'l'):
            return False
        elif(choice == 'r'):
            return True
        elif(choice == 'n'):
            return None
    
