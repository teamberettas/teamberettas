import pyglet
from pubsub import Publisher
from gamelib import utils, teeter, fallingobjects, constants, pipe

class LevelList(object):
    def __init__(self, window):
        self.Window = window
        self.Levels = [FirstLevel]
        self.CurrentLevel = -1
        self.Level = None
        self.PlayedLevels = []
        
    def Next(self):
        self.CurrentLevel += 1
        if self.CurrentLevel < len(self.Levels):
            self.Level = self.Levels[self.CurrentLevel](self.Window)
            self.Level.Number = self.CurrentLevel + 1 # Use 1-based here.
            Publisher.sendMessage("level.started", self.Level)
            self.PlayedLevels.append(self.Level)
        else:
            self.Level = None
            Publisher.sendMessage("game.over", self.PlayedLevels)
    
    def tick(self, dt):
        self.Level.tick(dt)
        
    def draw(self, parent):
        self.Level.draw(parent)

class BaseLevel(utils.Subscribable):
    def __init__(self, window, name, duration, background):
        self.Window = window
        self.Background = pyglet.resource.image(background)
        self.Name = name
        self.Duration = self.TimeLeft = duration
        self.Won = False
        self.Instruction = None

        self.Teeter = teeter.Teeter()
        self.Pipe = pipe.Pipe()
        self.ObjectQueue = []
        self.CurrentObject = None
        
        self.Subscriptions = []
        self.subscribe()
        
    def setInstruction(self, instruction):
        if self.Instruction:
            self.Instruction.stop()
        self.Instruction = instruction
        if self.Instruction: # Can pass None.
            self.Instruction.start()
        
    def clear(self):
        self.unsubscribe()
        self.setInstruction(None)
        
    def isWon(self):
        return self.Won
    
    def retry(self):
        self.TimeLeft = self.Duration
        self.Complete = False
        
    def nextObject(self):
        if not self.ObjectQueue:
            self.Won = True
            Publisher.sendMessage("level.ended", self)
        else:
            nextObj = self.ObjectQueue.pop(0)
            nextObj.position = (self.Pipe.x, constants.RESOLUTION[1])
            self.CurrentObject = nextObj
        
    def tick(self, dt):
        self.Teeter.tick(dt)
        self.Pipe.tick(dt)

        # Figure out what to do with the queue of objects.
        if self.CurrentObject is None:
            self.nextObject()
                
        if self.CurrentObject:
            self.CurrentObject.tick(dt)
            # Did the object fall of the screen?
            if self.CurrentObject.y < 0:
                # Oh no, the level is lost!
                self.CurrentObject = None
                self.Won = False
                Publisher.sendMessage("level.ended", self)
            elif self.Teeter.intersects(self.CurrentObject):
                self.Teeter.hold(self.CurrentObject)
                self.nextObject()

        if self.Instruction:
            self.Instruction.tick(dt)
    
    def draw(self, parent):
        self.Background.blit(0, 0)
        self.Teeter.draw()
        if self.CurrentObject:
            self.CurrentObject.draw()
        # Draw the pipe after the objects so they can appear to come out of the pipe.
        self.Pipe.draw()
            
        constants.tilebatch.draw()

class FirstLevel(BaseLevel):
    def __init__(self, window):
        BaseLevel.__init__(self, window, "First!", None, "bg_park.png")
        
        self.ObjectQueue = [fallingobjects.FallingWood(), fallingobjects.FallingPaper(), fallingobjects.FallingRock()]
        
        self.Instructions = (
            utils.Instruction("Welcome. Don't let the teeter totter tip!"),
        )
        self.setInstruction(self.Instructions[0])
        Publisher.subscribe(self.onInstructionComplete, "instruction.complete")
        
    def onInstructionComplete(self, message):
        instr = message.data
            
