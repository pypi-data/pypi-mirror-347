from pathlib import Path

def get_css_path(css_style="mdsci"):
    """Get the CSS file path after installation."""
    return str(Path(__file__).parent / "styles" / f"{css_style}.css")

__all__ = ["get_css_path"]