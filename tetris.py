WINDOW_TITLE = "Python Tetris "

import pygame
from pygame.locals import *
import random
from collections import Counter

class TetrisPart:
    #A single tetris square, i.e part of a complete tetris block
    active = True
    remove = False

    #A class representing a tetris block
    def __init__(self, posX, posY, parent):
        self.pos = (posX, posY)
        self.parent = parent

        self.blocking = (0 , 0)
        #Update immediately to make sure nothing shady happens in the first timer
        #before update is run naturally
        self.update()

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

        #print self.blocking[0]
        #print self.blocking[1]

    def move(self):
            self.pos = (self.pos[0], self.pos[1]+40)

    def getBlockingX(self):
        return self.blocking[0]

    def getBlockingY(self):
        return self.blocking[1]

    def getBlockingCoord(self):
        return self.blocking[0] * self.blocking[1]

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

    def setRemoveFlag(self,x):
        self.remove = x

    def getRemoveFlag(self):
        return self.remove

    def getParent(self):
        return self.parent

class TetrisCombined:
    #A combination of squares forming an actual tetris block
    texture = pygame.image.load("block.png")
    def __init__(self):
        print "init block"

        #Create 4 parts the block consist of
        #Generate random numebr for blocktype (total 7 blocks)
        blocktype = random.randint(0, 6)

        #Get the unique id of this object
        self.id = id(self)

        self.parts = []
        #Hatch block
        if(blocktype == 0):
            self.parts.append(TetrisPart(0,-40, self.id))
            self.parts.append(TetrisPart(40,-40, self.id))
            self.parts.append(TetrisPart(0,0, self.id))
            self.parts.append(TetrisPart(0,40, self.id))
        #Straight block
        if(blocktype == 1):
            self.parts.append(TetrisPart(0,-40, self.id))
            self.parts.append(TetrisPart(40,-40, self.id))
            self.parts.append(TetrisPart(80,-40, self.id))
            self.parts.append(TetrisPart(120,-40, self.id))
        #Inverted hatch
        if(blocktype == 2):
            self.parts.append(TetrisPart(0,-40, self.id))
            self.parts.append(TetrisPart(40,-40, self.id))
            self.parts.append(TetrisPart(40,0, self.id))
            self.parts.append(TetrisPart(40,40, self.id))
        # 3 + tip
        if(blocktype == 3):
            self.parts.append(TetrisPart(0,0, self.id))
            self.parts.append(TetrisPart(40,0, self.id))
            self.parts.append(TetrisPart(80,0, self.id))
            self.parts.append(TetrisPart(40,-40, self.id))
        #Square
        if(blocktype == 4):
            self.parts.append(TetrisPart(0,-40, self.id))
            self.parts.append(TetrisPart(0,0, self.id))
            self.parts.append(TetrisPart(40,-40, self.id))
            self.parts.append(TetrisPart(40,0, self.id))
        #Squiggly 
        if(blocktype == 5):
            self.parts.append(TetrisPart(40,-40, self.id))
            self.parts.append(TetrisPart(80,-40, self.id))
            self.parts.append(TetrisPart(0,0, self.id))
            self.parts.append(TetrisPart(40,0, self.id))
        #Squiggly inverted
        if(blocktype == 6):
            self.parts.append(TetrisPart(0,-40, self.id))
            self.parts.append(TetrisPart(40,-40, self.id))
            self.parts.append(TetrisPart(40,0, self.id))
            self.parts.append(TetrisPart(80,0, self.id))


        #The block part texture
        color = random.randint(1, 4)
        print "color: " + str(color)
        if(color == 1):
            print "color 1 set"
            self.texture = pygame.image.load("block.png")
        if(color == 2):
            print "color 2 set"
            self.texture = pygame.image.load("block2.png")
        if(color == 3):
            print "color 3 set"
            self.texture = pygame.image.load("block3.png")
        if(color == 4):
            print "color 4 set"
            self.texture = pygame.image.load("block4.png")

    #Randomize block type
    blocktype = random.randint(0, 6)

    def canMoveLeftRight(self, lr, blockingSpots):
       #left = 0, right = 1
       if(lr == 0):
           for part in self.parts:
                #Check if colliding with edge, if so return false
                if(part.blocking[0] == 1):
                    return False
            #Check for collissions with already placed blocks
           for part in self.parts:
               for blockingSpot in blockingSpots:
                    if(part.getBlockingX()-1 == blockingSpot[0] and part.getBlockingY() == blockingSpot[1]):
                        return False
       elif(lr == 1):
            for part in self.parts:
                #Check if colliding with edge, if so return false
                if(part.blocking[0] == 10):
                    return False
            #Check for collissions with already placed blocks
            for part in self.parts:
               for blockingSpot in blockingSpots:
                    if(part.getBlockingX()+1 == blockingSpot[0] and part.getBlockingY() == blockingSpot[1]):
                        return False
       else:
           nextPos = ""
           print "invalid value"

       #for tetris_block in self.tetris_blocks:
       #    for part in tetris_block.getParts():
       #        if(nextPos[0] == part.getBlocking(0) and nextPos[1] == part.getBlocking(1)):
       #            return False
       return True

    def moveRight(self):
        for part in self.parts:
            #move all parts in TetrisCombined to the right
            part.right()
            part.update()
    
    def moveLeft(self):
        for part in self.parts:
            #move all parts in TetrisCombined to the right
            part.left()
            part.update()

    def getParts(self):
        return self.parts

    def setParts(self, parts):
        self.parts = parts

    def move(self):
        for part in self.parts:
            part.move()

    def update(self):
        for part in self.parts:
            part.update()

    def getTexture(self):
        return self.texture

    def getId(self):
        return self.id


