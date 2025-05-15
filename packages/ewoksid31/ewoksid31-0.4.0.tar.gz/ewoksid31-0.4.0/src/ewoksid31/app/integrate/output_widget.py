import os
import logging

from silx.gui import qt, icons

from ewoksid31.app.integrate.utils import FilenameCompleterLineEdit

_logger = logging.getLogger(__name__)


class OutputWidget(qt.QGroupBox):
    def __init__(self):
        super().__init__("Output")

        gridLayout = qt.QGridLayout()

        spacer = qt.QSpacerItem(
            20, 10, qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum
        )
        gridLayout.addItem(spacer, 0, 1, 1, 1)

        self._outputLineEdit = FilenameCompleterLineEdit()
        self._outputLineEdit.setPlaceholderText("/path/to/output/directory")

        outputDirButton = qt.QPushButton("Select...")
        outputDirButton.setToolTip("Define a new output directory.")
        outputDirButton.setIcon(icons.getQIcon("folder"))
        outputDirButton.clicked.connect(self._outputDirButtonClicked)

        self._asciiExportCheckBox = qt.QCheckBox()
        self._asciiExportCheckBox.setToolTip(
            "Enable to export data in ASCII format (.xye)."
        )

        self._tomoEnabledCheckBox = qt.QCheckBox("")
        self._tomoEnabledCheckBox.setChecked(False)
        self._tomoEnabledCheckBox.setToolTip(
            "Enable to export data in tomo-compatible HDF5 files."
        )
        self._tomoEnabledCheckBox.toggled.connect(self.toggleTomoWidgets)

        self._rotNameLineEdit = qt.QLineEdit()
        self._rotNameLineEdit.setPlaceholderText("{rot_name}")
        self._rotNameLineEdit.setToolTip(
            "Specify the Rotation angle dataset (e.g., nth)."
        )

        self._yNameLineEdit = qt.QLineEdit()
        self._yNameLineEdit.setPlaceholderText("{y_name}")
        self._yNameLineEdit.setToolTip(
            "Specify the radial position dataset (e.g., ny)."
        )
        self.toggleTomoWidgets(self._tomoEnabledCheckBox.isChecked())

        gridLayout.addWidget(qt.QLabel("Directory:"), 0, 0, 1, 1, qt.Qt.AlignLeft)
        gridLayout.addWidget(self._outputLineEdit, 0, 1, 1, 3)
        gridLayout.addWidget(outputDirButton, 0, 4, 1, 1, qt.Qt.AlignRight)

        gridLayout.addWidget(qt.QLabel("ASCII export:"), 1, 0, 1, 1, qt.Qt.AlignLeft)
        gridLayout.addWidget(self._asciiExportCheckBox, 1, 1, 1, 1, qt.Qt.AlignLeft)

        gridLayout.addWidget(
            qt.QLabel("XRD-CT tomo export:"), 2, 0, 1, 1, qt.Qt.AlignLeft
        )
        gridLayout.addWidget(self._tomoEnabledCheckBox, 2, 1, 1, 1, qt.Qt.AlignLeft)
        gridLayout.addWidget(qt.QLabel("- Rot name:"), 3, 0, 1, 1, qt.Qt.AlignRight)
        gridLayout.addWidget(self._rotNameLineEdit, 3, 1, 1, 1, qt.Qt.AlignLeft)
        gridLayout.addWidget(qt.QLabel("- Y name:"), 4, 0, 1, 1, qt.Qt.AlignRight)
        gridLayout.addWidget(self._yNameLineEdit, 4, 1, 1, 1, qt.Qt.AlignLeft)

        self.setLayout(gridLayout)

    def getOutputDirName(self) -> str:
        """
        Returns the current output directory path from the line edit.
        """
        return self._outputLineEdit.text().strip()

    def setOutputDirName(self, path: str) -> None:
        """
        Update the output directory path in the line edit.
        """
        self._outputLineEdit.setText(os.path.abspath(path))

    def _outputDirButtonClicked(self) -> None:
        """
        Choose an output directory using a dialog and set it in the line edit.
        """
        currentPath = self.getOutputDirName()
        if currentPath and os.path.exists(currentPath):
            pass
        else:
            currentPath = os.getcwd()
            _logger.info(f"Path not found. Falling back to: {currentPath}")

        newPath = qt.QFileDialog.getExistingDirectory(
            self, "Choose output directory", currentPath
        )
        if newPath:
            self.setOutputDirName(newPath)

    def isAsciiExportEnabled(self) -> bool:
        return self._asciiExportCheckBox.isChecked()

    def setAsciiExportEnabled(self, value: bool):
        self._asciiExportCheckBox.setChecked(value)

    def toggleTomoWidgets(self, enabled):
        self._rotNameLineEdit.setEnabled(enabled)
        self._yNameLineEdit.setEnabled(enabled)

    def isTomoEnabled(self) -> bool:
        return self._tomoEnabledCheckBox.isChecked()

    def setTomoEnabled(self, value: bool):
        self._tomoEnabledCheckBox.setChecked(value)

    def getTomoRotName(self) -> str:
        return self._rotNameLineEdit.text().strip()

    def setTomoRotName(self, value: str):
        self._rotNameLineEdit.setText(value)

    def getTomoYName(self) -> str:
        return self._yNameLineEdit.text().strip()

    def setTomoYName(self, value: str):
        self._yNameLineEdit.setText(value)
