from types import SimpleNamespace

# fmt: off
VOID               = 0b00000  # noqa: E221
BORDER             = 0b00000  # noqa: E221
WALL               = 0b00001  # noqa: E221
BOUNDING_BOX       = 0b00010  # noqa: E221
BALL               = 0b00100  # noqa: E221
BALL_COLLISION_BOX = 0b01000  # noqa: E221
HITBOX             = 0b10000  # noqa: E221

MASK = SimpleNamespace()

MASK.VOID               = VOID  # noqa: E221
MASK.BORDER             = BORDER  # noqa: E221
MASK.WALL               = BOUNDING_BOX | BALL  # noqa: E221
MASK.BOUNDING_BOX       = WALL  # noqa: E221
MASK.BALL               = WALL | BALL_COLLISION_BOX | HITBOX | BALL  # noqa: E221
MASK.BALL_COLLISION_BOX = BALL  # noqa: E221
MASK.HITBOX             = BALL  # noqa: E221
# fmt: on
