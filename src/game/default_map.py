# Exports default map
from ._objects import wall

data = [
    wall(0, 0, 0, 600),
    wall(0, 0, 600, 0),
    wall(600, 0, 600, 600),
    wall(0, 600, 600, 600),
]
