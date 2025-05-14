from mdsci.core import register_filter

def mdsci_filter(keyword):
    """
    Decorator to register syntax filters.
    
    Example:
    @mdsci_filter('rgb')
    def handle_rgb(color, format, **kwargs):
        ...
    """
    def decorator(func):
        register_filter(keyword, func)
        return func
    return decorator