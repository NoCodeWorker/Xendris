from pathlib import Path

def get_app_config_dir():
    """Return the platform-appropriate application config directory path."""
    home = Path.home()
    return str(home / ".config" / "myapp")
