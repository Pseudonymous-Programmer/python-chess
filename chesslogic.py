"""
By PP 2017
A simple, unoptimized chess engine
that is designed for PvP and training.
https://github.com/Pseudonynomyous-Programmer/python-chess
"""
import copy as c

WHITE = True
BLACK = False
QUEENSIDE = True
KINGSIDE = False
A, B, C, D, E, F, G, H = 0, 1, 2, 3, 4, 5, 6, 7  # useful constants


class Square:
    def __init__(self, location):
        self.occupied = False
        self.location = location
        self.moved = True

    def isAttacked(self, board, white):
        # is this square attacked by pieces of color X?
        otherPieces = filterPieces(board, lambda piece: piece.white == white)
        for piece in otherPieces:
            if (self.location in piece.generateMoves(board)):
                return True
        return False

    def __repr__(self):
        return('Square({})'.format(self.location))

    def __str__(self):
        return(['\u25A0', '\u25A1']
               [(self.location[0] + self.location[1]) % 2 == 0])


class Piece(Square):  # inheirits isAttacked function
    def __init__(self, location, color):
        self.location = location
        self.white = color
        self.occupied = True
        self.moved = False

    def move(self, location):
        self.location = location
        self.moved = True

    def snip(self, seq, board):
        """
        A simple function that takes a sorted list of moves in a row
        and returns the valid moves in that list
         - for bishops, queens and rooks.
        """
        for key, i in enumerate(seq):
            piece = board[i[1]][i[0]]
            if (piece.occupied):
                if (piece.white == self.white):
                    return (seq[:key:])
                else:
                    return (seq[:key + 1:])
        return (seq)

    def raycast(self, board, movePatterns):
        ret = []
        for i in movePatterns:
            line = []
            location = self.location
            while (True):
                location = add(i, location)
                if (location is not None):
                    line.append(location)
                else:
                    break
            ret += self.snip(line, board)
        return (ret)

    def __repr__(self):
        return("{}({},{})".format(
               type(self).__name__, self.location, self.white))


class Rook(Piece):
    movePatterns = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __str__(self):
        return (['\u265C', '\u2656'][not self.white])

    def generateMoves(self, board):
        return (self.raycast(board, self.movePatterns))


class Bishop(Piece):
    movePatterns = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

    def __str__(self):
        return (['\u265D', '\u2657'][not self.white])

    def generateMoves(self, board):
        return (self.raycast(board, self.movePatterns))


class Queen(Piece):
    movePatterns = [(1, 0), (0, 1), (-1, 0), (0, -1),
                    (1, 1), (-1, 1), (-1, -1), (1, -1)]

    def __str__(self):
        return(['\u265B', '\u2655'][not self.white])

    def generateMoves(self, board):
        return (self.raycast(board, self.movePatterns)) 


