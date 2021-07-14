import webbrowser


class BrowserManager:
    def __init__(self) -> None:
        pass

    def open_browser(self, url):
        webbrowser.open_new_tab(url)


# Usage example
# brwmng = BrowserManager()
# brwmng.open_browser("www.helloworld.com")
