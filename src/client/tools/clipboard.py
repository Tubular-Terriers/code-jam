import pyperclip


class ClipboardManager:
    def __init__(self) -> None:
        pass

    def get_clipboard(self):
        return pyperclip.paste()

    def set_clipboard(self, text):
        return pyperclip.copy(text)


# Usage example
# clpmng = ClipboardManager()
# print(clpmng.set_clipboard("heyyo"))
# print(clpmng.get_clipboard())
