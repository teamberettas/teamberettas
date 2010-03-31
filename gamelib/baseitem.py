import pyglet
from gamelib import constants

class BaseItem(pyglet.sprite.Sprite):
    def __init__(self, imageName):
        img = pyglet.resource.image(imageName)
        pyglet.sprite.Sprite.__init__(self, img)
        #self.scale = 2.0
        
    def clear(self):
        self.batch = self.group = None
        
    def tick(self, dt):
        pass
    
