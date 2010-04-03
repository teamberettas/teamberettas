'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import pyglet
from pyglet.window import key
from pubsub import Publisher

import data
pyglet.resource.path.append(data.filepath("images"))
pyglet.resource.reindex()

from gamelib import splashstate, playstate, summarystate, constants 

class Window(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, width=800, height=600, caption="Chubby Chaser v%s" % constants.VERSION)
        keys = key.KeyStateHandler()
        self.push_handlers(keys)
        self.fps = pyglet.clock.ClockDisplay()
        pyglet.clock.schedule_interval(self.tick, 1/30.0)
        
        self.State = splashstate.SplashState(self)
        Publisher.subscribe(self.onGameNew, "game.new")
        Publisher.subscribe(self.onGameOver, "game.over")
        Publisher.subscribe(self.onGameExit, "game.exit")
        
    def onGameNew(self, message):
        self.State.unsubscribe()
        self.State = playstate.PlayState(self)
        self.State.start()
        
    def onGameOver(self, message):
        levels = message.data
        if all([level.Won for level in levels]):
            pyglet.media.load(data.filepath('sound/win1.wav'), streaming=False).play()
        else:
            pyglet.media.load(data.filepath('sound/lose1.wav'), streaming=False).play()
        self.State.unsubscribe()
        self.State = summarystate.SummaryState(levels)
        self.State.start()
        
    def onGameExit(self, message):
        import sys; sys.exit()
        
    def on_key_press(self, symbol, modifiers):
        Publisher.sendMessage("keypress.%s" % symbol, modifiers)

    def tick(self, dt):
        self.State.tick(dt)
        
    def on_draw(self):
        self.clear()
        self.State.draw()
        self.fps.draw()
        
    def on_mouse_motion(self, x, y, dx, dy):
        pass
            
    def on_mouse_press(self, x, y, button, mods):
        if button == pyglet.window.mouse.LEFT:
            Publisher.sendMessage("click.left")

def main():
    #print data.load('sample.txt').read()
    w = Window()
    pyglet.app.run()

if __name__ == "__main__":
    main()
