import re

def strip_path(path: str) -> str:
    """Stripping the path in to the bare path
    Args:
        path (str): The path to be stripped
    Returns:
        str: The stripped path
    Examples:
        >>> path = strip_path(path='*/references/*')
        >>> print(path)
        references
    """
    path = re.sub(r'^[*/]+', '', path)
    path = re.sub(r'[*/]+$', '', path)
    return path