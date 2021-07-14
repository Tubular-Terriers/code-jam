import re
from typing import Dict, List


class MapManager:
    def __init__(self) -> None:
        self.levels, self.intervals = [{}, {}]

    def set_level(self, level, _map):
        # map = """
        # -----oooo-oo-oooo---
        # --ppp-----o--oo--o--"""
        try:
            self.levels[level] = {"map": _map}
        except Exception as e:
            print(e)
            return False
        return True

    def get_level_size(self, level):
        return (self.levels[level]["w"], self.levels[level]["h"])

    def get_raw_interval(self, level):
        return self.intervals[level]

    def get_level(self, level):
        return self.levels[level]

    def generate(
        self, level=0
    ):  # generate random _map, even tho not random for the moment
        pass

    def parse(self, level=0) -> List[dict]:
        _map = self.levels[level]["map"]
        intervals = []
        assets = ["o+", "p+", "h+", "b"]
        col = 0

        # map is generated row by row for the simplicity of stdout
        for row in _map.split("\n"):
            if not row:
                continue

            row = row.strip()
            self.levels[level]["w"] = len(row)
            intervals.append(dict())
            for a in assets:
                dummy = []
                _type = ""
                for match in re.finditer(a, row):
                    dummy.append(list(map(lambda x: x / 5, match.span())))
                    if not _type:
                        _type = match.group()[0]
                    if not (_type in intervals[col]):
                        intervals[col][_type] = list()
                if dummy:
                    intervals[col][_type] = dummy

            col += 1

        self.levels[level]["h"] = col

        self.intervals[level] = intervals
        return intervals


# Example usage

# mapmng = MapManager()
# print(mapmng.set_level(0, """
#        -----oooo-oo-oooo---
#        --ppp-----o--oo--o--"""
#                       ))
# mapmng.parse(0)
# print(mapmng.set_level(1, """-ooo-oooooooooooooooo-oooo-p"""))
# mapmng.parse(1)
# print(mapmng.get_raw_level(1))
