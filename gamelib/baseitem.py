import pyglet
from gamelib import constants

class BaseItem(pyglet.sprite.Sprite):
    IMAGE = None
    def __init__(self):
        img = pyglet.resource.image(self.IMAGE)
        pyglet.sprite.Sprite.__init__(self, img)
        
    def clear(self):
        self.batch = self.group = None
        
    def tick(self, dt):
        pass
    
