import ure as re

R_SPLITTER = r'\/'
R_START = r'^'
R_PARAM = r'(\w*)'
R_FILENAME = r'(\/[a-zA-Z0-9_\.]+\.+[a-zA-Z0-9_]+)?'
R_END = r'$'

r_splitter = re.compile(R_SPLITTER)


def build(path: str, start: bool = True, end: bool = True):
    chunks = r_splitter.split(path)

    built = ''

    if start:
        built += R_START

    route_params = []

    for chunk in chunks:
        if chunk == '':
            continue

        if chunk.startswith(':'):
            content = R_PARAM
            route_params.append(chunk[1:])
        else:
            content = chunk

        built += R_SPLITTER + content

    built += R_FILENAME

    if end:
        built += R_END

    return built, route_params


def parse_path(string):
    # split path from query params and bookmark
    chunks = string.split('?', 1)

    path = chunks[0] if len(chunks) > 0 else None
    query = chunks[1] if len(chunks) > 1 else None
    bookmark = None

    if query:
        # split query params from bookmark
        chunks = query.split('#')
        query = chunks[0] if len(chunks) > 0 else None
        bookmark = chunks[1] if len(chunks) > 1 else None

        if query:
            query = parse_query(query)

    return path, query, bookmark


def parse_query(string: str):
    # split single params
    chunks = string.split('&')

    query = {}

    # parse query params to name, value
    for chunk in chunks:
        qparam = chunk.split('=')
        if len(qparam) > 1:
            query[qparam[0]] = qparam[1]

    return query
