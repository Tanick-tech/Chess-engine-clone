import random
import settings


'''
The goal for each sides:
For white pieces: get the score as high as possible (positive numbers)
For black pieces: get the score as low as possible (negative numbers)
'''
def findRandomMove(validMoves): #validMoves in this case is just the parameter for this def
    return validMoves[random.randint(0, len(validMoves)-1)]

#Find the best move based on material alone (greedy solution)
def findBestMove(gs, validMoves): #Helper method to make first recursive call (can only do with depth 2)
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore =  settings.CHECKMATE #Minimize opponents' maximum score (which is the white piece)
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMove()
        if gs.staleMate:
            opponentMaxScore = settings.STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -settings.CHECKMATE
        else:
            opponentMaxScore = -settings.CHECKMATE
            for opponentsMove in opponentsMoves: #opponentsMove: stopping condition. This loop is to generate the opponents' moves.
                gs.makeMove(opponentsMove)
                gs.getValidMove()
                if gs.checkMate:
                    score = settings.CHECKMATE
                elif gs.staleMate:
                    score = settings.STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove #Helper method to make


def findBestMoveMinMax(gs, validMoves): #Helper def
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, settings.DEPTH, gs.whiteToMove)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove): #The true minmax algorithm (with recursion happening)
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -settings.CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMove()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == settings.DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore


    else:
        minScore = -settings.CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMove()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == settings.DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


#Positive score --> good for white; negative score --> good for black
def scoreBoard(gs):
    score = 0
    if gs.checkmate:
        if gs.whiteToMove:
            return -settings.CHECKMATE #Black wins
        else:
            return settings.CHECKMATE #White wins
    elif gs.stalemate:
        return settings.STALEMATE
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += settings.pieceScore[square[1]]
            elif square[0] == 'b':
                score -= settings.pieceScore[square[1]]
    return score

#Score the board based on material
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += settings.pieceScore[square[1]]
            elif square[0] == 'b':
                score -= settings.pieceScore[square[1]]
    return score
