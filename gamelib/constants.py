OBJECT_BASE_SIZE = 40
RESOLUTION = (800, 600)
VERSION = "0.1"

import pyglet
tilebatch = pyglet.graphics.Batch()
layergroups = list(pyglet.graphics.OrderedGroup(i) for i in range(10))
overlaygroup = pyglet.graphics.OrderedGroup(len(layergroups))
