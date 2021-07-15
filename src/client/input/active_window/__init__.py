# determines whether to import linux or windows
import os
import platform
import time
from ctypes import byref, windll, wintypes


def is_focused():
    return get_window_pid(platform.system()) == init_pid


def pid_on_start():
    return get_window_pid(platform.system())


def get_window_pid(system):
    if system == "Linux":
        try:
            return int(
                os.popen(
                    "xprop -id `xdotool getwindowfocus` | grep '_NET_WM_PID' | grep -oE '[[:digit:]]*$'"
                ).read()
            )
        except Exception:
            return None

    elif system == "Windows":
        try:
            pid = wintypes.DWORD()
            active = windll.user32.GetForegroundWindow()
            return int(windll.user32.GetWindowThreadProcessId(active, byref(pid)))
        except Exception:
            return None


init_pid = pid_on_start()
