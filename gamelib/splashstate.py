import pyglet
from pubsub import Publisher

from gamelib import gamestate

labelBatch = pyglet.graphics.Batch()

class SplashState(gamestate.GameState):
    def __init__(self, window):
        gamestate.GameState.__init__(self)
        self.Window = window
        self.bg = pyglet.resource.image("splashbg.png")
        self.ypositions = (400, 300, 200)
        self.currentSelection = 0
        
        self.newGameLabel = pyglet.text.Label("New Game", font_size=32, batch=labelBatch)
        self.exitLabel = pyglet.text.Label("Exit", font_size=32, batch=labelBatch)
        self.labels = (self.newGameLabel, self.exitLabel)
        
        for y, label in zip(self.ypositions, self.labels):
            label.x = 300
            label.y = y
        
        self.menuBullet = pyglet.sprite.Sprite(pyglet.resource.image("menubullet.png"), batch=labelBatch)
        self.menuBullet.position = (250, self.ypositions[0])
        
        self.highlight(self.currentSelection)
        
        self.Subscriptions = (
            (self.onkeypress, "keypress"),
        )
        self.subscribe()
        
    def onkeypress(self, message):
        key = int(message.topic[-1])
        if key == pyglet.window.key.DOWN:
            if self.currentSelection < 2:
                self.currentSelection += 1
        elif key == pyglet.window.key.UP:
            if self.currentSelection > 0:
                self.currentSelection -= 1
        elif key in (pyglet.window.key.ENTER, pyglet.window.key.RETURN):
            action = ("new", "exit")[self.currentSelection]
            
            Publisher.sendMessage("game.%s" % action)
            
        self.menuBullet.y = self.ypositions[self.currentSelection]
        self.highlight(self.currentSelection)
            
    def highlight(self, pos):
        for i, label in enumerate(self.labels):
            if i == pos:
                label.color = (255, 255, 255, 255)
            else:
                label.color = (122, 122, 122, 255)
                
        
    def tick(self, dt):
        pass
    
    def draw(self):
        #w, h = self.Window.width, self.Window.height
        self.bg.blit(0, 0)
        self.menuBullet.draw()
        labelBatch.draw()
        
