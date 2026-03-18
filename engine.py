class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element of the list has 2 characters (1st: color; 2nd: type)
        #'--' represents an empty space with no piece
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.whiteToMove = True
        self.movelog = []

#This def will not work for castling, pawn promotion and en passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) #Log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #Swap players

    #Undo the last move made
    def undoMove(self):
        if len(self.movelog) != 0: #There is a move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Switch turns back

    #All moves considering checks
    def getValidMove(self):
        return self.getAllPossibleMoves() #For now we will not worry about checks


    #All moves without considering checks:
    def getAllPossibleMoves(self):
        moves = [Move((6,4), (4,4), self.board)]
        for r in range(len(self.board)): #Number of rows
            for c in range(len(self.board[r])): #Number of columns in given row
                turn = self.board[r][c][0] #To access the first variable of the board (white/black)
                if (turn=='w' and self.whiteToMove) and (turn=='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
        return moves

    # Get all the pawn moves for the pawn located ar row, col and add these moves to the list
    def getPawnMoves(self, r, c, moves):
        pass

    def getRookMoves(self, r, c, moves):
        pass

class Move():
    #map keys to values
    # key : value
    ranksToRows = {"1":7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filestoCols = {"a":0,"b": 1,"c": 2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filestoCols.items()}
    '''
    The four upper lines of codes are called "dictionaries"
    That 4 codes describes the coordinates in the real chess board, however now they are now crypted with the numbers.
    '''



    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]