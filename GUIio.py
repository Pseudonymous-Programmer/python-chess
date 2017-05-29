import pygame
from pygame.locals import *
from chesslogic import *
import textio

SIZE = 400
TILES = 8
TILESIZE = int(SIZE/TILES)

window = pygame.display.set_mode((SIZE,SIZE))

WKING,WQUEEN,WBISHOP,WKNIGHT,WROOK,WPAWN = map(lambda surf:
                                                   pygame.transform.scale(surf,(TILESIZE,TILESIZE)).convert_alpha(),
                                               map(lambda name:
                                                   pygame.image.load("sprites/White{}.png".format(name))
                                                       ,["King","Queen","Bishop","Knight","Rook","Pawn"]))

BKING,BQUEEN,BBISHOP,BKNIGHT,BROOK,BPAWN = map(lambda surf:
                                                   pygame.transform.scale(surf,(TILESIZE,TILESIZE)).convert_alpha(),
                                                   map(lambda name:
                                                       pygame.image.load("sprites/Black{}.png".format(name)),
                                                       ["King","Queen","Bishop","Knight","Rook","Pawn"]))

def draw_checkerboard(special_spots=[]):
    for y in range(TILES):
        for x in range(TILES):
            pygame.draw.rect(window,(125,125,200) if (x,y) in special_spots else (50,50,50) if (x+y) % 2 else (255,255,255),pygame.Rect(TILESIZE*x,TILESIZE*y,TILESIZE,TILESIZE))
    pygame.display.update()

def draw(piece,location):
    def _draw(_piece):
        window.blit(_piece,(location[0]*TILESIZE,location[1]*TILESIZE))
        pygame.display.update()
    if(isinstance(piece,King)):
        _draw(WKING if piece.white else BKING)
    elif(isinstance(piece,Queen)):
        _draw(WQUEEN if piece.white else BQUEEN)
    elif(isinstance(piece,Bishop)):
        _draw(WBISHOP if piece.white else BBISHOP)
    elif(isinstance(piece,Knight)):
        _draw(WKNIGHT if piece.white else BKNIGHT)
    elif(isinstance(piece,Rook)):
        _draw(WROOK if piece.white else BROOK)
    elif(isinstance(piece,Pawn)):
        _draw(WPAWN if piece.white else BPAWN)
    
    
def dispboard(board, perspective):
    for y,row in enumerate(board):
        for x,piece in enumerate(row):
            if(perspective == WHITE):
                draw(piece,(x,7-y))
            else:
                draw(piece,(x,y))

def get_square_click():
    while(True):
        event = pygame.event.poll()
        if(not event): continue
        if(event.type == QUIT): quit()
        if(event.type == MOUSEBUTTONDOWN):
            pos = event.pos
            return (pos[0]//TILESIZE,pos[1]//TILESIZE)

def choose_square(board,choices,color):
    if(color == WHITE): #flip for displaying
        choices = list(map(lambda location:(location[0],7-location[1]),choices))
    draw_checkerboard(choices)
    dispboard(board,color)
    while(True):
        click = get_square_click()
        if(click in choices):
            if(color == WHITE): return (click[0],7-click[1]) # reinvert the location
            return click

    
def choosePiece(board, color):
    pieces = filterPieces(board, lambda piece: piece.occupied and piece.white == color and findLegalMoves(piece.location,board) != [])
    square = choose_square(board,list(map(lambda piece:piece.location,pieces)),color)
    return square


def getMove(board, coords):
    piece = board[coords[1]][coords[0]]
    if (isinstance(piece, King)):
        color = piece.white
        castles = validCastles(color, board)
        if(castles):
            for castle in castles:
                print(('Queenside castle available (type Q)', 'Kingside castle available (type K)')[castle])
            choice = input("Choose one, or just press enter for neither")
            if(choice == 'K' or choice == 'Q'):
                return [-1, [piece.white, choice == 'Q']]
    moves = findLegalMoves(coords, board)
    return [coords,choose_square(board,moves,piece.white)]


def getPlayerMove(board,color):
    location = choosePiece(board,color)
    move = getMove(board,location)
    return(move)
getPieceType,promptEnPassant = textio.getPieceType,textio.promptEnPassant
