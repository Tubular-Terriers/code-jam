import pyperclip


class ClipboardManager:
    def __init__(self) -> None:
        pass

    def get_clipboard(self):
        try:
            return pyperclip.paste()
        except Exception:
            return ""

    def set_clipboard(self, text):
        try:
            return pyperclip.copy(text)
        except Exception:
            return ""


# Usage example
# clpmng = ClipboardManager()
# print(clpmng.set_clipboard("heyyo"))
# print(clpmng.get_clipboard())
