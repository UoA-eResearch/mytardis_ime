from PyQt5.QtWidgets import QApplication
from ime.mytardismetadataeditor import MyTardisMetadataEditor
import sys
import javabridge
import bioformats

if __name__ == "__main__":
    """
    The main function that initializes and runs the MyTardis Metadata Editor GUI application.

    Args:
        None

    Returns:
        None
    """
    # Check if a JVM is running
    is_jvm_running = False
    try:
        vm_env = javabridge.get_vm_env()
        if vm_env is not None:
            is_jvm_running= True
    except Exception:
        pass
    
    # Start the JVM if no JVM is running
    if not is_jvm_running:
        javabridge.start_vm(class_path=bioformats.JARS)

    app = QApplication([])
    window = MyTardisMetadataEditor()
    window.show()

    sys.exit(app.exec())
