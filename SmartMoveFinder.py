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
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore =  settings.CHECKMATE #Minimize opponents' maximum score (which is the white piece)
    bestPlayerMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMove()
        random.shuffle(validMoves)
        opponentMaxScore = -settings.CHECKMATE
        for opponentsMove in opponentsMoves: #opponentsMove: stopping condition
            gs.makeMove(opponentsMove)
            if gs.checkMate:
                score = -turnMultiplier * settings.CHECKMATE
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
    return bestPlayerMove



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
