# Exports default map
from ._objects import border, wall

data = [
    # Borders (arena border)
    border(0, 0, 0, 600),
    border(0, 0, 600, 0),
    border(600, 0, 600, 600),
    border(0, 600, 600, 600),
    # Inner walls
    wall(50, 50, 50, 100),
]
