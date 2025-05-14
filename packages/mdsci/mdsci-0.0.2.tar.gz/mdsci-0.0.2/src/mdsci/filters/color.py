from pandocfilters import RawInline, Str
from mdsci.decorators import mdsci_filter
from mdsci.svgs import draw_svg_circle
import string

@mdsci_filter('color')
def handle_color(color, format, alpha=None, **kwargs):
    """
    Filter use:
    - ;;color{rgb}
    - ;;color{rgb, alpha=...}

    Args:
        color: RGB hex color string (e.g., 'ffffff')
        alpha: transparency (0.0 to 1.0)
    
    HTML properties:
    
    - class:
      - mdsci_color
      - mdscir_color_icon
    """
    color = color.lower()
    if not all(c in string.hexdigits for c in color):
        return Str(f';;color{{{color}}}')
    
    if format == 'html':
        style = f"background-color: #{color}"
        if alpha is not None:
            style += f"; opacity: {alpha}"
        color_icon = draw_svg_circle(facecolor=color, html_class='mdscir_color_icon')
        html = f'<span class="code mdsci_color">{color_icon} #{color}</span>'
        return RawInline('html', html)
    return Str(f'#{color}')