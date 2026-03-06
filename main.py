import pygame as p
import engine
import settings


'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''


#The main driver for our code. This will handle user imput and updating the graphics
def main():
    p.init()
    screen = p.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = p.time.Clock()
    gs = engine.GameState()   # create game state
    font = p.font.SysFont("DejaVu Sans", settings.SQ_SIZE)               # load your Unicode chess icons

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

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
    font = p.font.SysFont("Segoe UI Symbol", settings.SQ_SIZE)
    for r in range(settings.DIMENSION):
        for c in range(settings.DIMENSION):
            piece = board[r][c]
            if piece != "--":
                symbol = settings.pieces.get(piece)
                if symbol:
                    text_surface = font.render(symbol, True, (0,0,0))
                    text_rect = text_surface.get_rect(center=(
                        c*settings.SQ_SIZE + settings.SQ_SIZE//2,
                        r*settings.SQ_SIZE + settings.SQ_SIZE//2
                    ))
                    screen.blit(text_surface, text_rect)



if __name__ == '__main__': #Whut the hell?
    main()