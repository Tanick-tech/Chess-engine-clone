'''
While we already have the "checking for checks" in the engine.py already, those code blocks are still expensive
The algorithm runs on generating all the possible moves of the opposing team (which is a lot since there will be only 1 or a few pieces going to check the king's square)
Therefore this is another way to "check for checks (by generating pins of the squares and directions depending on the king itself.
However, I will not implement these codes into the main one, I will just write out here (which will be run in main2.py)
Literal speaking, the way the code runs that are being showed on the user's interface is basically the same as main.py
'''
class GameState():
    def __init__(self):
        #board is a 8x8 2d list, each element of the list has 2 characters (1st: color; 2nd: type)
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
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves,
                              'N': self.getKnightMoves, 'B': self.getBishopMoves,
                              'Q': self.getQueenMoves, 'K': self.getKingMoves} #Creating a dictionary for the moves
        self.whiteToMove = True
        self.movelog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = () #Square where enpassant capture can happen
        ''''#Castling rights
        self.whiteCastleKingside = True
        self.whiteCastleQueenside = True
        self.blackCastleKingside = True
        self.blackCastleQueenside = True
        self.castleRightsLog = [CastleRights(self.whiteCastleKingside, self.blackCastleKingside, self.whiteCastleQueenside, self.blackCastleQueenside)]'''

