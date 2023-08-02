"""
utils.py - miscellaneous functions.
"""

from pathlib import Path
from PyQt5.QtWidgets import QHeaderView, QTreeWidget


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


def setup_section_autoresize(widget: QTreeWidget) -> None:
    """Auto resize a QTreeWidget's first column when new content is added.

    Args:
        widget (QTreeWidget): The tree widget to resize.
    """
    def _handle_new_rows_inserted():
        widget.resizeColumnToContents(0)
    widget.itemChanged.connect(_handle_new_rows_inserted)

def setup_header_layout(header: QHeaderView) -> None:
    """Given a QHeaderView from a table or tree widget,
    sets up the resize mode such that the first column
    stretches, and subsequent sections fit to content.

    Args:
        header (QHeaderView): The headerView to apply
        the layout to.
    """
    header.resizeSections(QHeaderView.ResizeMode.Stretch)
    for i in range(1, header.model().columnCount()):
        header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

def st_dev(path: Path) -> int:
    """Returns the device that the file
    `path`_ is stored on. This function uses
    os.Path.stat() to get the device id.

    Args:
        path (Path): The Path of the file.

    Returns:
        int: the device id.
    """
    return path.stat().st_dev