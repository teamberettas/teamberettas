from gamelib import utils
from pubsub import Publisher

class LevelList(object):
    def __init__(self, window):
        self.Window = window
        self.Levels = [FirstLevel]
        self.CurrentLevel = -1
        self.Level = None
        
    def Next(self):
        self.CurrentLevel += 1
        if self.CurrentLevel < len(self.Levels):
            self.Level = self.Levels[self.CurrentLevel](self.Window)
            self.Level.Number = self.CurrentLevel + 1 # Use 1-based here.
            Publisher.sendMessage("level.started", self.Level)
        else:
            Publisher.sendMessage("level.nomore")
    
    def tick(self, dt):
        self.Level.tick(dt)
        
    def draw(self, parent):
        self.Level.draw(parent)

class BaseLevel(utils.Subscribable):
    def __init__(self, window, name, duration, map=None):
        self.Window = window
        self.Name = name
        self.Duration = self.TimeLeft = duration
        self.Complete = False
        self.Instruction = None
        
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
        return False
    
    def retry(self):
        self.TimeLeft = self.Duration
        self.Complete = False
        
    def tick(self, dt):
        if not self.Complete:
           pass

        if self.Instruction:
            self.Instruction.tick(dt)
    
    def draw(self, parent):
        pass

class FirstLevel(BaseLevel):
    def __init__(self, window):
        BaseLevel.__init__(self, window, "First!", None)
        
        self.Instructions = (
            utils.Instruction("Welcome! Don't let the teeter totter tip!."),
        )
        self.setInstruction(self.Instructions[0])
        Publisher.subscribe(self.onInstructionComplete, "instruction.complete")
        
    def onInstructionComplete(self, message):
        instr = message.data
            
