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
        self.moveFunctions = {'p': self.getPawnMoves,
                              'R': self.getRookMoves,
                              'N': self.getKnightMoves,
                              'B': self.getBishopMoves,
                              'Q': self.getQueenMoves,
                              'K': self.getKingMoves} #Creating a dictionary for the moves


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
        moves = []
        for r in range(len(self.board)): #Number of rows
            for c in range(len(self.board[r])): #Number of columns in given row
                turn = self.board[r][c][0] #To access the first variable of the board (white/black)
                if (turn=='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #Calls the appropriate move function based on piece type
        return moves

    # Get all the pawn moves for the pawn located ar row, col and add these moves to the list
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #White pawn moves
            if self.board[r-1][c] == '--': #1 square on advance
                moves.append(Move((r, c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))

            if c - 1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #There is an enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c + 1 < 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: #Black pawn moves
            if self.board[r+1][c] == '--': #1 square move
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))
            #Captures
            if c - 1 >= 0: #Capture to the left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1), self.board))

            if c + 1 <= 7: #Capture to right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1), self.board))


    def getRookMoves(self, r, c, moves):
        directions = ((-1,0), (1,0), (0,-1), (0,1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #On board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': #Empty space valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else:
                        break
                else: #Off board
                    break


    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1),(-2,1), (-1, -2), (-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #Not an ally piece (empty of enemy piece)
                    moves.append(Move((r,c), (endRow,endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,1), (1,-1), (1,1)) #4 diagonals
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range (1, 8): #Bishop can move max of 7 squares
                endRow = r + d[0] * i
                endCol = r + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #is it on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': #Empty space valid
                        moves.append(Move((r,c),(endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #Enemy piece valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else: #Friendly piece invalid
                        break
                else: #Off board
                    break


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r,c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1, 0), (-1, 1), (0, -1), (0,1), (1,-1), (1,0), (1,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range (8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #Not an ally piece (empty of enemy piece)
                    moves.append(Move((r,c), (endRow,endCol), self.board))

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