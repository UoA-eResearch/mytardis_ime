"""Module for a Qt-based thread metadata extraction worker.
"""
from PySide6.QtCore import QObject, QThread, Signal

from ime.models import Datafile
from ime.parser.image_parser import ImageProcessor


class MetadataExtractionWorkerThread(QThread):
    """
    Worker thread for metadata extraction. This offloads extraction to
    a separate thread, so it doesn't block GUI.
    """

    # Qt Signal for when there's a change in the image being processed.
    processedImageChanged = Signal(str)

    def __init__(self, files: list[Datafile], parent: QObject | None = None) -> None:
        """Constructor method that creates the worker thread. Includes an
        argument for passing in the Datafiles that need to be processed.

        Args:
            files (list[Datafile]): The files to extract metadata from.
            parent (QObject | None, optional): The Qt object parent for this object. Defaults to None.
        """
        super().__init__(parent)
        self.image_processor = ImageProcessor()
        self.datafiles = files

    def run(self) -> None:
        """Method for running the task of processing the files."""
        for file in self.datafiles:
            self.processedImageChanged.emit(file.path_abs.as_posix())
            metadata = self.image_processor.get_metadata(file.path_abs.as_posix())
            if file.metadata is None:
                file.metadata = metadata
            else:
                # If there is already metadata, add extracted
                # metadata to it.
                file.metadata.update(metadata)
