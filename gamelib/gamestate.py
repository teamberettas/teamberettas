from pubsub import Publisher
from gamelib import utils

class GameState(utils.Subscribable):
    def start(self): pass
    def tick(self, dt): pass
    def draw(self): pass
