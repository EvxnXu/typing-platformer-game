import sys, os

def resource_path(relative_path):
    """Find the absolute path to a resource, works for PyInstaller and dev."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path
