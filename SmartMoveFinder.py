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


def findBestMove1(gs, validMoves, returnQueue): #Helper def
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    # findMoveMinMax(gs, validMoves, settings.DEPTH, gs.whiteToMove)
    # findMoveNegaMax(gs, validMoves, settings.DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, settings.DEPTH - 1, -settings.CHECKMATE, settings.CHECKMATE, 1 if gs.whiteToMove else -1)
    returnQueue.put(nextMove)

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

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -settings.CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMove()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == settings.DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    #Move ordering - implement later
    maxScore = -settings.CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMove()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == settings.DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #Pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


#Positive score --> good for white; negative score --> good for black
def scoreBoard(gs):
    score = 0
    if gs.checkMate:
        if gs.whiteToMove:
            return -settings.CHECKMATE #Black wins
        else:
            return settings.CHECKMATE #White wins
    elif gs.staleMate:
        return settings.STALEMATE
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                #Score it positionally
                piecePositionScore = 0
                if square[1] != 'K': #No position table for king
                    if square[1] == 'p':
                        piecePositionScore = settings.piecePositionScores[square][row][col] #For pawns
                    else:
                        piecePositionScore = settings.piecePositionScores[square[1]][row][col] #For the other pieces (except the king)

                if square[0] == 'w':
                    score += settings.pieceScore[square[1]] + piecePositionScore*.1
                elif square[0] == 'b':
                    score -= settings.pieceScore[square[1]] +piecePositionScore*.1
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

'''
The overall explanation of this file (in order):
1st: We code findRandomMove in order to let AI make a totally random move. This results in some "stupid" moves because it is randomly selected.

2nd: We code findBestMove. This is when the AI can think about "materials" (each piece has its value (coded in scoreMaterial and scoreBoard))
which means AI can do moves that captured other pieces for its advantage. However, this code can only loop twice (means think 2 moves in advanced) 
--> not efficient

3rd: We code findMoveMinMax and findBestMoveMinMax. The findMoveMinMax is used to calculate the best possible score that an AI can do 
(which results in points rather than the move). Therefore we need findBestMoveMinMax in order to make the move.
How does the MinMax algorithm work?
For example we have a tree:
                        A
                B              C
           D(3)   E(-2)    F(1)  G(0)
The algorithm runs like this.
Lets say it is black's turn to move. Black's goal is to make the number as negative as possible (whereas white needs the points to be as positive as possible).
With the depth of 2, the points for move D, E, F, G are 3; -2; 1; 0 respectively. With the goal of making the number as small as possible:
    On the B branch: We have 3 > -2 --> B = -2
    On the C branch: We have 1 > 0 --> C = 0
    On the A branch: We have 0 > -2 --> A = -2
    Result: with the situation A, black will choose B to move.
This tree only has the depth of 2. However, when it reaches to the depth of 3 --> the code is very slow.
In conclusion: MinMax algorithm's goal is to "minimize the maximum's opponent's score.
But the computer can't stimulate the tree into n depth --> we need something else to reduce the code.

4rd: We code findMoveNegaMax. The same as the 3rd step, we still need to use findBestMoveMinMax (now it is names as findBestMove) in order to convert the move.
Similar to MinMax, however, MinMax algorithm needs 2 recursions: 1 for min and 1 for max. 
For NegaMax (negative max), we will see that both sides want to "maximize". 
Therefore, instead of making 2 recursions, we only just need 1 and then add "-" to switch to the opponent's.
For example, if white makes a move that marks as +5 --> black will receive -5 (which is bad for black). Therefore, black need to increase the number. For example increase to -2
Then for white, it will be switched back to 2. Then white tries to increase (increase until reached settings.CHECKMATE).
Another situation will be like this: if black makes a move that results in 2 --> white will have -2 (which is bad for white). Then white have to increase again.
In conclusion, instead of using both sides: positive and negative numbers, NegaMax will try both sides increase to  + settings.CHECKMATE
However, the code is still slow.

5th: We cod findMoveNegaMaxAlphaBeta.
What is Alpha Beta pruning?
Alpha is the variable stands for the best score for white, whereas beta is the variable stands for the best score for black.
For white, it alpha >= beta --> no need to explore further. (The code stops)
For black, it is the same but everything is change (-beta <= - alpha) since black needs to be as negative as possible. (since we implement the NegaMax).
'''
