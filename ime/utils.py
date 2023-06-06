"""
utils.py - miscellaneous functions.
"""

from PyQt5.QtWidgets import QHeaderView


def file_size_to_str(size: float) -> str:
    """
    Given a file size, return a human-friendly string representation.

    Args:
        size (float): Size of the file in bytes.

    Returns:
        str: Human-friendly string representation of the file size.
    """
    """Given a file size, return a human-friendly string."""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    # If size exceeds 1024 TB, return in terms of TB.
    return "%3.1f %s" % (size, "TB")

def setup_header_layout(header: QHeaderView) -> None:
    """Given a QHeaderView from a table or tree widget,
    sets up the resize mode such that the first column
    stretches, and subsequent sections fit to content.

    Args:
        header (QHeaderView): The headerView to apply
        the layout to.
    """
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    for i in range(1, header.model().columnCount()):
        header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
