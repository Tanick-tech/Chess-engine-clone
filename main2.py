import pygame as p
import engine2
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
    gs = engine2.GameState() # create game state
    validMoves = gs.getValidMove()
    moveMade = False #Glad variable for when a move is made
    loadImages()
    running = True
    sqSelected =() #No squares is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] #Keep track of the player clicks

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    move = engine2.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () #Reset user clicks
                        playerClicks = []
                    else:
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
        if moveMade:
            validMoves = gs.getValidMove()
            moveMade = False
        drawGameState(screen, gs)   # <-- draw board + pieces here
        clock.tick(settings.MAX_FPS)
        p.display.flip()


#Responsible for all the graphics within a current game state.
def drawGameState(screen,gs):
    drawBoard(screen) #Draw squares on the board
    #Add in piece highlighting or move suggestions
    drawPieces(screen, gs.board)
    #The order in this (board first and pieces later) determines the layer of these 2 variables (the board and pieces)

#Draw the squares on the board. The top left square is always light
def drawBoard(screen):
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




if __name__ == '__main__': #Whut the hell?
    main()