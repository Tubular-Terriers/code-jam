import uuid
from re import T


class EntityManager:

    def __init__(self, map, renderer) -> None:
        self.renderer = renderer
        self.map = map
        self.entities = {}

    def parse(self, map=None):
        name_map = {"o": "obstacle", "p": "player", "h": "health", "b": "ball"}
        try:
            for row in range(len(self.map)):
                for type, intervals in self.map[row].items():
                    for int in intervals:
                        self.add(name_map[type], type, int[0], row, int[1] - int[0])
        except Exception as e:
            print(e)
            return False
        self.renderer.entities = self.entities
        return True

    def add(self, name, type, x, y, width) -> bool:
        try:
            _uuid = uuid.uuid4()
            self.entities[str(_uuid)] = {
                "name": name,
                "type": type,
                "x": x,
                "y": y,
                "w": width,
            }
        except Exception as e:
            print(e)
            return False
        return True

    def remove(self, uuid) -> bool:
        try:
            del self.entities[uuid]
        except Exception as e:
            print(e)
            return False
        return True

    def update(self, uuid, updates: dict) -> bool:
        for key in updates.keys():
            try:
                self.entities[uuid][key] = updates[key]
            except Exception as e:
                print(e)
                return False
        return True

    def get_entities(self) -> dict:
        return self.entities
