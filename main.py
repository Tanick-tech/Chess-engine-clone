from tarfile import version

import pygame as p
import engine
import settings


'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
       settings.IMAGES[piece] = p.transform.scale(p.image.load("image/" + piece + ".png"), (settings.SQ_SIZE, settings.SQ_SIZE))

#The main driver for our code. This will handle user input and updating the graphics
def main():
    p.init()
    screen = p.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = engine.GameState() # create game state
    validMoves = gs.getValidMove()
    moveMade = False #Flag variable for when a move is made
    animate = False #Flag variable for when we should animate a move
    loadImages()
    running = True
    gameOver = False
    sqSelected =() #No squares is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] #Keep track of the player clicks

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() #(x,y) location of the mouse
                    col = location[0]//settings.SQ_SIZE # 0 means the x variable of location
                    row = location[1]//settings.SQ_SIZE # 1 means the y variable of location
                    if sqSelected == (row, col): #The user clicked the same square --> this is the undo step
                        sqSelected = () #De-select
                        playerClicks = [] #Clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #Append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: #after 2nd click
                        move = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () #Reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                        '''
                        The reason why the sqSelected, playerClicks are 'tabbed' and another 'else' code block in is because to save the clicks
                        For instance: if we press on the queen and press on the block that is invalid a move --> just waste a click
                        Without tabbing in will affect the coordination libraries we are running behind.
                        '''
            #Undo-the-move code block
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Undo when z is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #Reset the board when 'r' is pressed
                    gs = engine.GameState()
                    validMoves = gs.getValidMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        if moveMade:
            if animate == True:
                animateMove(gs.movelog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMove()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)   # <-- draw board + pieces here

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(settings.MAX_FPS)
        p.display.flip()

#Highlight square selected and moves for piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            #Highlight selected square
            s = p.Surface((settings.SQ_SIZE, settings.SQ_SIZE))
            s.set_alpha(100) #Transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*settings.SQ_SIZE, r*settings.SQ_SIZE))
            #Highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*settings.SQ_SIZE, move.endRow*settings.SQ_SIZE))

#Responsible for all the graphics within a current game state.
def drawGameState(screen,gs, validMoves, sqSelected):
    drawBoard(screen) #Draw squares on the board
    #Add in piece highlighting or move suggestions
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    #The order in this (board first and pieces later) determines the layer of these 2 variables (the board and pieces)

#Draw the squares on the board. The top left square is always light
def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range (settings.DIMENSION):
        for c in range (settings.DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*settings.SQ_SIZE, r*settings.SQ_SIZE, settings.SQ_SIZE, settings.SQ_SIZE))



# Draw the pieces on the board using the current GameState.board
def drawPieces(screen, board):
    for r in range(settings.DIMENSION):
        for c in range (settings.DIMENSION):
            piece = board[r][c]
            if piece != "--": #Not an empty square
                screen.blit(settings.IMAGES[piece], p.Rect(c*settings.SQ_SIZE, r*settings.SQ_SIZE, settings.SQ_SIZE, settings.SQ_SIZE))

#Animating the square
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 10 #Frames to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framePerSquare
    for frame in range(frameCount+1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        #Erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*settings.SQ_SIZE, move.endRow*settings.SQ_SIZE, settings.SQ_SIZE, settings.SQ_SIZE)
        p.draw.rect(screen,color, endSquare)
        #Draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(settings.IMAGES[move.pieceCaptured], endSquare)
        #Draw moving piece
        screen.blit(settings.IMAGES[move.pieceMoved], p.Rect(c*settings.SQ_SIZE, r*settings.SQ_SIZE, settings.SQ_SIZE, settings.SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen,text):
    font = p.font.SysFont('Helvitca', 32, False, False)
    textObject = font.render(text, 0, p.Color('black'))
    textLocation = p.Rect(0, 0, settings.WIDTH, settings.HEIGHT).move(settings.WIDTH / 2 - textObject.get_width() / 2,
                                                                      settings.HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation.move(2, 2))
    textObject = font.render(text, 0, p.Color('red'))
    screen.blit(textObject, textLocation)


if __name__ == '__main__': #Whut the hell?
    main()