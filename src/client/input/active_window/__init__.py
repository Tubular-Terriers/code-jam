# determines whether to import linux or windows
import ctypes
import os
import platform
import time


def is_focused():
    return get_window_pid(platform.system()) == init_pid


def pid_on_start():
    return get_window_pid(platform.system())


def get_window_pid(system):
    if system == "Linux":
        return int(
            os.popen(
                "xprop -id `xdotool getwindowfocus` | grep '_NET_WM_PID' | grep -oE '[[:digit:]]*$'"
            ).read()
        )

    elif system == "Windows":
        pid = ctypes.wintypes.DWORD()
        active = ctypes.windll.user32.GetForegroundWindow()
        return int(
            ctypes.windll.user32.GetWindowThreadProcessId(active, ctypes.byref(pid))
        )


init_pid = pid_on_start()
