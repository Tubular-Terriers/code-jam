import re

import markdown as md


class MarkdownManager:
    def __init__(self, path="/srv/code-jam/devlog/README.md"):
        self.path = path

    def parse(self, path=None):
        if path is None:
            path = self.path

        rm = open(path, "r")
        file = md.markdown(rm.read())
        contents = re.split(r"<h1>[a-zA-Z0-9\s]*<\/h1>\n", file)[1:]
        headers = re.findall(r"<h1>[a-zA-Z0-9\s]*<\/h1>\n", file)
        return (contents, headers)
