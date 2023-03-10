from PyQt5.QtWidgets import QApplication
from ime.mytardismetadataeditor import MyTardisMetadataEditor
import sys

if __name__ == "__main__":
    """
    The main function that initializes and runs the MyTardis Metadata Editor GUI application.

    Args:
        None

    Returns:
        None
    """
    app = QApplication([])
    window = MyTardisMetadataEditor()
    window.show()
    sys.exit(app.exec())