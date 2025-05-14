MDSCI_FILTERS = {}

def register_filter(keyword, handler):
    if keyword in MDSCI_FILTERS:
        raise ValueError(f"Filter ';;{keyword}' already registered")
    MDSCI_FILTERS[keyword] = handler

def get_filter(keyword):
    return MDSCI_FILTERS.get(keyword)

def process_filter(value, format, meta):
    import re
    # Match styles:
    #     ;;keyword{args}
    #     ;;keyword{args, key1=value1, key2=value2, ...}
    match_args = re.match(r';;(\w+)\{(.+?)\}', value)
    if match_args:
        keyword, args_str = match_args.groups()
        filter = get_filter(keyword)
        if filter:
            args = []
            kwargs = {}
            for part in args_str.split(','):
                part = part.strip()
                if '=' in part:
                    k, v = part.split('=', 1)
                    kwargs[k.strip()] = v.strip()
                else:
                    args.append(part)
            return filter(*args, format=format, meta=meta, **kwargs)
    return None