import os

def get_app_config_dir():
    """Return the platform-appropriate application config directory path."""
    home = os.path.expanduser("~")
    return os.path.join(home, ".config", "myapp")
