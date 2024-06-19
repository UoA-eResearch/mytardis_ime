"""
Classes for styles.
"""
from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtWidgets import QProxyStyle, QStyleOption, QStyleOptionViewItem, QWidget


class CenteredCheckboxInViewItemStyle(QProxyStyle):
    """
    Style class for Qt View items, to center check boxes.
    To use:
    ```
    style = CenteredCheckboxInViewItemStyle(QApplication.style().name()) # Inherit styling from default app style.
    style.setParent(table_view) # Set Qt parent to prevent memory leak
    table_view.setStyle(style) # Apply style on a particular widget.
    ```
    Adapted from:
        https://forum.qt.io/topic/94049/how-to-center-a-column-with-a-checkbox-in-qtableview/12

    """

    def subElementRect(
        self, element: QProxyStyle.SubElement, option: QStyleOption, widget: QWidget
    ) -> QRect:
        """Override method for handling a subelement.
        Returns the sub-area for the given element as described in the provided style option.
        The returned rectangle is defined in screen coordinates.
        For all checkbox elements in a Qt View item, move to center of parent element.


        Returns:
            QRect: Screen coordinates for the sub-area.
        """
        # Due to a bug in PySide6 type annotation, ignoring errors on particular lines:
        # https://bugreports.qt.io/browse/PYSIDE-2263
        baseRes = super().subElementRect(element, option, widget)
        itemRect = option.rect  # type:ignore
        retval = baseRes
        sz = baseRes.size()

        # Check for Qt View cell items, and see if they are checkable.
        if isinstance(option, QStyleOptionViewItem):
            flags: Qt.ItemFlag = option.index.flags()  # type:ignore
            if flags & Qt.ItemFlag.ItemIsUserCheckable:
                # Apply centering styling on checkbox.
                if element == QProxyStyle.SubElement.SE_ItemViewItemCheckIndicator:
                    x = itemRect.x() + (itemRect.width() / 2) - (baseRes.width() / 2)
                    retval = QRect(QPoint(x, baseRes.y()), sz)

                elif element == QProxyStyle.SubElement.SE_ItemViewItemFocusRect:
                    sz.setWidth(baseRes.width() + baseRes.x())
                    retval = QRect(QPoint(0, baseRes.y()), sz)
        return retval
