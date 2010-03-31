import sys, pyglet
from pubsub import Publisher

from gamelib import constants

class Subscribable(object):
    def __init__(self):
        self.Subscriptions = ()
        
    def subscribe(self):
        for callback, event in self.Subscriptions:
            Publisher.subscribe(callback, event)
            
    def unsubscribe(self):
        for callback, event in self.Subscriptions:
            Publisher.unsubscribe(callback)

def clamp(val, minv, maxv=sys.maxint):
    return min((max((val, minv)),maxv))

class Instruction(object):
    def __init__(self, text):
        self.document = document = pyglet.text.document.FormattedDocument(text)
        document.set_style(0, 999, {"font_size": 18, "halign":"center"})
        self.Layout = pyglet.text.layout.TextLayout(document, 590, 600, True, group=constants.overlaygroup)
        self.Layout.x = 5
        #self.Layout.y = 500
        self.Timeout = 6
        self.FadeTime = 1.5
        self.Opacity = 0
        self.State = None
        
    def start(self):
        self.State = "FADEIN"
        self.Layout.batch = batch=constants.tilebatch
        
    def stop(self):
        """Sometimes an instruction may be stopped before its timeout."""
        self.Opacity = 0
        self.Layout.delete()
        self.State = None
        
    def setOpacity(self):
        self.document.set_style(0, 999, {"color": (255, 255, 255, int(self.Opacity))})
        
    def tick(self, dt):
        if self.State == "FADEIN":
            self.Opacity += dt / self.FadeTime * 255
            if self.Opacity >= 255:
                self.Opacity = 255
                self.State = "COUNTING"
            self.setOpacity()
        elif self.State == "COUNTING":
            self.Timeout -= dt
            if self.Timeout <= 0:
                self.State = "FADEOUT"
        elif self.State == "FADEOUT":
            self.Opacity -= dt / self.FadeTime * 255
            if self.Opacity <= 0:
                self.stop()
                Publisher.sendMessage("instruction.complete", self)
            self.setOpacity()
            
            
