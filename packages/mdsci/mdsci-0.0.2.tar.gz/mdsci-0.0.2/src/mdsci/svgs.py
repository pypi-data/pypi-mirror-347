def draw_svg_circle(facecolor="ffffff", edgecolor="000000", html_class=None):
    """SVG code to draw a circle."""
    class_str = f' class="{html_class}"' if html_class else ''
    svg_str = (
        f'<svg{class_str} width="20" height="20">'
        f'<circle cx="10" cy="10" r="8" fill="#{facecolor}" stroke="#{edgecolor}" stroke-width="1"/>'
        '</svg>'
    )
    return svg_str