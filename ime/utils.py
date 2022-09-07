"""
utils.py - miscellaneous functions.
"""

def file_size_to_str(size: float) -> str:
    """Given a file size, return a human-friendly string."""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    # If size exceeds 1024 TB, return in terms of TB.
    return "%3.1f %s" % (size, "TB")