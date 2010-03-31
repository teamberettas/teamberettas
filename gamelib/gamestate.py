from pubsub import Publisher
from gamelib import utils

class GameState(utils.Subscribable):
    def tick(self): pass
    def draw(self): pass
