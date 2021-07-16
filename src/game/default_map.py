# Exports default map
import random

from ._objects import border, wall

cor1x = [102, 360, 58 , 412, 489, 231, 409, 535, 146]
cor1y = [55, 177 , 186, 298, 0  , 186, 385, 406, 494]
cor2x = [234, 489, 230, 546, 489, 231, 409, 535, 146]
cor2y = [55, 177 , 186, 298, 180, 320, 561, 540, 600]

data = [
    # Borders (arena border)
    border(0, 0, 0, 600),
    border(0, 0, 600, 0),
    border(600, 0, 600, 600),
    border(0, 600, 600, 600),
    # Inner
    wall(cor1x[0], cor1y[0], cor2x[0], cor2y[0]),
    wall(cor1x[1], cor1y[1], cor2x[1], cor2y[1]),
    wall(cor1x[2], cor1y[2], cor2x[2], cor2y[2]),
    wall(cor1x[3], cor1y[3], cor2x[3], cor2y[3]),
    wall(cor1x[4], cor1y[4], cor2x[4], cor2y[4]),
    wall(cor1x[5], cor1y[5], cor2x[5], cor2y[5]),
    wall(cor1x[6], cor1y[6], cor2x[6], cor2y[6]),
    wall(cor1x[7], cor1y[7], cor2x[7], cor2y[7]),
    wall(cor1x[8], cor1y[8], cor2x[8], cor2y[8]),
]
