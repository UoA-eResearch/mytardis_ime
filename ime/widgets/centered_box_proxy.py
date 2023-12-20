"""PySide6 port of a solution to center a column with checkbox: https://forum.qt.io/topic/94049/how-to-center-a-column-with-a-checkbox-in-qtableview/12"""
from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtWidgets import QProxyStyle, QStyleOptionViewItem, QStyleOption, QWidget

class CenteredBoxProxy(QProxyStyle):
    def subElementRect(self, element: QProxyStyle.SubElement, option: QStyleOption, widget: QWidget) -> QRect:
        # Due to a bug in PySide6 type annotation, ignoring errors on particular lines:
        # https://bugreports.qt.io/browse/PYSIDE-2263
        baseRes = super().subElementRect(element, option, widget)
        itemRect = option.rect # type:ignore 
        retval = baseRes
        sz = baseRes.size()

        if isinstance(option, QStyleOptionViewItem):
            flags: Qt.ItemFlag = option.index.flags() # type:ignore
            if flags & Qt.ItemFlag.ItemIsUserCheckable:
                # Apply centering styling on checkbox.
                if element == QProxyStyle.SubElement.SE_ItemViewItemCheckIndicator:
                    x = itemRect.x() + (itemRect.width()/2) - (baseRes.width()/2)
                    retval = QRect( QPoint(x, baseRes.y()), sz)

                elif element == QProxyStyle.SubElement.SE_ItemViewItemFocusRect:
                    sz.setWidth(baseRes.width() + baseRes.x())
                    retval = QRect(QPoint(0, baseRes.y()), sz)
        return retval