from typing import List
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDataWidgetMapper, QDialog, QHeaderView, QLabel, QLineEdit, QListView, QTableView
from pytestqt.qtbot import QtBot
import pytest
from ime.qt_models import DataclassTableModel
from ime.models import Experiment, IngestionMetadata

@pytest.fixture
def experiments(metadata: IngestionMetadata):
    # This path is relative to where pytest is run.
    # So run pytest at the root directory.
    source_mdl = DataclassTableModel(Experiment)
    source_mdl.set_instance_list(metadata.experiments)
    return source_mdl

def test_show_experiment_table(qtbot: QtBot, experiments: DataclassTableModel[Experiment]):
    view = QTableView()
    model = experiments.proxy(["title"])
    model.set_read_only(True)
    view.setModel(model)
    # view.setColumnHidden(model.column_for_field("project_id"), True)
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    # Assert that the proxy model shows the correct data in the first row, second column.
    assert model.rowCount() == 3
    assert model.data(model.index(0,0), Qt.ItemDataRole.DisplayRole) == "biru-exp1"

def test_retrieve_instance(qtbot: QtBot, experiments: DataclassTableModel[Experiment]):
    model = experiments.proxy(['title'])
    instance = model.instance(0)
    assert instance.title == "biru-exp1"

# def test_simple_edit_experiment_table(qtbot: QtBot, experiments: List[Experiment]):
#     view = QDialog()
#     name_label = QLabel("Experiment name", view)
#     name_edit = QLineEdit(view)
#     model = MyTardisObjectModel(experiments)
#     mapper = QDataWidgetMapper()
#     mapper.setModel(model)
#     mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
#     mapper.addMapping(name_edit, model.column_for_field("experiment_name"))
#     mapper.toFirst()
#     qtbot.add_widget(view)
#     view.show()
#     qtbot.wait_exposed(view)
#     assert name_edit.text() == "Calibration 10 X"
#     name_edit.setText("Modified calibration 20 X")
#     mapper.submit()
#     # Test that the edit has made it to data model
#     assert experiments[0].experiment_name == "Modified calibration 20 X"