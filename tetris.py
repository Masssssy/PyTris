WINDOW_TITLE = "Python Tetris "

import pygame
from pygame.locals import *
import random


class TetrisBlock:
    blocktype = random.randint(0, 6)
    active = True

    #toprobabydo add different textures and sizes
    texture = pygame.image.load("block.png")

    #A class representing a tetris block
    def __init__(self):
        self.pos = (0, -40)

        #self.blocking = [(0,0), (0,0), (0,0), (0,0)]
        #Temp blocking list
        self.blocking = (0 , 0)
    def update(self):
        #calculate what squares the active block is blocking
        #X-axis
        if(self.pos[0] > 0):
            #block is at posx/40 in coordinate system
            self.blocking = ((self.pos[0] / 40) + 1, self.blocking[1])
        else:
            #block is at zero
            self.blocking = (1, self.blocking[1])


        #Y-Axis

        if(self.pos[1] > 0):
            #block is at posx/40 in coordinate system
            self.blocking = (self.blocking[0], (self.pos[1] / 40) + 1)
        else:
            #block is at zero
            self.blocking = (self.blocking[0], 1)

        print self.blocking[0]
        print self.blocking[1]

    def move(self):
            self.pos = (self.pos[0], self.pos[1]+40)

    def getBlocking(self, x):
        return self.blocking[x]

    def left(self):
        self.pos = (self.pos[0] - 40, self.pos[1])

    def right(self):
        self.pos = (self.pos[0] + 40, self.pos[1])

    def drop(self, game):
        print "drop"

    def getPos(self):
        return self.pos

    def setPos(self, posX, posY):
        self.pos = (posX, posY)

class GameMain():
    """game Main. entry point. handles intialization of game and graphics, as well as game loop."""
    done = False
    color_bg = Color('darkgrey')  # or also: Color(50,50,50) , or: Color('#fefefe')
    DROPTIMEREVENT = USEREVENT + 1

    def newBlock(self):
        #Move the active block into array of blocks and create a new block to fill active_block
        self.tetris_blocks.append(self.active_block)
        self.active_block = TetrisBlock()

    def canMove(self):
        #Next position of the active block
        nextPos = (self.active_block.blocking[0], self.active_block.blocking[1]+1)
        if(nextPos[1] > 20):
            return False
        for tetris_block in self.tetris_blocks:
            if(nextPos[0] == tetris_block.getBlocking(0) and nextPos[1] == tetris_block.getBlocking(1)):
                return False

        return True

    def __init__(self, width=400, height=800):
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

        posX = 200
        self.tetris_blocks = []
        self.active_block = TetrisBlock()


        # save w, h, and screen
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode(( self.width, self.height ))
        pygame.display.set_caption(WINDOW_TITLE)

        # fps clock, limits max fps
        self.clock = pygame.time.Clock()
        self.limit_fps = True
        self.fps_max = 40
        pygame.time.set_timer(self.DROPTIMEREVENT, 500)


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

        #Render the active block
        self.screen.blit(self.active_block.texture , (self.active_block.pos[0], self.active_block.pos[1]))
        #Render all other tetris blocks
        for tetris_block in self.tetris_blocks:
            self.screen.blit(tetris_block.texture, (tetris_block.pos[0],tetris_block.pos[1]))

        # draw your stuff here. sprites, gui, etc....        

        pygame.display.flip()

    def update(self):
        #Update the game state, positions, collisions, rows to delete etc
        self.now = pygame.time.get_ticks()


    def handle_events(self):
        """handle events: keyboard, mouse, etc."""
        events = pygame.event.get()
        kmods = pygame.key.get_mods()

        for event in events:
            #Events for key presses
            if event.type == pygame.QUIT:
                self.done = True
            # event: keydown
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.done = True
                if event.key == K_LEFT:
                    #Move block left
                    print "left pressed"
                    if(self.active_block.blocking[0] > 1):
                        self.active_block.left()
                        self.active_block.update()
                if event.key == K_RIGHT:
                    #Move block right
                    print "right pressed"
                    if(self.active_block.blocking[0] < 10):
                        self.active_block.right()
                        self.active_block.update()
                if event.key == K_SPACE:
                    print "drop pressed"
                    #self.active_block.drop(self)
                    while (self.canMove()):
                        self.active_block.move()
                        self.active_block.update()
                    #When dropping a block a new one needs to be created
                    self.newBlock()

            #If timer has passed drop time, move the active block down
            if event.type == self.DROPTIMEREVENT:
                if(self.canMove()):
                    self.active_block.move()
                    #Update the blocks blocking properties
                    self.active_block.update()
                else:
                    self.newBlock()

if __name__ == "__main__":
    game = GameMain()
    game.main_loop()




