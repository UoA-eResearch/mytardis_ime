from PyQt5.QtWidgets import QApplication
from ime.mytardismetadataeditor import MyTardisMetadataEditor
import sys

if __name__ == "__main__":
    app = QApplication([])
    window = MyTardisMetadataEditor()
    window.show()
    sys.exit(app.exec_())