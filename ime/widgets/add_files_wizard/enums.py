"enum.py - Shared constant values in the Wizard."

from enum import Enum


class FieldNames(Enum):
    """Enum for wizard field names. These names are used in QWizard and QWizardPages
    for registering fields, and getting and setting values. 
    """
    IS_NEW_PROJECT = "isNewProject"
    IS_EXISTING_PROJECT = "isExistingProject"
    EXISTING_PROJECT = "existingProject"
    IS_NEW_EXPERIMENT = "isNewExperiment"
    IS_EXISTING_EXPERIMENT = "isExistingExperiment"
    EXISTING_EXPERIMENT = "existingExperiment"
    IS_NEW_DATASET = "isNewDataset"
    IS_EXISTING_DATASET = "isExistingDataset"
    EXISTING_DATASET = "existingDataset"
    PROJECT_ID = "projectIDLineEdit"
    PROJECT_NAME = "projectNameLineEdit"
    PROJECT_PI = "piLineEdit"
    EXPERIMENT_NAME = "experimentNameLineEdit"
    EXPERIMENT_ID = "experimentIDLineEdit"
    DATASET_ID = "datasetIDLineEdit"
    DATASET_NAME = "datasetNameLineEdit"

class PageNames(Enum):
    """Enum for wizard page names. These names are used to refer to specific wizard pages.
    They are also specified in ui/ui_add_files_wizard.ui."""
    INTRODUCTION = "introductionPage"
    PROJECT = "projectPage"
    EXPERIMENT = "experimentPage"
    DATASET = "datasetPage"
    NEW_PROJECT = "newProjectPage"
    NEW_EXPERIMENT = "newExperimentPage"
    NEW_DATASET = "newDatasetPage"
    INCLUDED_FILES = "includedFilesPage"
    SKIP_DATASET = "skipDatasetPage"
    SKIP_EXPERIMENT = "skipExpPage"
    SKIP_PROJECT = "skipProjectPage"
