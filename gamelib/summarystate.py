import pyglet
from gamelib import gamestate, constants

class SummaryState(gamestate.GameState):
    def __init__(self, levels):
        gamestate.GameState.__init__(self)
        self.initialDraw(levels)
        
    def initialDraw(self, levels):
        pyglet.text.Label("That's a wrap!", x=100, y=450, font_size=30, batch=constants.tilebatch, group=constants.overlaygroup)
        for i, level in enumerate(levels):
            won = level.isWon()
            pyglet.text.Label("Level %s (%s): %s" % (i+1, level.Name, {True: "Won!", False: "Lost :'("}[won]),
                              x=100, y=400-i*25,
                              batch=constants.tilebatch,
                              group=constants.overlaygroup,
                              color=(200*(not won), 200*won, 0, 255),
                              )