class Knight(Piece):
    def __str__(self):
        return(['\u265E', '\u2658'][not self.white])
    
    def generateMoves(self, board):
        movePatterns = [(2, -1), (-2, 1), (2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        ret = [add(self.location, i) for i in movePatterns]
        pops = []
        true = []
        for key, i in enumerate(ret):
            if (i is not None):
                piece = board[i[1]][i[0]]
                if (piece.occupied):
                    if (piece.white == self.white):
                        pops.append(key)
            else:
                pops.append(key)
        for key, i in enumerate(ret):
            if (not key in pops):
                true.append(i)
        return (true)


class Pawn(Piece):
    def __str__(self):
        return(['\u265F', '\u2659'][not self.white])
    
    def generateMoves(self, board):
        ret = []
        direction = 1 if self.white else -1
        move = add(self.location, (0, direction))
        if (move is not None):
            if (not board[move[1]][move[0]].occupied):
                ret.append(move)
        if (not self.moved and ret != []):
            move = add(self.location, (0, direction * 2))
            if (move is not None):
                if (not board[move[1]][move[0]].occupied):
                    ret.append(move)
        attacks = [(-1, direction), (1, direction)]
        for attack in attacks:
            move = add(attack, self.location)
            if (move is not None):
                piece = board[move[1]][move[0]]
                if (piece.occupied):
                    if (piece.white != self.white):
                        ret.append(move)
        return (ret)


class King(Piece):
    def __str__(self):
        return(['\u265A', '\u2654'][not self.white])
    
    def generateMoves(self, board):
        movePatterns = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        ret = []
        for i in movePatterns:
            test = add(self.location, i)
            if (test is not None):
                piece = board[test[1]][test[0]]
                if (piece.occupied):
                    if (piece.white != self.white):
                        ret.append(test)
                else:
                    ret.append(test)
        return (ret)

    def isChecked(self, board):
        return (self.isAttacked(board, not self.white))


def filterPieces(board, lmbda):
    ret = []
    for row in board:
        for piece in row:
            if (piece.occupied):
                if (lmbda(piece)):
                    ret.append(piece)
    return (ret)


def do(move, board):
    """
    Moves are [PieceLocation,PieceDestination]
    or [-1,[color,side]] for castles
    """
    copy = c.deepcopy(board)
    if (move[0] == -1):
        castle(move[1][1], move[1][0], copy)
    else:
        location, destination = move  # unwraps the move a little
        copy[destination[1]][destination[0]] = copy[location[1]][location[0]]
        copy[destination[1]][destination[0]].move(destination)
        copy[location[1]][location[0]] = Square((location[0], location[1]))
    return (copy)


def validCastles(color, board):
    rank = 0 if color else 7
    attackLambda = lambda square: square.isAttacked(board,
                                                    not color)  # is this square attacked by pieces of the opposing color?
    occupyLambda = lambda square: square.occupied  # is this square occupied
    ret = []
    valid = True
    kingSpot = board[rank][E]
    if (isinstance(kingSpot, King) and not kingSpot.moved):
        QueenRook = board[rank][A]
        if (isinstance(QueenRook, Rook) and not QueenRook.moved):
            valid = True
            for file in range(B, E):
                if (occupyLambda(board[rank][file])):
                    valid = False
            for file in range(A, F):
                if (attackLambda(board[rank][file])):
                    valid = False
            if (valid):
                ret.append(QUEENSIDE)
        KingRook = board[rank][H]
        if (isinstance(KingRook, Rook) and not KingRook.moved):
            valid = True
            for file in range(F, H):
                if (occupyLambda(board[rank][file])):
                    valid = False
            for file in range(E, H + 1):
                if (attackLambda(board[rank][file])):
                    valid = False
            if (valid):
                ret.append(KINGSIDE)
    return (ret)


def castle(color, side, board):
    """
    True is queenside,
    false is kingside
    """
    rank = 0 if color else 7
    if (side):
        board = do([(E, rank), (C, rank)], board)
        board = do([(A, rank), (D, rank)], board)
    else:
        board = do([(E, rank), (G, rank)], board)
        board = do([(H, rank), (F, rank)], board)
    return (board)


def findLegalMoves(location, board):
    piece = board[location[1]][location[0]]
    color = piece.white
    location = piece.location
    ret = []
    for move in piece.generateMoves(board):
        testBoard = do([location, move], board)
        if (not filterPieces(testBoard,
                             lambda piece: piece.white == color and isinstance(piece, King)
                             )[0].isChecked(testBoard)):
            ret.append(move)
    return (ret)


def add(coord1, coord2):
    """
    A 'smart' tuple adder that checks that it's on the chessboard
    """
    ret = tuple([coord1[i] + coord2[i] for i in range(len(coord1))])
    for i in ret:
        if (i < 0 or i > 7):
            return (None)
    return (ret)


def allValidMoves(color, board):
    pieces = filterPieces(board, lambda piece: piece.white == color)
    ret = []
    for piece in pieces:
        ret += findLegalMoves(piece.location, board)
    return (ret)


def checkEnPassant(board, move): #this code hurts me
    location = move[0]
    destination = move[1]
    piece = board[location[1]][location[0]]
    ret = []
    if (isinstance(piece, Pawn)):  # is it a pawn
        if (not piece.moved):  # who hasn't moved yet
            direction = 1 if piece.white else -1
            if (add(location, (0, 2 * direction)) == destination):  # but now is moving two squares
                rank = 3 if piece.white else 4  # rank enemy pawns need to be on
                files = [location[0] - 1, location[0] + 1]  # files they need to be on
                for key, file in enumerate(files):
                    try:
                        if (isinstance(board[rank][file], Pawn) and  # is the board at that spot
                                    board[rank][file].white != piece.white):  # a pawn, and is it 'evil'?
                            copy = c.deepcopy(board)
                            copy[location[1]][location[0]] = Square(location)  # the pawn dies
                            copy = do([(file, rank), (location[0], location[1] + direction)], copy)
                            ret.append([bool(key), copy])
                    except IndexError:
                        pass  # catches bad files - not very good programming, but it's easy
    return (ret)


def doEnPassant(board,move,side,color): # as with all other "move" functions,this just blindly does it and requires a move generator
    location = move[0]
    direction = 1 if color else -1
    board = do([location,add(location,(0,direction))],board)
    offset = 1 if side else -1
    board = do([add(location,(offset,direction*2)),add(location,(0,direction))])
    return(board)

    
def checkPromotion(board, color):
    rank = 7 if color else 0
    filterLambda = lambda square: isinstance(square, Pawn) and square.location[1] == rank
    pieces = filterPieces(board, filterLambda)
    return (pieces[0].location if len(pieces) else None)  # there should only be one promotable pawn


def isCheckmated(board, color):
    moves = allValidMoves(color, board)
    if (moves == [] and filterPieces(board, lambda piece: isinstance(piece, King) and piece.white == color)[0]):
        king = filterPieces(board, lambda piece: isinstance(piece, King) and piece.white == color)[0]
        if (king.isChecked(board)):
            return (True)
    return (False)


def isStalemated(board, color):
    moves = allValidMoves(color, board)
    if (moves == [] and filterPieces(board, lambda piece: isinstance(piece, King) and piece.white == color)[0]):
        king = filterPieces(board, lambda piece: isinstance(piece, King) and piece.white == color)[0]
        if (not king.isChecked(board)):
            return (True)
    return (False)


def promote(board,location,kind):
    copy = c.deepcopy(board)
    copy[location[1]][location[0]] = kind(location,copy[location[1]][location[0]].white)
    return(copy)


STARTINGBOARD = [
    [Rook((0, 0), True), Knight((1, 0), True), Bishop((2, 0), True), Queen((3, 0), True), King((4, 0), True),
     Bishop((5, 0), True), Knight((6, 0), True), Rook((7, 0), True)],
    [Pawn((i, 1), True) for i in range(8)],
    [Square((i, 2)) for i in range(8)],
    [Square((i, 3)) for i in range(8)],
    [Square((i, 4)) for i in range(8)],
    [Square((i, 5)) for i in range(8)],
    [Pawn((i, 6), False) for i in range(8)],
    [Rook((0, 7), False), Knight((1, 7), False), Bishop((2, 7), False), Queen((3, 7), False), King((4, 7), False),
    Bishop((5, 7), False), Knight((6, 7), False), Rook((7, 7), False)]]

blankBoard = [[Square((i, j)) for i in range(8)] for j in range(8)]