class GameMain():
    """game Main. entry point. handles intialization of game and graphics, as well as game loop."""
    done = False
    color_bg = Color('white')  # or also: Color(50,50,50) , or: Color('#fefefe')
    DROPTIMEREVENT = USEREVENT + 1

    def newBlock(self):
        #Move the active block into array of blocks and create a new block to fill active_block
        self.tetris_blocks.append(self.active_block)
        #Check if rows are filled (i.e should be removed)
        self.checkRows()
        self.active_block = TetrisCombined()

    def removeLine(self, lineToRemove):
        print "remove line"
        for tetris_block in self.tetris_blocks:
            #print "tetris block " + str(tetris_block.getBlocking(0)) + ", " + str(tetris_block.getBlocking(1))
            for part in tetris_block.getParts():
                if(part.getBlockingY() == lineToRemove):
                    print "flag to remove x:" + str(part.getBlockingX()) + "y:" + str(part.getBlockingY())
                    part.setRemoveFlag(True)

#TODO THIS FUNCTION DOES NOT DELETE ALL PARTS MARKED FOR DELETION
        for tetris_block in self.tetris_blocks:
           for part in tetris_block.getParts()[::-1]:
               if(part.getRemoveFlag() == True):
                    print "actually remove  x:" + str(part.getBlockingX()) + "y:" + str(part.getBlockingY())
                    tetris_block.getParts().remove(part)

        #Row is removed move blocks above down
        moved_block = True
        while(moved_block):
            moved_block = False
            for tetris_block in self.tetris_blocks:
                for part in tetris_block.getParts():
                    if(part.getBlockingY() < lineToRemove):
                        if(self.canMove(tetris_block)):
                            print "moving block " + str(part.getBlockingX()) + ", " + str(part.getBlockingY())
                            moved_block = True
                            tetris_block.move()
                            tetris_block.update()


    def checkRows(self):
        self.blockedSpots = []
        for tetris_block in self.tetris_blocks:
            for tetris_part in tetris_block.getParts():
                self.blockedSpots.append((tetris_part.getBlockingX(), tetris_part.getBlockingY()))

        # Check amount of blocks on each line and remove "full lines"
        itemsOnLines = Counter(elem[1] for elem in self.blockedSpots)
        for line in itemsOnLines.iteritems():
              if(line[1] >= 10):
                self.removeLine(line[0])
                print "remove line"


    def canMove(self, block):
        #Next position of the active block
        for part in block.getParts():
            nextPos = (part.blocking[0], part.blocking[1]+1)
            if(nextPos[1] > 20):
                return False
            for tetris_block in self.tetris_blocks:
                for part in tetris_block.getParts():
                    #Dont check if colliding with parts in same "TetrisCombined", continue
                    if part.getParent() == block.getId():
                       continue
                    if(nextPos[0] == part.getBlockingX() and nextPos[1] == part.getBlockingY()):
                        print "false"
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

        #Init sound mixer
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)

        pygame.init()
        #Better random
        random.seed();

        #Load tetris song
        pygame.mixer.music.load("tetris.ogg")
        #pygame.mixer.music.play() #loops=-1

        self.tetris_blocks = []
        self.active_block = TetrisCombined()

        self.blockedSpots = []


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
        i = 0
        for blockPart in self.active_block.getParts():
            self.screen.blit(self.active_block.getTexture(), (blockPart.pos[0], blockPart.pos[1]))
            i += 1

        #Render all other tetris blocks
        for tetris_block in self.tetris_blocks:
            for part in tetris_block.getParts():
                self.screen.blit(tetris_block.getTexture(), (part.pos[0],part.pos[1]))

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
                    if(self.active_block.canMoveLeftRight(0,self.blockedSpots)):
                        self.active_block.moveLeft()
                    #for part in self.active_block.getParts():
                    #    if(part.blocking[0] > 1 and self.canMoveLeftRight(part, 0)):
                    #        part.left()
                    #        part.update()
                if event.key == K_RIGHT:
                    #Move block right
                    print "right pressed"
                    if(self.active_block.canMoveLeftRight(1,self.blockedSpots)):
                        self.active_block.moveRight()

                    #for part in self.active_block.getParts():
                    #    if(part.blocking[0] < 10 and self.canMoveLeftRight(part, 1)):
                    #        part.right()
                    #        part.update()

                if event.key == K_SPACE:
                    print "drop pressed"
                    #self.active_block.drop(self)
                    while (self.canMove(self.active_block)):
                        self.active_block.move()
                        self.active_block.update()
                    #When dropping a block a new one needs to be created
                    self.newBlock()
                if event.key == K_BACKSPACE:
                    self.removeLine(20)

            #If timer has passed drop time, move the active block down
            if event.type == self.DROPTIMEREVENT:
                if(self.canMove(self.active_block)):
                    self.active_block.move()
                    #Update the blocks blocking properties
                    self.active_block.update()
                else:
                    self.newBlock()

if __name__ == "__main__":
    game = GameMain()
    game.main_loop()