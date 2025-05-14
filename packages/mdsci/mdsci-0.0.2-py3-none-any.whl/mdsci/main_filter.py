from pandocfilters import toJSONFilter
from mdsci.core import process_filter
from mdsci.filters import *

def main():
    return toJSONFilter(apply_filters)

def apply_filters(key, value, format, meta):
    """Main entry for filters."""
    if key == 'Str':
        result = process_filter(value, format, meta)
        if result is not None:
            return result
    return None

if __name__ == "__main__":
    main()