from PySide6.QtCore import QItemSelection, QSignalBlocker, Qt
from PySide6.QtWidgets import QLineEdit, QTableWidgetItem, QWidget

from ime.bindable import IBindableInput
from ime.models import MyTardisObject
from ime.ui.ui_metadata_tab import Ui_MetadataTab
from ime.utils import setup_header_layout


class MetadataTab(QWidget, IBindableInput):
    """A tab widget for displaying and editing metadata information for an object."""
    metadata_object: MyTardisObject
    ui: Ui_MetadataTab

    def __init__(self, parent=None):
        """Initializes the metadata tab with the given parent widget."""
        super().__init__(parent)
        self.ui = Ui_MetadataTab()
        self.ui.setupUi(self)
        self.ui.metadata_table.cellChanged.connect(self._handle_cell_changed)
        self.ui.schemaLineEdit.textChanged.connect(self.handle_schema_changed)
        self.ui.metadata_table.selectionModel().selectionChanged.connect(self.handle_selection_changed)
        self.ui.add_row_btn.clicked.connect(self._handle_add_row_click)
        self.ui.remove_rows_btn.clicked.connect(self.handle_remove_rows_click)
        self.ui.notes_textedit.textChanged.connect(self.handle_Notes_changed)
        setup_header_layout(self.ui.metadata_table.horizontalHeader())

    def handle_schema_changed(self, schema: str) -> None:
        """Handles the schema text box changing."""
        self.metadata_object.object_schema = self.ui.schemaLineEdit.text()

    def handle_Notes_changed(self) -> None:
        """Handler method for notes changed."""
        if self.metadata_object.metadata is None:
            self.metadata_object.metadata = {}
        self.metadata_object.metadata['Notes'] = self.ui.notes_textedit.toPlainText()

    def add_insert_metadata_row(self) -> None:
        """Adds an empty row to the metadata table."""
        table = self.ui.metadata_table

        # Create empty items for key and value
        key_item = QTableWidgetItem("")
        val_item = QTableWidgetItem("")

        # Get the current row count and insert a new row at the end
        row_idx = table.rowCount()
        table.insertRow(row_idx)

        # Set the empty items in the new row
        table.setItem(row_idx, 0, key_item)
        table.setItem(row_idx, 1, val_item)

    def get_metadata_row(self, key: str, val: str) -> tuple[QTableWidgetItem, QTableWidgetItem]:
        """Returns a key-value metadata row as QTableWidgetItem objects.

        Args:
            key (str): The key for the metadata field.
            val (str): The value for the metadata field.

        Returns:
            tuple(QTableWidgetItem, QTableWidgetItem): The key and value QTableWidgetItem objects.
        """
        # key_edit = QLineEdit()
        # key_edit.setText(key)
        # key_edit.setPlaceholderText("Name for the field, e.g. Batch number")
        key_item = QTableWidgetItem(key)
        # Use the UserRole to store another copy of the key,
        # so when user has edited the item we can find the
        # associated value.
        key_item.setData(Qt.ItemDataRole.UserRole, key)
        # key_item.setFlags(Qt.ItemFlag.ItemIsSelectable)
        # val_edit = QLineEdit()
        # val_edit.setText(val)
        # val_edit.setPlaceholderText("Value for the field, e.g. 400")
        val_item = QTableWidgetItem(val)
        return key_item, val_item

    def handle_selection_changed(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        """Enables the "Remove Rows" button if rows are selected in the metadata table.

        Args:
            selected (QItemSelection): The selected item(s).
            deselected (QItemSelection): The deselected item(s).
        """
        table = self.ui.metadata_table
        selected_rows = table.selectionModel().selectedRows()
        self.ui.remove_rows_btn.setEnabled(len(selected_rows) > 0)

    def _handle_cell_changed(self, row: int, col: int) -> None:
        """Private method that handles the change event for a cell in the metadata table.

        Args:
            row (int): The row index of the changed cell.
            col (int): The column index of the changed cell.
        """
        table = self.ui.metadata_table
        if self.metadata_object.metadata is None:
            self.metadata_object.metadata = {}
        metadata = self.metadata_object.metadata
        cell = table.item(row, col)
        cell_val = cell.text().strip()

        with QSignalBlocker(table):
            if col == 0:  # Key column
                old_name = cell.data(Qt.ItemDataRole.UserRole)
                if old_name and old_name in metadata:
                    if cell_val in metadata and old_name != cell_val:
                        # Duplicate key detected, revert to old name
                        cell.setText(old_name)
                        return
                    if cell_val == '':
                        # User has cleared the key, leaving an orphan value.
                        # Revert to old edit.
                        cell.setText(old_name)
                        return
                    else:
                        metadata[cell_val] = metadata.pop(old_name)
                        cell.setData(Qt.ItemDataRole.UserRole, cell_val)
                elif row == table.rowCount() - 1 and cell_val:  # New key in the last row
                    if cell_val in metadata:
                        # Duplicate key detected, clear the cell
                        cell.setText('')
                        return
                    metadata[cell_val] = ''
                    cell.setData(Qt.ItemDataRole.UserRole, cell_val)
            elif col == 1:  # Value column
                key_item = table.item(row, 0)
                if key_item:
                    key = key_item.text().strip()
                    if key:
                        metadata[key] = cell_val
                    else:
                        # If key is empty, clear the value
                        cell.setText('')

    def _handle_add_row_click(self) -> None:
        """Private method for handling when the Add button is
        clicked. Focuses the editing on the new edit row.
        """
        table = self.ui.metadata_table

        with QSignalBlocker(table):
            self.add_insert_metadata_row()

        new_row_index = table.rowCount() - 1
        # Focus the editing on the first cell of the new row
        edit_row_name_cell = table.model().index(new_row_index, 0)
        table.selectRow(new_row_index)
        table.edit(edit_row_name_cell)

    def handle_remove_rows_click(self) -> None:
        """Handles the click event for the Remove Rows button."""
        table = self.ui.metadata_table
        selected_rows = table.selectionModel().selectedRows()
        # Sort rows in descending order to avoid index shifting issues
        sorted_rows = sorted(selected_rows, key=lambda index: index.row(), reverse=True)

        with QSignalBlocker(table):
            for index in sorted_rows:
                row = index.row()
                key_item = table.item(row, 0)
                if key_item and self.metadata_object.metadata is not None:
                    key = key_item.text().strip()
                    if key in self.metadata_object.metadata:
                        del self.metadata_object.metadata[key]
                table.removeRow(index.row())

    def update_metadata_object(self, metadata_obj: MyTardisObject) -> None:
        """Updates the object this tab is modifying.

        Args:
            metadata_obj (MyTardisObject): The metadata object to update the tab with.
        """
        self.metadata_object = metadata_obj  # Update the metadata object first

        # Block table change signals while object is being updated.
        with QSignalBlocker(self.ui.metadata_table):
            table = self.ui.metadata_table
            # Clear all existing rows (if any) that's already
            # in the tab.
            table.clearContents()
            table.setRowCount(0)
            # Populate table with new items
            metadata = metadata_obj.metadata or {}
            # Set the row count, excluding "Notes" if present
            num_new = len(metadata) - ('Notes' in metadata)
            table.setRowCount(num_new)
            row_idx = 0
            for key, val in metadata.items():
                if key == "Notes":
                    # Skip the notes field. Display it in the separate notes
                    # section instead
                    continue
                key_item, val_item = self.get_metadata_row(key, str(val))
                table.setItem(row_idx, 0, key_item)
                table.setItem(row_idx, 1, val_item)
                row_idx += 1
        # Update schema
        object_schema_value = metadata_obj.object_schema
        self.ui.schemaLineEdit.setText(str(object_schema_value))
        # Update notes section
        notes = metadata.get('Notes', '')
        with QSignalBlocker(self.ui.notes_textedit):
            self.ui.notes_textedit.setText(notes)
