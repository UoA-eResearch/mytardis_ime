from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QTableWidget, QUndoStack
from PyQt5.QtCore import QItemSelection, QItemSelectionModel, Qt
from metadata_tab import MetadataTab
from models import IngestionMetadata
from pytestqt.qtbot import QtBot
import pytest



@pytest.fixture
def metadata():
    with open('test/fixtures.yaml') as f:
        content = f.read()
        fixtures = IngestionMetadata.from_yaml(content)
        return fixtures
    

@pytest.fixture
def widget():
    return MetadataTab()

@pytest.fixture
def table(widget: MetadataTab):
    return widget.ui.metadata_table

def test_create_table_entries(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    assert table.rowCount() == 0
    exp = metadata.experiments[0]
    nrows = len(exp.metadata)
    widget.update_metadata_object(exp)
    qtbot.add_widget(widget)
    widget.show()
    qtbot.wait_exposed(widget)
    # Check that displayed table content reflects
    # imported yaml.
    assert table.rowCount() == nrows + 1
    assert table.item(0,0).text() == "lens"
    assert table.item(0,1).text() == "4"
    assert table.item(4,0).text() == ""
    assert table.item(4,1).text() == ""
    
def test_update_metadata_object_replaces_table_entries(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    exp = metadata.experiments[0]
    widget.update_metadata_object(exp)
    widget.show()
    proj = metadata.projects[0]
    widget.update_metadata_object(proj)
    qtbot.wait_exposed(widget)
    assert table.rowCount() == 4
    assert table.item(0,0).text() == "startdate"
    assert table.item(0,1).text() == "2022-08-01"
    assert table.item(3,0).text() == ""
    assert table.item(3,1).text() == ""

def test_update_metadata_key_changes_object(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    exp = metadata.experiments[0]
    widget.update_metadata_object(exp)
    nrows = len(exp.metadata)
    widget.show()
    qtbot.wait_exposed(widget)
    field_to_edit = table.item(0,1)
    field_to_edit.setText('9')
    assert exp.metadata['lens'] == '9'
    # Test creating a new entry by typing into the key field
    new_key_field = table.item(nrows,0)
    new_key_field.setText('Sample')
    assert 'Sample' in exp.metadata
    assert table.rowCount() == nrows + 2
    qtbot.stop()

def test_update_metadata_object_updates_value(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    exp = metadata.experiments[0]
    proj = metadata.projects[0]
    widget.update_metadata_object(exp)
    widget.show()
    qtbot.wait_exposed(widget)
    # Swap to a project, ensure that edits are being written
    # to the project.
    widget.update_metadata_object(proj)
    field_to_edit = table.item(0,1)
    field_to_edit.setText('1992-08-02')
    assert proj.metadata['startdate'] == '1992-08-02'

def test_delete_metadata_rows(qtbot: QtBot, metadata: IngestionMetadata, widget: MetadataTab, table: QTableWidget):
    exp = metadata.experiments[0]
    widget.update_metadata_object(exp)
    widget.show()
    qtbot.wait_exposed(widget)
    assert not widget.ui.remove_rows_btn.isEnabled()
    # Select the row.
    old_count = table.rowCount()
    old_text = table.item(2,1).text()
    table.selectRow(2)
    qtbot.stop()
    assert widget.ui.remove_rows_btn.isEnabled()
    widget.ui.remove_rows_btn.click()
    assert table.rowCount() == old_count - 1
    assert table.item(2,1).text() is not old_text
    assert "resolution" not in exp.metadata
