from PyQt5.QtWidgets import QUndoStack
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

def test_create_table_entries(qtbot: QtBot, metadata: IngestionMetadata):
    widget = MetadataTab()
    table = widget.ui.metadata_table
    assert table.rowCount() == 0
    exp = metadata.experiments[0]
    widget.update_object(exp)
    qtbot.add_widget(widget)
    widget.show()
    qtbot.wait_exposed(widget)
    # Check that displayed table content reflects
    # imported yaml.
    assert table.rowCount() == 5
    assert table.item(0,0).text() == "lens"
    assert table.item(0,1).text() == "4"
    assert table.item(4,0).text() == ""
    assert table.item(4,1).text() == ""
    
def test_update_object_replaces_table_entries(qtbot: QtBot, metadata: IngestionMetadata):
    widget = MetadataTab()
    table = widget.ui.metadata_table
    exp = metadata.experiments[0]
    widget.update_object(exp)
    widget.show()
    proj = metadata.projects[0]
    widget.update_object(proj)
    qtbot.wait_exposed(widget)
    assert table.rowCount() == 4
    assert table.item(0,0).text() == "startdate"
    assert table.item(0,1).text() == "2022-08-01"
    assert table.item(3,0).text() == ""
    assert table.item(3,1).text() == ""



    # qtbot.mouseClick(widget.button_greet, qt_api.QtCore.Qt.MouseButton.LeftButton)

    # assert widget.greet_label.text() == "Hello!"