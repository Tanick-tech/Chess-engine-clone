class GameState():
    def __init__(self):
        #board is a 8x8 2d list, each element of the list has 2 characters (1st: color; 2nd: type)
        #'--' represents an empty space with no piece
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
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
        self.enpassantPossible = () #Coordinates for the square where an enpassant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible] #Building a list for undo purposes (creating a new GameState for enpassant when every move is made so when we can easily undo the move)
        self.currentCastlingRight = CastleRights(True, True, True, True)
        # Creating a list of self.currentCastlingRight (later for undo purposes), and each turns will be recorded as 1 piece of data in order to recognise the changes
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        

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

        #Pawn promotion
        if move.isPawnPromotion == True:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #Enpassant move
        if move.isEnpassantMove == True:
            self.board[move.startRow][move.endCol] = '--' #Capturing the pawn

        #Update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #Only on 2 square pawn advances. Abs: absolute value
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
        self.enpassantPossibleLog.append(self.enpassantPossible)

        #Castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #Kingside castle move
                self.board[move.endRow][5] = self.board[move.endRow][7] #Moves the rook
                self.board[move.endRow][7] = '--' #Erase old rook
            else: #Queenside castle move
                self.board[move.endRow][3] = self.board[move.endRow][0] #Moves the rook
                self.board[move.endRow][0] = '--' #Erase old rook

        #Update castling rights - whenever a rook or a king move
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs,self.currentCastlingRight.bqs))
        self.updateCastleRights(move)

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
            #Undo the enpassant move:
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #Landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossibleLog.pop()
            self.enpassantPossible  =self.enpassantPossibleLog[-1]


            #Undo castling moves
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # Kingside castle move
                    self.board[move.endRow][7] = self.board[move.endRow][5]  # Moves the rook
                    self.board[move.endRow][5] = '--'  # Erase old rook
                else:  # Queenside castle move
                    self.board[move.endRow][0] = self.board[move.endRow][3]  # Moves the rook
                    self.board[move.endRow][3] = '--'  # Erase old rook

            # Undo castling rights
            # 1. Save current rights FIRST
            self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
            # 2. THEN update rights
            self.updateCastleRights(move)

            self.checkMate = False
            self.stateMate = False




    #Update the castle rights given the move
    '''
    Rules for castling:
    1. Neither the king nor the rook involved has moved before. Even if they return to their original squares, castling is no longer allowed.
    2. No pieces between the king and rook. The path must be completely clear.
    3. The king is not currently in check.
    4. The king cannot move through or land on a square under attack. For example, if an enemy bishop controls one of the squares the king would cross, castling is illegal.
    5. Only one rook can be used per castling move. You choose either kingside or queenside, not both.
    If one of these rules are broken then the flag for that castling side (king side and queen side) will be switched to False (else will always be True).
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wk':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bk':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #Left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #Right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #Left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #Right rook
                    self.currentCastlingRight.bks = False
        rights = {
                "wqs": (7, 0, "wR", [(7, 1)]),  # White queenside rook at a1, check b1 empty
                "bqs": (0, 0, "bR", [(0, 1)]),  # Black queenside rook at a8, check b8 empty
                "wks": (7, 7, "wR", []),  # White kingside rook at h1
                "bks": (0, 7, "bR", []),  # Black kingside rook at h8
            }
        for side, (row, col, rook, blockers) in rights.items():
            if self.board[row][col] != rook or any(self.board[r][c] != '--' for r, c in blockers):
                setattr(self.currentCastlingRight, side, False)
            else:
                setattr(self.currentCastlingRight, side, True)
    '''
    Meaning of the code (starts at the 'rights' attribute):
    if self.board[7][1] != '--' or self.board[7][0] != 'wR':
        self.currentCastlingRight.wqs = False
    else:
        self.currentCastlingRight.wqs = True
    if self.board[0][1] != '--' or self.board[0][0] != 'bR':
        self.currentCastlingRight.bqs = False
    else:
        self.currentCastlingRight.bqs = True
    if self.board[7][7] != 'wR':
        self.currentCastlingRight.wks = False
    else:
        self.currentCastlingRight.wks = True
    if self.board[0][7] != 'bR':
        self.currentCastlingRight.bks = False
    else:
        self.currentCastlingRight.bks = True
    '''






    #All moves considering checks
    def getValidMove(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) #Copy the current castling rights
        # The algorithm:
        # 1) Generate all the possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        # 2) For each move, make the move
        for i in range (len(moves) - 1, -1, -1): #When removing from a list go backwards through that list
            self.makeMove(moves[i])
            # 3) Generate all opponent's moves
            # 4) For each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) # 5) If they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: #Either checkmate or statemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        # 5) If they do attack your king, not a valid move
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves
    '''
            We need to delete the element of the list backward.
            Reason: For example:
            nums = [0, 1, 2, 3, 3, 4, 5]
            for num in  nums:
                if num == 3:
                    nums.remove(num)
            Then this code will run to the first 3 in the 'nums' list and delete that 3 --> nums = [0, 1, 2, 3, 4, 5]
            But the num is showing the indexing number of that list (which is at the 3rd position, which is now the 2nd 3)
            Then it will jump to the 4th position in the new list (which is number 4 in 'nums') --> skip the remaining 3 --> BUG 
            '''

    #Determine if the current player is in check
    def inCheck (self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # Determine if the enemy can attack the square r, c (means the king's position)
    def squareUnderAttack (self,r,c):
        self.whiteToMove = not self.whiteToMove #Switch to opponent's turn
        oopMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #Switch turns black
        for move in oopMoves:
            if move.endRow == r and move.endCol == c: #Square is under attack
                return True
        return False


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
            if r-1 >= 0 and self.board[r-1][c] == '--': #1 square on advance
                moves.append(Move((r, c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))

            if c - 1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #There is an enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r-1,c-1), self.board, isEnpassantMove= True))
            if c + 1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c+1), self.board, isEnpassantMove= True))

        else: #Black pawn moves
            if self.board[r+1][c] == '--': #1 square move
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2 ][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))
            #Captures
            if c - 1 >= 0: #Capture to the left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1), self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+1,c-1), self.board, isEnpassantMove= True))

            if c + 1 <= 7: #Capture to right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1), self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1,c+1), self.board, isEnpassantMove= True))



    def getRookMoves(self, r, c, moves):
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
        knightMoves = ((-2, -1),(-2,1), (-1, -2), (-1,2),(1,-2),(1,2),(2,-1),(2,1)) #Move in Ls
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
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


    #Generate all valid castle moves for the king at (r,c) and add them to the list of moves
    def getCastleMoves (self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return #Can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves (r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if c+2 < len(self.board[r]):
            if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
                if not self.squareUnderAttack (r, c+1) and not self.squareUnderAttack(r, c+2):
                    moves.append(Move((r,c), (r, c+2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves):
        if c - 3 >= 0:
            if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3]:
                if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                    moves.append(Move((r,c),(r,c-2), self.board, isCastleMove= True))


                    
                    

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

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False, pawnLeap = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = ((self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7))
        self.isCapture = self.pieceCaptured != '--'
        '''
        Why add pawn promotion in here but not in the def getPawnMoves?
        1st: In the getPawnmoves we need to deal with 6 different types of pawns (pawns do 1 square advance, pawn to 2 square advance, capturing (x2 due to 2 two colours: white and black))
        2nd: Since dealing with all those different types of pawns --> do 6 times the PawnPromotion (however we only need 1 line of code in this def
        '''
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #Castle move
        self.isCastleMove = isCastleMove


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    #Overriding the str() function
    def __str__(self):
        #Castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
            "O-O" #King side castle
            "O-O-O" #Queen side castle

        endSquare = self.getRankFile(self.endRow, self.endCol)
        #Pawn moves
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + 'X' + endSquare
            else:
                return endSquare
        #Pawn promotion
        if self.isPawnPromotion:
            return self.getChessNotation() + "--> Q"


        #Also adding + for a check move, and # for a checkmate move

        #Piece moves
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs