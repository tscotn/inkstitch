import os
import sys
from os.path import dirname, realpath

import psutil
from whichcraft import which


def get_bundled_dir(name):
    if getattr(sys, 'frozen', None) is not None:
        return realpath(os.path.join(sys._MEIPASS, "..", name))
    else:
        return realpath(os.path.join(dirname(realpath(__file__)), '..', '..', name))


def get_resource_dir(name):
    if getattr(sys, 'frozen', None) is not None:
        return realpath(os.path.join(sys._MEIPASS, name))
    else:
        return realpath(os.path.join(dirname(realpath(__file__)), '..', '..', name))


def get_inkscape():
    # Inkscape 1.0 puts itself in the PATH to ensuire we can find it.
    inkscape = which("inkscape")
    if inkscape is not None:
        return inkscape

    # For earlier versions, let's go fishing.
    for pid in psutil.pids():
        try:
            exe = psutil.Process(pid).exe()
            if os.path.basename(exe).lower.startswith("inkscape"):
                return exe
        except psutil.Error:
            pass

    return None
