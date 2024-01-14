"""extraction_progress_dialog.py - Module for dialog to show progress in metadata extraction.
"""
from PySide6.QtWidgets import QDialog, QWidget
from ime.ui.ui_extraction_progress_dialog import Ui_ExtractionProgressDialog

class ExtractionProgressDialog(QDialog):
    """
    Class for the metadata extraction progress dialog.
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_ExtractionProgressDialog()
        self.ui.setupUi(self)

    def extractionFinished(self) -> None:
        """Method for notifying the dialog that extraction has
        finished. This will exit the dialog.
        """
        self.accept()
    
    def setNumFiles(self, num_files: int) -> None:
        """Sets the total number of files to perform extraction on.
        This will determine the progress bar calculation and reset any
        progress in the bar.

        Args:
            num_files (int): The number of files to extract.
        """
        self.ui.progressBar.setRange(1, num_files)
        self.ui.progressBar.reset()

    def progressChanged(self, name: str) -> None:
        """Method for advancing the progress bar by one file. Pass in
        the file name to show user which file is being processed.

        Args:
            name (str): File name to display in the file name label.
        """
        progressBar = self.ui.progressBar
        current = progressBar.value()
        # Increment progress by 1.
        self.ui.progressBar.setValue(current + 1)
        self.ui.fileName.setText(name)