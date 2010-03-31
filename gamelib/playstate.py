from pubsub import Publisher
import pyglet

#import levels, menu, gamestate, constants
from gamelib import gamestate, constants, levels

class PlayState(gamestate.GameState):
    def __init__(self, window):
        gamestate.GameState.__init__(self)
        self.Window = window
        self.Status = []
        
        self.Subscriptions = (
            (self.onLevelEnded, "level.ended"),
            (self.onLevelsDone, "level.nomore"),
        )
        self.subscribe()
        
    def onLevelEnded(self, message):
        level = message.data
        self.Status.append(level)
        level.clear()
        self.Levels.Next()
        
    def onLevelsDone(self, message):
        pyglet.text.Label("That's a wrap!", x=100, y=450, font_size=30, batch=constants.tilebatch, group=constants.overlaygroup)
        for i, level in enumerate(self.Status):
            won = level.isWon()
            pyglet.text.Label("Level %s (%s): %s" % (i+1, level.Name, {True: "Won!", False: "Lost :'("}[won]),
                              x=100, y=400-i*25,
                              batch=constants.tilebatch,
                              group=constants.overlaygroup,
                              color=(200*(not won), 200*won, 0, 255),
                              )
        
    def start(self):
        self.Levels = levels.LevelList(self.Window)
        self.Levels.Next()
        
    def tick(self, dt):
        self.Levels.tick(dt)
        
    def draw(self):
        self.Levels.draw(self)