#This def will not work for castling, pawn promotion and en passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) #Log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #Swap players
        #Update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow,move.endCol)
        #If pawn moves twice, next move can capture enpassant
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.endRow + move.startRow)//2, move.endCol)
        else:
            self.enPassantPossible = ()
        #If an enpassant move, must update the board to capture the pawn
        if move.enPassant:
            self.board[move.startRow][move.endCol] = '--'
        #If pawn promotion change piece
        if move.pawnPromotion:
            promotedPiece = input('Promote to Q, R, B, or N:')
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece
        '''#Update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.whiteCastleKingside, self.blackCastleKingside, self.whiteCastleQueenside, self.blackCastleQueenside))
        #Castle moves
        if move.castle:
            if move.endCol - move.startCol == 2: #kingside
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] #Move the rook
                self.board[move.endRow][move.endCol + 1] = '--' #Empty space where rook was
            else: #Queen side
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] #Move the rook
                self.board[move.endRow][move.endCol - 2] = '--' #Empty space where rook was'''


    #Undo the last move made
    def undoMove(self):
        if len(self.movelog) != 0: #There is a move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Switch turns back
            # Update the king's location if undo
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            #Undo enpassant is different from engine.py
            if move.enPassant:
                self.board[move.endRow][move.endCol] = '--' #Removes the pawn that was added in the wrong square
                self.board[move.startRow][move.endCol] = move.pieceCaptured #Puts the pawn back on the correct square it was captured
                self.enPassantPossible = (move.endRol, move.endCol) #Allow an enpassant to happen on the next move
            #Undo a 2 square pawn advance should make enPassantPossible = () again
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()
            #Give back castle rights if move took them away
            '''self.castleRightsLog.pop()
            castleRights = self.castleRightsLog[-1]
            self.whiteCastleKingside = castleRights.wks
            self.blackCastleKingside = castleRights.bks
            self.whiteCastleQueenside = castleRights.wqs
            self.blackCastleQueenside = castleRights.bqs'''
    def getValidMove(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsandChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation [1]
        if self.inCheck:
            if len(self.checks) == 1: #Only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                #To block a check, we must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0] #Check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #Enemy piece causing the check
                validSquares = [] #Squares that pieces can move to
                #If knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range (1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i) #check[2] and check[3] are the check direction
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #Once you get to piece end checks
                            break
                #Get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1): #Go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'K': #Move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: #Move doesn't block check or capture piece
                            moves.remove(moves[i])
            else: # Double check, king has to move
                self.getKingMoves (kingRow, kingCol, moves)
        else: #Not in check so all moves are fine
            moves = self.getAllPossibleMoves()
        return moves

    def checkForPinsandChecks(self):
        pins = [] #Squares where the allied pinned piece is and direction pinned from
        checks = [] #Squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        #Check outward from king for pins and checks, keep track of pins
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))
        for j in range (len(directions)):
            d = directions[j]
            possiblePin = () #Reset possible pins
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == (): # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # 2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        '''
                        There are 5 possibilities here in this complex conditional
                        1) Orthogonally away from king and piece is a rook
                        2) Diagonally away from king and piece is a bishop
                        3) 1 square away diagonally from king and piece is a pawn
                        4) Any direction and piece is a queen
                        5) Any direction 1 square away and piece is a king (this is necessary to prevent a king move to a square controlled by another king
                        '''
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4<=j <=5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): #NO piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #piece blocking so pin
                                break
                        else: #Enemy piece not applying check:
                            break
                else:
                    break #Off board
        #Check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == enemyColor and endPiece[1] == 'N': #Enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks






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
        piecePinned = False
        pinDirection = ()
        for i in range (len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pinsremove(self.pins[i])
                break

        if self.whiteToMove: #White pawn moves
            if self.board[r-1][c] == '--': #1 square move
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == '--': # 2 square moves
                        moves.append(Move((r,c), (r-2,c), self.board))

            #Captures
            if c - 1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #There is an enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c + 1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: #Black pawn moves
            if self.board[r+1][c] == '--': #1 square move
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((r,c), (r+1,c), self.board))
                    if r == 1 and self.board[r+2][c] == '--': # 2 square moves
                        moves.append(Move((r,c), (r+2,c), self.board))

            #Captures
            if c - 1 >= 0: #Capture to the left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1), self.board))

            if c + 1 <= 7: #Capture to right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1), self.board))


    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range (len(self.pins) -1, -1, -1):
            piecePIned = True
            pinDirection = (self.pins[i][2], self.pins[i][3])
            if self.board[r][c][1] != 'Q': #Can't remove queen from pin on rook moves, only remove it on bishop moves
                self.pins.remove(self.pins[i])
            break
        directions = ((-1,0), (1,0), (0,-1), (0,1)) #Up, left, down, right
        '''
        The reason in directions we have 0 is that when we don't click on that piece, it will not move (since 0 * n = 0)
        '''
        enemyColor = 'b' if self.whiteToMove else 'w'
        '''
        It is equivalent to the 4 following lines of codes
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'
        '''
        for d in directions: #directions is acting as a library
            for i in range (1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: #On board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
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
        '''
        The "break' code means it will break that scenario, but jump directly to a new scenario of the 'for' loop
        '''


    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            piecePinned = True
            pinDirection = (self.pin[i][2], self.pins[i][3])
            self.pins.remove(self.pins[i])
            break
        knightMoves = ((-2, -1),(-2,1), (-1, -2), (-1,2),(1,-2),(1,2),(2,-1),(2,1)) #Move in Ls
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #Not an ally piece (empty of enemy piece)
                        moves.append(Move((r,c), (endRow,endCol), self.board))


    def getBishopMoves(self, r, c, moves): #Pretty the same as the rook, except for the fact that directions are changed
        directions = ((-1,-1), (-1,1), (1,-1), (1,1)) #4 diagonals
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range (1, 8): #Bishop can move max of 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
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



'''
Instead of manually generating all the opposing possible moves (like in engine.py). We need to track both the kings' squares in order to check checks and all the 8 directions that towards the king.
Illustration:
SE      S       SW
E   the king    W
NE      N       NW
Key: SE: southeast  S: south    SW: southwest   E: east     W: west     NE: northeast   N: north    NW: northwest
To check this, we need to call 3 variables

This block of code that runs for checking checks runs on 3 variables: incheck, pin and check
    1st: Incheck
This is the variable that basically check for checks the king directly and naturally.
    2nd: Pin
If that piece is moved which later cause the check --> that piece can't move (which is called a pin)
Example:
['bR','bN','bB','--','bK','bB','bN','bR'],
['bp','bp','--','bp','bp','bp','bp','bp'],
['--','--','--','--','--','--','--','--'],
['--', 'bQ', '--', '--', '--', '--', '--', '--'],
['--', '--', 'wN', '--', '--', '--', '--', '--'],
['--', '--', '--', '--', '--', '--', '--', '--'],
['wp', 'wp', 'wp', '--', 'wp', 'wp', 'wp', 'wp'],
['wR', '--', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]. In this scenario, the wN acts like a pin (since moving it will cause a check --> wN can't move or the bQ must be eaten
However, pin will not work for Knights --> write the code that specifically for Knights (since Knight can jump over pieces)
    3rd: Check
This is a list of incheck variables. This will be used in case of a double check
Example
['bR','bN','bB','--','bK','bB','bN','bR'],
['bp','bp','bp','bp','bp','bp','bp','bp'],
['--','--','--','--','--','--','--','--'],
['--', '--', '--', '--', '--', '--', '--', 'bQ'],
['--', '--', '--', '--', '--', '--', '--', '--'],
['--', '--', '--', '--', '--', '--', '--', '--'],
['wp', 'wp', 'wp', 'wp', 'wp', '--', 'bN', 'wp'],
['wR', 'wN', 'wB', 'wQ', 'wK', '--', '--', 'wR']]. In this scenario, the only way is to move the wK since there are bQ and bN checking at the same time.
'''
