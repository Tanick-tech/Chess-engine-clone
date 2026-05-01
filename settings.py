#Basic board measurements
WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

#Scoring system
pieceScore = {'K': 0, 'Q': 9, 'R': 5, 'B':3, 'N': 3, 'p': 1}
CHECKMATE = 1000
STALEMATE = 0

