import re
from typing import Dict, List


class MapManager:
    def __init__(self) -> None:
        self.levels, self.intervals = [{}, {}]

    def set_level(self, level, map):
        # map = """
        # -----oooo-oo-oooo---
        # --ppp-----o--oo--o--"""
        try:
            self.levels[level] = {"map": map}
        except Exception as e:
            print(e)
            return False
        return True

    def get_raw_level(self, level):
        return self.intervals[level]

    def generate(
        self, level=0
    ):  # generate random map, even tho not random for the moment
        pass

    def parse(self, level=0) -> List[dict]:
        map = self.levels[level]["map"]
        intervals = []
        assets = ["o+", "p+", "h+", "b"]
        col = 0

        # map is generated row by row for the simplicity of stdout
        for row in map.split("\n"):
            if not row:
                continue

            row = row.strip()
            # print(row)
            self.levels[level]["w"] = len(row)
            intervals.append(dict())
            for a in assets:
                dummy = []
                _type = ""
                for match in re.finditer(a, row):
                    dummy.append(match.span())
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


# Example of usage

# mapmng = MapManager()
# print(mapmng.set_level(0, """
#        -----oooo-oo-oooo---
#        --ppp-----o--oo--o--"""
#                       ))
# mapmng.parse(0)
# print(mapmng.set_level(1, """-ooo-oooooooooooooooo-oooo-p"""))
# mapmng.parse(1)
# print(mapmng.get_raw_level(1))
