from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from ime.widgets.metadata_tab import MetadataTab
from ime.models import IngestionMetadata
from pytestqt.qtbot import QtBot
import pytest

@pytest.fixture
def widget():
    """Fixture to create MetadataTab widget instance."""
    return MetadataTab()

@pytest.fixture
def table(widget: MetadataTab):
    """Fixture to get the metadata table from the widget."""
    return widget.ui.metadata_table

def test_create_table_entries(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    """Test creating table entries from metadata."""
    assert table.rowCount() == 0, "Initial table should be empty"
    exp = metadata.experiments[0]
    assert exp.metadata is not None, "Experiment metadata should not be None"
    nrows = len(exp.metadata)
    widget.update_metadata_object(exp)
    qtbot.add_widget(widget)
    widget.show()
    qtbot.wait_exposed(widget)
    # Check that displayed table content reflects
    # imported yaml.
    assert table.rowCount() == nrows, "Table row count should match metadata"
    assert table.item(0,0).text() == "lens", "First item key should be 'lens'."
    assert table.item(0,1).text() == "4", "First item value should be '4'."
    
def test_update_metadata_object_replaces_table_entries(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    """Test updating metadata object replaces table entries."""
    exp = metadata.experiments[0]
    widget.update_metadata_object(exp)
    widget.show()
    proj = metadata.projects[0]
    widget.update_metadata_object(proj)
    qtbot.wait_exposed(widget)
    assert table.rowCount() == 3
    assert table.item(0,0).text() == "startdate"
    assert table.item(0,1).text() == "2022-08-01"

def test_update_metadata_key_changes_object(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    """Test that changing a metadata key updates the object."""
    exp = metadata.experiments[0]
    widget.update_metadata_object(exp)
    assert exp.metadata is not None, "Experiment metadata should not be None"
    nrows = len(exp.metadata)
    widget.show()
    qtbot.wait_exposed(widget)
    field_to_edit = table.item(0,1)
    if field_to_edit is None:
        field_to_edit = QTableWidgetItem()
        table.setItem(0,1, field_to_edit)
    field_to_edit.setText('9')
    assert exp.metadata['lens'] == '9', "Metadata object should be updated with new value."
    # Test changing the key.
    key_to_edit = table.item(0,0)
    if key_to_edit is None:
        key_to_edit = QTableWidgetItem()
        table.setItem(0,0, key_to_edit)
    key_to_edit.setText('Sample')
    assert 'lens' not in exp.metadata, "Old key should be removed from metadata object."
    assert 'Sample' in exp.metadata, "New key should be added to metadata object."

def test_update_metadata_object_updates_value(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    """Test updating metadata object updates value in the table."""
    exp = metadata.experiments[0]
    proj = metadata.projects[0]
    assert proj.metadata is not None
    widget.update_metadata_object(exp)
    widget.show()
    qtbot.wait_exposed(widget)
    # Swap to a project, ensure that edits are being written
    # to the project.
    widget.update_metadata_object(proj)
    field_to_edit = table.item(0,1)
    assert field_to_edit is not None
    field_to_edit.setText('1992-08-02')
    assert proj.metadata['startdate'] == '1992-08-02'

def test_delete_metadata_rows(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    """Test deleting metadata rows from the table."""
    exp = metadata.experiments[0]
    assert exp.metadata is not None
    widget.update_metadata_object(exp)
    widget.show()
    qtbot.wait_exposed(widget)
    assert not widget.ui.remove_rows_btn.isEnabled()
    # Select the row.
    old_count = table.rowCount()
    old_text = table.item(2,1).text() if table.item(2,1) is not None else ""
    table.selectRow(2)
    assert widget.ui.remove_rows_btn.isEnabled()
    widget.ui.remove_rows_btn.click()
    assert table.rowCount() == old_count - 1
    assert table.item(2,1).text() is not old_text
    assert "resolution" not in exp.metadata
