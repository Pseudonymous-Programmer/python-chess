'''
By Thomas Neil 2017
A simple, unoptimized chess engine
that is designed for PvP and training.
https://github.com/Thomas-Neill/python-chess
'''
from textio import *
class Piece:
    def __init__(self,location,color):
        self.location = location
        self.white = color
        self.occupied = True
        self.moved = False
    def move(self,location):
        self.location = location
        self.moved = True
    def generateMoves(self,board):
        '''
        Returns a list of tuples for valid moves
        '''
        assert False,"Subclass Piece, you idiot"
    def snip(self,seq,board):
        '''
        A simple function that takes a sorted list of moves in a row and returns the valid moves in that list
         - for bishops, queens and rooks.
        '''
        for key, i in enumerate(seq):
            piece = board[i[1]][i[0]]
            if(piece.occupied):
                if(piece.white == self.white):
                    return(seq[:key:])
                else:
                    return(seq[:key+1:])
        return(seq)


class Empty:
    def __init__(self):
        self.occupied = False


class Rook(Piece):
    def generateMoves(self,board):
        ret = []
        movePatterns = [(1,0),(0,1),(-1,0),(0,-1)]
        for i in range(4):
            line = []
            location = self.location
            while(True):
                location = add(movePatterns[i],location)
                if(location is not None):
                    line.append(location)
                else:
                    break
            ret += self.snip(line,board)
        return(ret)


class Bishop(Piece): #reusable code,bruh
    def generateMoves(self,board):
        ret = []
        movePatterns = [(1,1),(-1,1),(-1,-1),(1,-1)]
        for i in range(4):
            line = []
            location = self.location
            while(True):
                location = add(movePatterns[i],location)
                if(location is not None):
                    line.append(location)
                else:
                    break
            ret += self.snip(line,board)
        return(ret)


class Queen(Piece):
    def generateMoves(self,board):
        ret = []
        movePatterns = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
        for i in range(4):
            line = []
            location = self.location
            while(True):
                location = add(movePatterns[i],location)
                if(location is not None):
                    line.append(location)
                else:
                    break
            ret += self.snip(line,board)
        return(ret)

class Knight(Piece):
    def generateMoves(self,board):
        movePatterns = [(2,-1),(-2,1),(2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)]
        ret = [add(self.location, i) for i in movePatterns]
        pops = []
        true = []
        for key,i in enumerate(ret):
            if(i is not None):
                piece = board[i[1]][i[0]]
                if(piece.occupied):
                    if(piece.white == self.white):
                        pops.append(key)
            else:
                pops.append(key)
        for key,i in enumerate(ret):
            if(not key in pops):
                true.append(i)
        return(true)

class Pawn(Piece):
    def generateMoves(self,board):
        ret = []
        direction = 1 if self.white else -1
        move = add(self.location,(0,direction))
        if(move is not None):
            if(not board[move[1]][move[0]].occupied):
                ret.append(move)
        if(not self.moved and ret != []):
            move = add(self.location,(0,direction*2))
            if(move is not None):
                if(not board[move[1]][move[0]].occupied):
                    ret.append(move)
        attacks = [(-1,direction),(1,direction)]
        for attack in attacks:
            move = add(attack,self.location)
            if(move is not None):
                piece = board[move[1]][move[0]]
                if(piece.occupied):
                    if(piece.white != self.white):
                        ret.append(move)
        return(ret)
    
class King(Piece):
    def generateMoves(self,board):
        movePatterns = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        ret = []
        for i in movePatterns:
            test = add(self.location,i)
            if(test is not None):
                piece = board[test[1]][test[0]]
                if(piece.occupied):
                    if(piece.white != self.white):
                        ret.append(test)
                else:
                    ret.append(test)
        return(ret)
    def isChecked(self,board):
        otherPieces = filterPieces(board,lambda piece: piece.white != self.white)
        for piece in otherPieces:
            if(self.location in piece.generateMoves(board)):
                return(True)
        return(False)

def filterPieces(board,lmbda):
    ret = []
    for row in board:
        for piece in row:
            if(piece.occupied):
                if(lmbda(piece)):
                    ret.append(piece)
    return(ret)

def do(move,board):
    '''
    Moves are [PieceLocation,PieceDestination]
    '''
    copy = board[:]
    location,destination = move #unwraps the move a little
    copy[destination[1]][destination[0]] = copy[location[1]][location[0]]
    copy[location[1]][location[0]]  = Empty()
    return(copy)


def findLegalMoves(location,board):
    piece = board[location[1]][location[0]]
    color = piece.white
    location = piece.location
    ret = []
    for move in piece.generateMoves(board):
        testBoard = do([location,move],board)
        if(not filterPieces(testBoard,
                            lambda piece: piece.white == color and isinstance(piece,King)
                            )[0].isChecked(board)):
            
            ret.append(move)
    return(ret)
                    
def newBoard(move,board):
    '''
    Takes a "move" tuple formatted like this:
    Location, Location that piece is to be moved to
    '''
    cpBoard = board[:]
    piece = board[move[0][1]][move[0][0]]
    cpBoard[move[1][1]][move[1][0]] = piece
    cpBoard[move[0][1]][move[0][0]] = Empty()
    return(cpBoard)

def add(coord1,coord2):
    '''
    A 'smart' tuple adder that checks that it's on the chessboard
    '''
    ret = tuple([coord1[i] + coord2[i] for i in range(len(coord1))])
    for i in ret:
        if(i < 0 or i > 7):
            return(None)
    return(ret)

STARTINGBOARD = [
    [Rook((0,0),True),Knight((1,0),True),Bishop((2,0),True),Queen((3,0),True),King((4,0),True),Bishop((5,0),True),Knight((6,0),True),Rook((7,0),True)],
    [Pawn((i,1),True) for i in range(8)],
    [Empty() for i in range(8)],
    [Empty() for i in range(8)],
    [Empty() for i in range(8)],
    [Empty() for i in range(8)],
    [Pawn((i,6),False) for i in range(8)],
    [Rook((0,7),False),Knight((1,7),False),Bishop((2,7),False),Queen((3,7),False),King((4,7),False),Bishop((5,7),False),Knight((6,7),False),Rook((7,7),False)]
    ]
if(__name__ == '__main__'):
    print('Debugging!')
    printBoard(STARTINGBOARD,True)
    print(findLegalMoves((0,1),STARTINGBOARD))
    
