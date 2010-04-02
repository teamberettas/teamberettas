import pyglet
from gamelib import constants

class BaseItem(pyglet.sprite.Sprite):
    IMAGE = None
    WEIGHT = 1 

    def __init__(self):
        img = pyglet.resource.image(self.IMAGE)
        pyglet.sprite.Sprite.__init__(self, img)
        
    def get_abs_pos(self):
        return [pos - anchor for pos, anchor in zip(self.position, (self.image.anchor_x, self.image.anchor_y))]
        
    def clear(self):
        self.batch = self.group = None
        
    def tick(self, dt):
        pass
    
