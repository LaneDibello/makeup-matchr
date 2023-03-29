from html import unescape

def to_ascii(utf8: str) -> bytes:
    ascii: bytes = utf8.encode('ascii', 'xmlcharrefreplace')
    return ascii

def to_utf8(ascii: str) -> bytes:
    utf8: str = unescape(ascii)
    return utf8

def file_to_ascii(path: str) -> None:
    with open(path, 'r') as utf8:
        content: str = utf8.read()

    path_split: list[str] = path.split('.')

    converted: str = to_ascii(content)
    with open(f'{path_split[0]}_utf8.{path_split[1]}', 'wb') as ascii:
        ascii.write(converted)
    
    return