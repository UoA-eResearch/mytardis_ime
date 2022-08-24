from typing import List
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QDataWidgetMapper, QDialog, QHeaderView, QLabel, QLineEdit, QListView, QTableView
from pytestqt.qtbot import QtBot
import pytest
from ime.qt_models import ExperimentDataModel, ListModel, ViewOnlyDataModel
from ime.models import Experiment, IngestionMetadata
from ime.widgets.ui_experiment_props import Ui_ExperimentPropertyEditor

@pytest.fixture
def experiments():
    # This path is relative to where pytest is run.
    # So run pytest at the root directory.
    with open('ime/tests/fixtures_qt_models.yaml') as f:
        content = f.read()
        fixtures = IngestionMetadata.from_yaml(content)
        return fixtures.experiments

def test_show_experiment_table(qtbot: QtBot, experiments: List[Experiment]):
    view = QTableView()
    model = ExperimentDataModel(experiments)
    viewOnlyModel = ViewOnlyDataModel()
    viewOnlyModel.setSourceModel(model)
    view.setModel(viewOnlyModel)
    # view.setColumnHidden(model.column_for_field("project_id"), True)
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    # qtbot.stop()
    assert model.rowCount() == 2
    assert model.data(model.index(0, 0)) == "Calibration 10 X"

def test_simple_edit_experiment_table(qtbot: QtBot, experiments: List[Experiment]):
    view = QDialog()
    name_label = QLabel("Experiment name", view)
    name_edit = QLineEdit(view)
    model = ExperimentDataModel(experiments)
    mapper = QDataWidgetMapper()
    mapper.setModel(model)
    mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
    mapper.addMapping(name_edit, model.column_for_field("experiment_name"))
    mapper.toFirst()
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    assert name_edit.text() == "Calibration 10 X"
    name_edit.setText("Modified calibration 20 X")
    mapper.submit()
    # Test that the edit has made it to data model
    assert experiments[0].experiment_name == "Modified calibration 20 X"

def test_nested_edit_experiment_table(qtbot, experiments: List[Experiment]):
    view = QDialog()
    user_list_label = QLabel("List users", view)
    user_list_edit = QListView(view)
    model1 = ListModel(experiments[0].admin_groups)
    user_list_edit.setModel(model1)
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
