'''
Runs the chess board and has high-level logic for
promotion and en passant
'''
from textio import *
from chesslogic import * #not needed, but makes dependencies clear
def getPlayerMove(board,color):
    location = choosePiece(board,color)
    move = getMove(board,location)
    return(move)
def checkEnPassant(board,move):
    location = move[0]
    destination = move[1]
    piece = board[location[1]][location[0]]
    ret = []
    if(isinstance(piece,Pawn)): #is it a pawn
        if(not piece.moved): #who hasn't moved yet
            direction = 1 if piece.white else -1
            if(add(location,(0,2*direction)) == destination): #but now is moving two squares
                rank = 3 if piece.white else 4 #rank enemy pawns need to be on
                files = [location[0]-1,location[0]+1] #files they need to be on
                for key,file in enumerate(files):
                    try:
                        if(isinstance(board[rank][file],Pawn) and #is the board at that spot
                           board[rank][file].white != piece.white): #a pawn, and is it 'evil'?
                           copy = c.deepcopy(board)
                           copy[location[1]][location[0]] = Square(location) #the pawn dies
                           copy = do([(rank,file),(location[0],location[1]+direction)],copy)
                           ret.append([bool(key),copy])
                    except IndexError:
                        pass #catches bad files - not very good programming, but it's easy
    return(ret)
blankBoard = [
[ Square((i,j)) for i in range(8)]
for j in range(8)
]
dispBoard(blankBoard,WHITE)
