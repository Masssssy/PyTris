WINDOW_TITLE = "Python Tetris "

import pygame
from pygame.locals import *
import random


class TetrisBlock:
    blocktype = random.randint(0, 6)
    print blocktype

    active = True

    #toprobabydo add different textures and sizes
    texture = pygame.image.load("ball.png")

    #A class representing a tetris block
    def __init__(self, posX, posY):
        self.pos = (posX, posY)

    def move(self):
        self.pos = (self.pos[0], self.pos[1]+1)

    def getPos(self):
        return self.pos

    def setPos(self, posX, posY):
        self.pos = (posX, posY)




class GameMain():
    """game Main. entry point. handles intialization of game and graphics, as well as game loop."""
    done = False
    color_bg = Color('darkgrey')  # or also: Color(50,50,50) , or: Color('#fefefe')

    def __init__(self, width=400, height=600):
        """Initialize PyGame window.
        
        variables:
            width, height = screen width, height
            screen = main video surface, to draw on
            
            fps_max = framerate limit to the max fps
            limit_fps = boolean toggles capping FPS, to share cpu, or let it run free.
            now = current time in Milliseconds. ( 1000ms = 1second)
        """
        pygame.init()
        #Better random
        random.seed();



        posX = 10
        posY = 10
        self.tetris_blocks = []
        self.tetris_blocks.append(TetrisBlock(posX, posY))
        self.tetris_blocks.append(TetrisBlock(150, posY))


        # save w, h, and screen
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode(( self.width, self.height ))
        pygame.display.set_caption(WINDOW_TITLE)

        # fps clock, limits max fps
        self.clock = pygame.time.Clock()
        self.limit_fps = True
        self.fps_max = 40

        self.time = 0;

    def main_loop(self):
        """Game() main loop."""
        while not self.done:
            self.handle_events()
            self.update()
            self.draw()

            # cap FPS if: limit_fps == True
            if self.limit_fps:
                self.clock.tick(self.fps_max)
            else:
                self.clock.tick()

    def draw(self):
        """draw screen"""
        self.screen.fill(self.color_bg)

        #Render all tetris blocks
        for tetris_block in self.tetris_blocks:
            self.screen.blit(tetris_block.texture, (tetris_block.pos[0],tetris_block.pos[1]))

        # draw your stuff here. sprites, gui, etc....        

        pygame.display.flip()

    def update(self):
        """move guys."""
        self.now = pygame.time.get_ticks()

        print self.now
        #Move the active tetris block
        if self.now > 500:
            for tetris_block in self.tetris_blocks:
                    if tetris_block.active == True:
                        tetris_block.move();
            self.now = 0;





    def handle_events(self):
        """handle events: keyboard, mouse, etc."""
        events = pygame.event.get()
        kmods = pygame.key.get_mods()

        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
            # event: keydown
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.done = True

    def moveActiveBlock(self, tetris_block):
        print 1


if __name__ == "__main__":
    game = GameMain()
    game.main_loop()




