import pyglet
from pubsub import Publisher
from gamelib import utils, teeter, fallingobjects, constants, pipe

import data

class LevelList(object):
    def __init__(self, window):
        self.Window = window
        self.Levels = [FirstLevel,SecondLevel,ThirdLevel]
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
        pyglet.media.load(data.filepath('sound/start1.wav'), streaming=False).play()
    
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
        self.CurrentObjects = []
        self.FallPlayer = pyglet.media.load(data.filepath('sound/fall1.wav'), streaming=False)

        # self.NextObjectInQueue and self.NullObject are used to figure out the end of
        # the "next item" list and remember the position.
        self.NextObjectInQueue = fallingobjects.NullItem()
        self.NextObjectInQueue.position = (constants.RESOLUTION[0]-75, 150) 
        self.NullObject = self.NextObjectInQueue

        self.NextLabel = pyglet.text.Label("Next Item", font_size=24, bold=True, x=constants.RESOLUTION[0]-155, y=200)

        self.Subscriptions = (
            (self.onkeypress, "keypress"),
        )
        self.subscribe()

    def onkeypress(self, message):
        key = int(message.topic[-1])
        if key == pyglet.window.key.SPACE:
            if self.NextObjectInQueue != self.NullObject:
                self.nextObject()

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

    def setNextItem(self):
        if self.ObjectQueue:
            comingUpObj = self.ObjectQueue.pop(0)
            comingUpObj.position = self.NullObject.position
            self.NextObjectInQueue = comingUpObj
        else:
            self.NextObjectInQueue = self.NullObject
            self.NextLabel.text = "No more"
 
    def nextObject(self):
        self.FallPlayer.play()
        nextObj = self.NextObjectInQueue 
        nextObj.position = self.Pipe.position
        self.CurrentObjects.append(nextObj)
        self.setNextItem()
        
    def tick(self, dt):
        self.Teeter.tick(dt)
        self.Pipe.tick(dt)
                
        for obj in self.CurrentObjects:
            obj.tick(dt)
            # Did the object fall off the screen?
            if obj.y < 0:
                # Oh no, the level is lost!
                self.CurrentObjects = []
                self.Won = False
                Publisher.sendMessage("level.ended", self)
            elif self.Teeter.intersects(obj):
                self.Teeter.hold(obj)
                self.CurrentObjects.remove(obj)
                if self.NextObjectInQueue == self.NullObject and not self.CurrentObjects:
                    self.Won = True
                    Publisher.sendMessage("level.ended", self)

        if self.Instruction:
            self.Instruction.tick(dt)
    
    def draw(self, parent):
        self.Background.blit(0, 0)
        self.Teeter.draw()
        for obj in self.CurrentObjects:
            obj.draw()
        # Draw the pipe after the objects so they can appear to come out of the pipe.
        self.Pipe.draw()
        self.NextLabel.draw()
        self.NextObjectInQueue.draw()    
        constants.tilebatch.draw()

class FirstLevel(BaseLevel):
    def __init__(self, window):
        BaseLevel.__init__(self, window, "First!", None, "bg_park.png")
        
        self.ObjectQueue = [fallingobjects.FallingPaper(), fallingobjects.FallingWood()]
 
        self.Instructions = (
            utils.Instruction("Welcome. Press SPACE to release a box, but don't drop any!"),
        )
        self.setInstruction(self.Instructions[0])
        Publisher.subscribe(self.onInstructionComplete, "instruction.complete")
        
        self.setNextItem()       
 
    def onInstructionComplete(self, message):
        instr = message.data

class SecondLevel(BaseLevel):
    def __init__(self, window):
        BaseLevel.__init__(self, window, "Level 2", None, "bg_night.png")

        self.ObjectQueue = [fallingobjects.FallingBaby(), fallingobjects.FallingBaby(), fallingobjects.FallingBaby(), fallingobjects.FallingBaby()]

        self.Instructions = (
            utils.Instruction("Save the babies from the evil vampire bats!!"),
        )
        self.setInstruction(self.Instructions[0])
        Publisher.subscribe(self.onInstructionComplete, "instruction.complete")

        self.setNextItem()

    def onInstructionComplete(self, message):
        instr = message.data

            
class ThirdLevel(BaseLevel):
    def __init__(self, window):
        BaseLevel.__init__(self, window, "Level 3", None, "bg_city.png")

        self.ObjectQueue = [fallingobjects.FallingPaper(), fallingobjects.FallingPaper(), fallingobjects.FallingPaper(), fallingobjects.FallingPaper()]

        self.Instructions = (
            utils.Instruction("Clean the city!"),
        )
        self.setInstruction(self.Instructions[0])
        Publisher.subscribe(self.onInstructionComplete, "instruction.complete")

        self.setNextItem()

    def onInstructionComplete(self, message):
        instr = message.data
