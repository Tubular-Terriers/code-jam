import pymunk


def border(x1, y1, x2, y2):
    return pymunk.Segment(None, (x1, y1), (x2, y2), radius=4)


def wall(x1, y1, x2, y2):
    return pymunk.Segment(None, (x1, y1), (x2, y2), radius=2)
