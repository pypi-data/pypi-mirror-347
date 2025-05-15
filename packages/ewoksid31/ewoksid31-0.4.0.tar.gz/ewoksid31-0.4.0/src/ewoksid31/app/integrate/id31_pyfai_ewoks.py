from __future__ import annotations

import argparse
import os
import logging
import threading
import sys
import ctypes
from importlib.metadata import version

# Environment variable HDF5_USE_FILE_LOCKING must be set *before* importing HDF5 libraries
# This prevents file locking issues, especially in shared filesystems (e.g., NFS).
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

from .hdf5widget import Hdf5TreeView  # noqa: E402
from .utils import (  # noqa: E402
    generateInputs,
    extractScanNumber,
    getScanEnergy,
    FilenameCompleterLineEdit,
    get_scan_url,
)
from ewoks.bindings import execute_graph  # noqa: E402
from ewoks.bindings import submit_graph  # noqa: E402

import PyQt5.QtCore  # noqa: F401,E402; Needed to force PyQt5
from silx.gui import qt, icons, hdf5  # noqa: E402
from silx.gui.utils.concurrent import submitToQtMainThread  # noqa: E402

from ..utils import (  # noqa: E402
    FLATFIELD_DEFAULT_DIR,
    NEWFLAT_FILENAME,
    OLDFLAT_FILENAME,
)
from .output_widget import OutputWidget  # noqa: E402

_logger = logging.getLogger(__name__)

_FILE_EXTENSIONS = ".h5", ".hdf5", ".hdf", ".nx", ".nxs", ".nx5", ".nexus"


class Id31FAIEwoksMainWindow(qt.QMainWindow):
    """
    This GUI is designed for reprocessing HDF5 scans data with fast azimuthal
    integration using Ewoks workflows (ewoksXRPD)
    """

    _SETTINGS_VERSION_STR: str = "1"
    _DETECTOR_NAMES: tuple[str] = (
        "p3",
        "de",
        "perkin",
    )
    _MONITOR_NAMES: tuple[str] = "mondio", "scaled_detdio", "scaled_mondio", "srcur"
    _INTEGRATION_METHODS: tuple[str] = (
        "no_csr_cython",
        "bbox_csr_cython",
        "full_csr_cython",
        "no_csr_ocl_gpu",
        "bbox_csr_ocl_gpu",
        "full_csr_ocl_gpu",
        "no_histogram_cython",
        "bbox_histogram_cython",
        "full_histogram_ocl_gpu",
    )

    _WORKFLOW_WITH_FLAT: str = "integrate_with_saving_with_flat.json"
    _WORKFLOW_WITHOUT_FLAT: str = "integrate_with_saving.json"
    _WORKFLOW_LOAD_OPTIONS: dict = {"root_module": "ewoksid31.workflows"}
    _HOSTS: tuple[str] = "Local", "Ewoks worker"

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("pyFAI with EWOKS - ID31")
        self.resize(1000, 800)

        self.statusBar = qt.QStatusBar()
        self.setStatusBar(self.statusBar)

        # Set paths
        self._defaultDirectoryRaw = ""
        self._flatFieldDirName = FLATFIELD_DEFAULT_DIR

        # Central Layout setup
        centralWidget = qt.QWidget(self)
        self.setCentralWidget(centralWidget)
        mainLayout = qt.QVBoxLayout(centralWidget)

        # HDF5 Viewer
        self._hdf5Widget = Hdf5TreeView()
        mainLayout.addWidget(self._hdf5Widget)

        # Menu and Toolbar setup
        self._setupMenuAndToolBar()

        # pyFAI Config Section
        pyFaiGroupBox = qt.QGroupBox("pyFAI config")
        pyFaiLayout = qt.QGridLayout()

        self._configFileLineEdit = FilenameCompleterLineEdit()
        self._configFileLineEdit.setPlaceholderText("/path/to/pyfai_config.json")

        loadConfigFileButton = qt.QPushButton("Open...")
        loadConfigFileButton.setIcon(icons.getQIcon("document-open"))
        loadConfigFileButton.clicked.connect(self._loadConfigFileButtonClicked)

        pyFaiLayout.addWidget(self._configFileLineEdit, 0, 0, 1, 1)
        pyFaiLayout.addWidget(loadConfigFileButton, 0, 1, 1, 1)

        pyFaiGroupBox.setLayout(pyFaiLayout)
        mainLayout.addWidget(pyFaiGroupBox)

        # Processing Options Section
        processingOptionsGroupBox = qt.QGroupBox("Processing options")
        processingOptionsLayout = qt.QGridLayout()

        spacer = qt.QSpacerItem(
            20, 10, qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum
        )
        processingOptionsLayout.addItem(spacer, 0, 4, 2, 4)

        detectorLabel = qt.QLabel("Detector:")
        self._detectorComboBox = qt.QComboBox()
        self._detectorComboBox.addItems(self._DETECTOR_NAMES)
        self._detectorComboBox.setCurrentText("p3")
        self._detectorComboBox.setToolTip("Select the detector type.")
        self._detectorComboBox.activated.connect(self._onDetectorChanged)

        processingOptionsLayout.addWidget(detectorLabel, 0, 0, 1, 1, qt.Qt.AlignLeft)
        processingOptionsLayout.addWidget(self._detectorComboBox, 0, 1, 1, 2)

        monitorNameLabel = qt.QLabel("Monitor name:")
        self._monitorNameComboBox = qt.QComboBox()
        self._monitorNameComboBox.addItems(self._MONITOR_NAMES)
        self._monitorNameComboBox.setCurrentText("scaled_mondio")
        self._monitorNameComboBox.setToolTip(
            "Select the monitor name for normalization."
        )

        processingOptionsLayout.addWidget(monitorNameLabel, 1, 0, 1, 1, qt.Qt.AlignLeft)
        processingOptionsLayout.addWidget(self._monitorNameComboBox, 1, 1, 1, 2)

        self._sigmaClipCheckBox = qt.QCheckBox("Sigma clipping threshold:")
        self._sigmaClipCheckBox.setChecked(False)
        self._sigmaClipCheckBox.setToolTip(
            "Check to enable sigma clipping and set threshold."
        )

        self._sigmaClipThresholdSpinBox = qt.QDoubleSpinBox()
        self._sigmaClipThresholdSpinBox.setSingleStep(0.1)
        self._sigmaClipThresholdSpinBox.setRange(0.1, 10.0)
        self._sigmaClipThresholdSpinBox.setValue(3.0)
        self._sigmaClipThresholdSpinBox.setDecimals(1)
        self._sigmaClipThresholdSpinBox.setEnabled(False)

        self._sigmaClipCheckBox.toggled.connect(
            self._sigmaClipThresholdSpinBox.setEnabled
        )
        self._sigmaClipCheckBox.toggled.connect(self._sigmaClipCheckBoxToggled)

        processingOptionsLayout.addWidget(
            self._sigmaClipCheckBox, 2, 0, 1, 1, qt.Qt.AlignLeft
        )
        processingOptionsLayout.addWidget(
            self._sigmaClipThresholdSpinBox, 2, 1, 1, 2, qt.Qt.AlignLeft
        )

        integrationMethodLabel = qt.QLabel("Integration method:")
        self._integrationMethodComboBox = qt.QComboBox()
        self._integrationMethodComboBox.addItems(self._INTEGRATION_METHODS)
        self._integrationMethodComboBox.setCurrentText("no_histogram_cython")
        self._integrationMethodComboBox.setToolTip(
            "Select the pyFAI integration method."
        )

        processingOptionsLayout.addWidget(
            integrationMethodLabel, 3, 0, 1, 1, qt.Qt.AlignLeft
        )
        processingOptionsLayout.addWidget(self._integrationMethodComboBox, 3, 1, 1, 2)

        radialUnitLabel = qt.QLabel("Radial unit:")
        self._qCheckBox = qt.QCheckBox("q (scattering vector)")
        self._qUnitsComboBox = qt.QComboBox()
        self._qUnitsComboBox.addItems(("Å⁻¹", "nm⁻¹"))
        self._2thCheckBox = qt.QCheckBox("2theta (degree)")
        self._qUnitsComboBox.setEnabled(False)
        self._qCheckBox.toggled.connect(self._qUnitsComboBox.setEnabled)

        processingOptionsLayout.addWidget(radialUnitLabel, 4, 0, 1, 1, qt.Qt.AlignLeft)
        processingOptionsLayout.addWidget(self._qCheckBox, 4, 1, 1, 1, qt.Qt.AlignLeft)
        processingOptionsLayout.addWidget(
            self._qUnitsComboBox, 4, 2, 1, 1, qt.Qt.AlignRight
        )
        processingOptionsLayout.addWidget(
            self._2thCheckBox, 5, 1, 1, 1, qt.Qt.AlignLeft
        )

        processingOptionsGroupBox.setLayout(processingOptionsLayout)
        mainLayout.addWidget(processingOptionsGroupBox)

        # Output Section
        self._outputWidget = OutputWidget()
        mainLayout.addWidget(self._outputWidget)

        # Run Section
        executionModeLayout = qt.QHBoxLayout()

        executionModeLabel = qt.QLabel("Host:")
        self._executionModeComboBox = qt.QComboBox()
        self._executionModeComboBox.addItems(self._HOSTS)
        self._executionModeComboBox.setCurrentText("Local")
        self._executionModeComboBox.setToolTip(
            "Select where the process will be executed: locally or on an Ewoks worker."
        )

        runButton = qt.QPushButton("Run")
        runButton.setIcon(icons.getQIcon("next"))
        runButton.clicked.connect(self._runButtonClicked)
        runButton.setToolTip("Run the processing workflow on the selected host.")
        runButton.setMinimumSize(runButton.sizeHint() * 2)

        executionModeLayout.addStretch()
        executionModeLayout.addWidget(runButton)
        executionModeLayout.addWidget(executionModeLabel)
        executionModeLayout.addWidget(self._executionModeComboBox)
        executionModeLayout.addStretch()

        mainLayout.addLayout(executionModeLayout)

    def _showHelpDialogClicked(self):
        """
        Display the Help dialog when the Help button is clicked.
        """
        helpDialog = qt.QMessageBox(self)
        helpDialog.setWindowTitle("Help")
        helpDialog.setIcon(qt.QMessageBox.Information)

        helpDialog.setTextFormat(qt.Qt.RichText)
        helpDialog.setText(
            f"<b>Welcome to the pyFAI with EWOKS application help (version {version('ewoksid31')}).</b><br>"
            "<br>How to get started?<br>"
            "<ul>"
            f"<li>Load raw data files {_FILE_EXTENSIONS}.</li>"
            "<li>Load the pyFAI configuration file.</li>"
            "<li>Select an output directory to save the processed data.</li>"
            "<li>Click Run to execute the workflow.</li>"
            "</ul>"
            "<br>For more information, visit:<br>"
            '<a href="https://ewoksid31.readthedocs.io/en/latest/">Ewoksid31 Documentation</a><br>'
            '<a href="https://confluence.esrf.fr/display/ID31KB/GUI+for+reprocessing+XRPD+data">ID31 GUI Confluence Page</a>'
        )

        helpDialog.setStandardButtons(qt.QMessageBox.Ok)
        helpDialog.exec_()

    def _setupMenuAndToolBar(
        self,
    ) -> None:
        """
        Setup of the main menu and toolbar with actions for file handling.
        """
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")

        openAction = qt.QAction(icons.getQIcon("document-open"), "Open...", self)
        openAction.triggered.connect(self._openActionTriggered)
        openAction.setShortcut(qt.QKeySequence.StandardKey.Open)
        reloadAction = qt.QAction(icons.getQIcon("view-refresh"), "Reload", self)
        reloadAction.triggered.connect(self._hdf5Widget.reloadSelected)
        reloadAction.setShortcut(qt.QKeySequence.StandardKey.Refresh)
        clearAction = qt.QAction(icons.getQIcon("remove"), "Clear", self)
        clearAction.triggered.connect(self._hdf5Widget.clearFiles)
        clearAction.setShortcut(qt.QKeySequence.StandardKey.Delete)

        fileMenu.addActions([openAction, reloadAction, clearAction])

        toolBar = self.addToolBar("File Actions")
        toolBar.addActions([openAction, reloadAction, clearAction])
        toolBar.setMovable(False)
        self.setContextMenuPolicy(qt.Qt.PreventContextMenu)
        toolBar.setFloatable(False)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Preferred)
        toolBar.addWidget(spacer)

        helpAction = qt.QAction(
            self.style().standardIcon(qt.QStyle.SP_TitleBarContextHelpButton), "", self
        )
        font = helpAction.font()
        font.setBold(True)
        helpAction.setFont(font)
        helpAction.setToolTip("About this app")
        helpAction.triggered.connect(self._showHelpDialogClicked)
        toolBar.addAction(helpAction)

    def addRawDataFile(self, fileName: str) -> None:
        """
        Proxy method to add a new file to the HDF5 tree viewer.
        """
        if not fileName or not os.path.isfile(fileName):
            qt.QMessageBox.warning(
                self, "Invalid File Format", "The selected file does not exist."
            )
            return
        if not fileName.endswith(_FILE_EXTENSIONS):
            qt.QMessageBox.warning(
                self,
                "Invalid File Format",
                f"Please select a valid HDF5 or NEXUS file {_FILE_EXTENSIONS}.",
            )
            return
        self._hdf5Widget.addFile(fileName)
        self._defaultDirectoryRaw = os.path.dirname(fileName)

    def _openActionTriggered(self) -> None:
        """
        Add Raw data as HDF5 file without cleaning the tree viewer.
        """
        nameFilter = " ".join(f"*{ext}" for ext in _FILE_EXTENSIONS)
        fileName, _ = qt.QFileDialog.getOpenFileName(
            self,
            "Add RAW data file",
            self._defaultDirectoryRaw,
            f"HDF5 files ({nameFilter});;All files (*)",
        )
        if fileName:
            self.addRawDataFile(fileName)

    def _loadConfigFileButtonClicked(self) -> None:
        """
        Choose and import JSON or PONI config file.
        """
        currentDir = os.path.dirname(self.getConfigFilePath()) or os.getcwd()
        filePath, _ = qt.QFileDialog.getOpenFileName(
            self,
            "Open config file",
            currentDir,
            "JSON or PONI files (*.json *.poni);;All files (*)",
        )
        if filePath:
            self.setConfigFilePath(filePath)
        else:
            self.setConfigFilePath("")
            _logger.info("No config file chosen.")

    def getFlatFieldDirName(self) -> str:
        """Returns the flat-field directory where to find flats.mat and oldflats.mat"""
        return self._flatFieldDirName

    def setFlatFieldDirName(self, path: str):
        """Set the directory where to find flats.mat and oldflats.mat"""
        self._flatFieldDirName = os.path.abspath(path)

    def getConfigFilePath(self) -> str:
        """
        Returns the current configuration file path from the line edit.
        """
        return self._configFileLineEdit.text().strip()

    def setConfigFilePath(self, path: str) -> None:
        """
        Update the configuration file path in the line edit.
        """
        self._configFileLineEdit.setText(path)

    def _sigmaClipCheckBoxToggled(self, toggled: bool) -> None:
        """
        Update integration methods combo box according to sigma clipping.

        - Change selected method if not supported by sigma clipping
        - Enable/Disable pixel splitting methods depending on sigma clipping
        """
        noCsrPrefix = "no_csr"

        if toggled and not self._integrationMethodComboBox.currentText().startswith(
            noCsrPrefix
        ):
            self._integrationMethodComboBox.setCurrentText("no_csr_ocl_gpu")

        model = self._integrationMethodComboBox.model()
        for row in range(self._integrationMethodComboBox.count()):
            item = model.item(row)
            if not item.text().startswith(noCsrPrefix):
                flags = item.flags()
                if toggled:
                    item.setFlags(flags & ~qt.Qt.ItemIsEnabled)
                    item.setToolTip("Not available with sigma clipping")
                else:
                    item.setFlags(flags | qt.Qt.ItemIsEnabled)
                    item.setToolTip("")

    def _getSigmaClippingThreshold(self) -> float | None:
        """
        Retrieve Sigma Clipping threshold from the user interface.

        Returns:
            The Sigma Clipping threshold if enabled.
        """
        if self._sigmaClipCheckBox.isChecked():
            return float(self._sigmaClipThresholdSpinBox.value())
        return None

    def _onDetectorChanged(self) -> None:
        """
        Prompt the user to verify the configuration file after changing the detector.

        Ensures that the selected config file in the 'pyFAI config' section is compatible with the newly selected detector.
        """

        selectedDetector = self._detectorComboBox.currentText()

        message = (
            f"You just changed the detector to <b><i>{selectedDetector}</i></b>.<br><br>"
            "Please ensure that the <b>config file</b> in the <i>pyFAI config</i> section is correct.<br>"
            "If necessary, load the appropriate <b>JSON</b> or <b>PONI</b> file."
        )

        qt.QMessageBox.information(self, "Configuration file verification", message)

    def _getSelectedUnits(self) -> list[str]:
        """
        Retrieves the selected units for azimuthal integration.

        Returns:
            A list of selected units, including q (Å⁻¹ or nm⁻¹) and/or 2θ (degrees).
        """
        units = list()
        if self._qCheckBox.isChecked():
            if self._qUnitsComboBox.currentText() == "Å⁻¹":
                units.append("q_A^-1")
            elif self._qUnitsComboBox.currentText() == "nm⁻¹":
                units.append("q_nm^-1")
        if self._2thCheckBox.isChecked():
            units.append("2th_deg")
        return units

    def _getParameters(
        self, datasetFilename: str, scanNumber: int, unit: str
    ) -> dict | None:
        """
        Generates parameters to execute workflow for a given scan.

        Args:
            datasetFilename: Filename of the HDF5 file containing the scan
            scanNumber: Number of the scan.
            unit: Selected unit.

        Returns:
            Dictionnary of parameters for the workflow, or None if failed.
        """
        energy = getScanEnergy(datasetFilename, scanNumber)

        if energy is None:
            _logger.error(
                f"Unable to retrieve energy for scan {scanNumber} in file {datasetFilename}."
            )
            return None

        inputParameters = generateInputs(
            newFlat=os.path.join(self.getFlatFieldDirName(), NEWFLAT_FILENAME),
            oldFlat=os.path.join(self.getFlatFieldDirName(), OLDFLAT_FILENAME),
            energy=energy,
            pyfaiConfig=self.getConfigFilePath(),
            pyfaiMethod=self._integrationMethodComboBox.currentText(),
            datasetFilename=datasetFilename,
            scanNumber=scanNumber,
            monitorName=self._monitorNameComboBox.currentText(),
            referenceCounts=1,
            detectorName=self._detectorComboBox.currentText(),
            outputDirectory=self._outputWidget.getOutputDirName(),
            sigmaClippingThreshold=self._getSigmaClippingThreshold(),
            asciiExport=self._outputWidget.isAsciiExportEnabled(),
            unit=unit,
            tomoEnabled=self._outputWidget.isTomoEnabled(),
            tomoScanEntryUrl=f"{datasetFilename}::/{scanNumber}.1",
            rotName=self._outputWidget.getTomoRotName(),
            yName=self._outputWidget.getTomoYName(),
            tomoOutputFilename=os.path.join(
                self._outputWidget.getOutputDirName(), f"{scanNumber}_tomo.h5"
            ),
        )

        return inputParameters

    def _prepareScans(self, scans: list[hdf5.H5Node]) -> list[dict]:
        """
        Prepares parameters for each unique selected scan and selected unit.
        """
        uniqueScans = set()
        for scan in scans:
            scanNumber = extractScanNumber(scan.physical_name)
            if scanNumber == -1:
                _logger.warning(
                    f"Skipping scan: Invalid scan number in {scan.physical_name}"
                )
                continue
            uniqueScans.add((scan.physical_filename, scanNumber))

        inputParameters = list()
        selectedUnits = self._getSelectedUnits()
        for rawDataFilename, scanNumber in uniqueScans:
            for unit in selectedUnits:
                workflowParameters = self._getParameters(
                    rawDataFilename, scanNumber, unit
                )
                if not workflowParameters:
                    _logger.warning(
                        f"Skipping scan {rawDataFilename}::{scanNumber} due to missing parameters."
                    )
                    continue

                inputParameters.append(workflowParameters)

        return inputParameters

    def _processScans(self, scans: list[hdf5.H5Node], local: bool = True) -> None:
        """
        Execute workflow and save HDF5 data and JSON workflow ewoks file from a single selected scan
        and selected unit.

        Executing in a separate thread.

        Args:
            scans: Selected scan nodes
            local: Whether to execute locally or submit to Ewoks worker.
        """
        inputParameters = self._prepareScans(scans)

        if local:
            self._updateStatusBar("Processing scans locally...")
            _logger.info("Processing scans locally...")
            thread = threading.Thread(
                target=self._executeWorkflowForParams, args=(inputParameters,)
            )
            thread.start()
        else:
            self._updateStatusBar("Submitting scans to Ewoks worker...")
            _logger.info("Submitting scans to Ewoks worker...")
            self._submitWorkflowForParams(inputParameters)

    def _showErrorInStatusBar(self, message: str) -> None:
        """
        Display an error message in the status bar and log it.

        Args:
            message: The error message to display.
        """
        _logger.error(message)
        submitToQtMainThread(self._updateStatusBar, message, error=True)

    def _getWorkflow(self) -> str:
        """
        Returns the appropriate workflow based on the selected detector.
        """
        if self._detectorComboBox.currentText() == "p3":
            return self._WORKFLOW_WITH_FLAT
        return self._WORKFLOW_WITHOUT_FLAT

    def _executeWorkflowForParams(self, params: list[dict]) -> None:
        """
        Workflow execution for multiple scans in a single thread (locally).

        Args:
            params: List of workflow input parameters for each scan.
        """
        for workflowParameters in params:
            datasetFilename, scanNumber = get_scan_url(workflowParameters)

            try:
                execute_graph(
                    self._getWorkflow(),
                    load_options=self._WORKFLOW_LOAD_OPTIONS,
                    **workflowParameters,
                )
                _logger.info(
                    f"Successfully processed scan: {os.path.basename(datasetFilename)}::{scanNumber}"
                )
            except Exception as e:
                errorMsg = f"Error processing scan {scanNumber}: {e}"
                _logger.error(errorMsg)
                submitToQtMainThread(self._updateStatusBar, errorMsg, error=True)
                raise e

        submitToQtMainThread(
            self._updateStatusBar, "Processing completed successfully."
        )
        _logger.info(f"All results saved in: {self._outputWidget.getOutputDirName()}")

    def _runButtonClicked(self) -> None:
        """
        Handle the run button click. Validate inputs, adjust output directory and process scans based on the selected execution mode.
        """
        if not self._validateInputParameters():
            return
        pass

        selectedScanNodes = list(self._hdf5Widget.getSelectedNodes())

        if not self._adjustOutputDirectory():
            self._updateStatusBar("Process canceled by user.", error=True)
            return

        executionMode = self._executionModeComboBox.currentText()

        if executionMode == "Local":
            self._processScans(selectedScanNodes, local=True)
        elif executionMode == "Ewoks worker":
            self._processScans(selectedScanNodes, local=False)
        else:
            self._updateStatusBar(
                f"Unknown execution mode: {executionMode}.", error=True
            )

    def _processFutures(self, futures: list[tuple]) -> None:
        """
        Process the futures in a separate thread.

        Args:
            futures: A list of tuples containing -> (future, scanName).
        """
        failed = list()
        for future, scanName in futures:
            try:
                future.get()
            except Exception as e:
                _logger.error(f"Workflow failed for {scanName}: {e}")
                failed.append(scanName)

        if failed:
            errorMsg = f"Workflows completed with errors for scans: {', '.join(failed)}"
            submitToQtMainThread(self._updateStatusBar, errorMsg, error=True)

        else:
            successMsg = "All workflows completed successfully."
            submitToQtMainThread(self._updateStatusBar, successMsg)
            _logger.info(
                f"All results saved in: {self._outputWidget.getOutputDirName()}"
            )

    def _submitWorkflowForParams(self, params: list[dict]) -> None:
        """
        Submit workflow for multiple scans to the Ewoks worker (remotely).

        Args:
            params: List of workflow input parameters for each scan.
        """
        futures = list()

        for workflowParameters in params:
            scanName = workflowParameters.pop("scanName", "Unknown scan")
            _logger.info(f"Submitting workflow for parameters: {scanName}")

            try:
                future = submit_graph(
                    self._getWorkflow(),
                    load_options=self._WORKFLOW_LOAD_OPTIONS,
                    **workflowParameters,
                )
                futures.append((future, scanName))
                _logger.info(f"Successfully submitted scan: {scanName}")
            except Exception as e:
                errorMsg = f"Error submitting scan {scanName}: {e}"
                _logger.error(errorMsg)
                self._updateStatusBar(errorMsg, error=True)

        thread = threading.Thread(target=self._processFutures, args=(futures,))
        thread.start()

    def _submitButtonClicked(self) -> None:
        """
        Handle the submit button click. Validate inputs, adjust output directory and submit scans to the worker.
        """

        if not self._validateInputParameters():
            return

        selectedScanNodes = list(self._hdf5Widget.getSelectedNodes())

        if not self._adjustOutputDirectory():
            self._updateStatusBar("Process canceled by user.", error=True)
            return

        self._processScans(selectedScanNodes, local=False)

    def _getValidationErrors(
        self,
        rawDataLoaded: bool,
        selectedScanNodes: list[hdf5.H5Node],
        configFileLoaded: bool,
        unitSelected: bool,
    ) -> list[str]:
        """
        Generate a list of validation error messages based on the current state.

        Args:
            rawDataLoaded: Whether raw data is loaded.
            selectedScanNodes: List of selected scan nodes.
            configFileLoaded: Whether a configuration file is loaded.
            unitSelected: Whether at least one radial unit is selected.

        Returns:
            A list of error messages if validation fails, otherwise an empty list.
        """
        errors = list()

        isOnlyRootSelected = (
            len(selectedScanNodes) == 1 and selectedScanNodes[0].physical_name == "/"
        )

        if isOnlyRootSelected:
            errors.append(
                "Only the root of the HDF5 file is selected. Please select one or more scans."
            )

        if not rawDataLoaded:
            errors.append("No raw data file loaded.")
        if not selectedScanNodes:
            errors.append("No scan selected.")
        if not configFileLoaded:
            errors.append("No pyFAI config file loaded.")
        if not unitSelected:
            errors.append("No radial unit selected.")
        return errors

    def _showWarningMessage(self, errorMessages: list[str]) -> None:
        """
        Show a warning message box if prerequisites for processing are not met.
        """
        warningMessageBox = qt.QMessageBox(self)
        warningMessageBox.setWindowTitle("Workflow cannot be excecuted")
        warningMessageBox.setIcon(qt.QMessageBox.Warning)
        warningMessageBox.setText("\n".join(errorMessages))
        warningMessageBox.exec_()

    def _validateInputParameters(self) -> bool:
        """
        Validates that all necessary inputs are present before starting processing.

        Returns:
            True if inputs are valid, False otherwise.
        """
        rawDataLoaded = not self._hdf5Widget.isEmpty()
        selectedScanNodes = self._hdf5Widget.getSelectedNodes()
        configFileLoaded = bool(self.getConfigFilePath())

        unitSelected = self._qCheckBox.isChecked() or self._2thCheckBox.isChecked()

        errorMessages = self._getValidationErrors(
            rawDataLoaded, selectedScanNodes, configFileLoaded, unitSelected
        )

        if errorMessages:
            self._updateStatusBar(" ".join(errorMessages), error=True)
            _logger.warning(f"Processing cannot start: {' '.join(errorMessages)}")
            self._showWarningMessage(errorMessages)
            return False
        return True

    def _showConfirmationMessage(self, outputDirectory: str) -> bool:
        """
        Show a confirmation message box when creating a new directory for output file.

        Returns True is the user confirms, otherwise False.
        """
        confirmationMessageBox = qt.QMessageBox(self)
        confirmationMessageBox.setWindowTitle("Overwrite Output Files")
        confirmationMessageBox.setIcon(qt.QMessageBox.Question)
        confirmationMessageBox.setText("The selected output directory already exists.")
        confirmationMessageBox.setInformativeText(
            f"Do you want to overwrite existing files in: {outputDirectory} ?\nUnchanged files will be preserved."
        )
        confirmationMessageBox.setStandardButtons(
            qt.QMessageBox.Ok | qt.QMessageBox.Cancel
        )
        userResponse = confirmationMessageBox.exec_()
        return userResponse == qt.QMessageBox.Ok

    def _adjustOutputDirectory(self) -> bool:
        """
        Use the selected output directory directly, without creating a new one.
        Ask for confirmation if the folder already exists.

        Returns:
            True if the process should continue, False if canceled.
        """
        currentOutputDir = self._outputWidget.getOutputDirName()
        if os.path.exists(currentOutputDir):
            if not self._showConfirmationMessage(currentOutputDir):
                _logger.info("Process canceled by the user.")
                return False
            _logger.info(
                f"Processed data will be written in existing directory: {currentOutputDir}"
            )

        return True

    def _updateStatusBar(self, message: str, error: bool = False):
        """
        Updates the status bar with a message.

        If 'error' is True, displays the message in red.
        """
        self.statusBar.setStyleSheet("color: red;" if error else "")
        self.statusBar.showMessage(message)

    def loadSettings(self) -> None:
        """
        Load user settings.
        """
        settings = qt.QSettings()

        if settings.value("version") != self._SETTINGS_VERSION_STR:
            _logger.info("Setting version mismatch. Clearing settings.")
            settings.clear()
            return

        geometry = settings.value("mainWindow/geometry")
        if geometry:
            self.restoreGeometry(geometry)

        self._defaultDirectoryRaw = settings.value("input/inputDirectory", "")

        self.setConfigFilePath(settings.value("config/configFile", ""))

        detectorName = settings.value("options/detectorName", None)
        if detectorName in self._DETECTOR_NAMES:
            self._detectorComboBox.setCurrentText(detectorName)

        monitorName = settings.value("options/monitorName", None)
        if monitorName in self._MONITOR_NAMES:
            self._monitorNameComboBox.setCurrentText(monitorName)

        self._sigmaClipCheckBox.setChecked(
            settings.value("options/sigmaClipping/enabled", False, type=bool)
        )
        self._sigmaClipThresholdSpinBox.setValue(
            settings.value("options/sigmaClipping/threshold", 3, type=float)
        )

        integrationMethod = settings.value("options/integrationMethod", None)
        if integrationMethod in self._INTEGRATION_METHODS:
            self._integrationMethodComboBox.setCurrentText(integrationMethod)

        self._qCheckBox.setChecked(settings.value("options/units/q", False, type=bool))
        selectedQUnit = settings.value("options/units/q_unit", "Å⁻¹")
        if selectedQUnit in ["Å⁻¹", "nm⁻¹"]:
            self._qUnitsComboBox.setCurrentText(selectedQUnit)

        self._2thCheckBox.setChecked(
            settings.value("options/units/2th", False, type=bool)
        )

        self._outputWidget.setTomoEnabled(
            settings.value("output/tomo/enabled", False, type=bool)
        )
        self._outputWidget.setTomoRotName(settings.value("output/tomo/rot_name", "nth"))
        self._outputWidget.setTomoYName(settings.value("output/tomo/y_name", "ny"))

        outputDirectory = settings.value("output/outputDirectory", "")
        self._outputWidget.setOutputDirName(outputDirectory)
        self._outputWidget.setAsciiExportEnabled(
            settings.value("output/asciiExport", False, type=bool)
        )

        executionMode = settings.value("run/executionMode", None)
        if executionMode in self._HOSTS:
            self._executionModeComboBox.setCurrentText(executionMode)

    def closeEvent(self, event: qt.QCloseEvent) -> None:
        """
        Save user settings on application close.
        """
        settings = qt.QSettings()

        settings.setValue("version", self._SETTINGS_VERSION_STR)
        settings.setValue("mainWindow/geometry", self.saveGeometry())

        settings.setValue("input/inputDirectory", self._defaultDirectoryRaw)

        settings.setValue("config/configFile", self.getConfigFilePath())

        settings.setValue("options/detectorName", self._detectorComboBox.currentText())
        settings.setValue(
            "options/monitorName", self._monitorNameComboBox.currentText()
        )
        settings.setValue(
            "options/sigmaClipping/enabled", self._sigmaClipCheckBox.isChecked()
        )
        settings.setValue(
            "options/sigmaClipping/threshold",
            float(self._sigmaClipThresholdSpinBox.value()),
        )
        settings.setValue(
            "options/integrationMethod", self._integrationMethodComboBox.currentText()
        )
        settings.setValue("options/units/q", self._qCheckBox.isChecked())
        settings.setValue("options/units/q_unit", self._qUnitsComboBox.currentText())
        settings.setValue("options/units/2th", self._2thCheckBox.isChecked())

        settings.setValue("output/tomo/enabled", self._outputWidget.isTomoEnabled())
        settings.setValue("output/tomo/rot_name", self._outputWidget.getTomoRotName())
        settings.setValue("output/tomo/y_name", self._outputWidget.getTomoYName())

        settings.setValue(
            "output/outputDirectory", self._outputWidget.getOutputDirName()
        )
        settings.value("output/asciiExport", self._outputWidget.isAsciiExportEnabled())

        settings.setValue(
            "run/executionMode", self._executionModeComboBox.currentText()
        )

        event.accept()


def create_argument_parser():
    parser = argparse.ArgumentParser(
        description="",
    )
    parser.add_argument(
        "-f",
        "--fresh",
        action="store_true",
        help="Start without loading previous user preferences",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=False,
        help="Dataset file to process (HDF5 format)",
        default="",
        metavar="FILE",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        required=False,
        help="Folder where to store the results",
        default="",
        metavar="FOLDER",
    )
    parser.add_argument(
        "-c",
        "--pyfai-config",
        type=str,
        default=None,
        help="PyFAI config file (.json)",
        metavar="FILE",
    )
    parser.add_argument(
        "--flat-dir",
        type=str,
        required=False,
        help=f"Folder containing flat-field files: flats.mat and old_flats.mat (default: {FLATFIELD_DEFAULT_DIR})",
        default=FLATFIELD_DEFAULT_DIR,
        metavar="FOLDER",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level (-v: INFO, -vv:DEBUG)",
    )
    return parser


def main():
    logging.basicConfig(level=logging.WARNING)

    parser = create_argument_parser()
    args = parser.parse_args()

    logging.captureWarnings(True)

    if args.verbose == 0:
        logging.getLogger().setLevel(logging.ERROR)
        _logger.setLevel(logging.INFO)

    elif args.verbose == 1:
        logging.getLogger().setLevel(logging.WARNING)
        _logger.setLevel(logging.INFO)

    else:
        logging.getLogger().setLevel(logging.DEBUG)

    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "ESRF.id31pyfaiewoks"
        )

    app = qt.QApplication([])
    app.setOrganizationName("ESRF")
    app.setOrganizationDomain("esrf.fr")
    app.setApplicationName("id31pyfaiewoks")

    app.setWindowIcon(
        qt.QIcon(os.path.join(os.path.dirname(__file__), "integrate.svg"))
    )

    window = Id31FAIEwoksMainWindow()
    window.setAttribute(qt.Qt.WA_DeleteOnClose)

    window.setFlatFieldDirName(args.flat_dir)

    if not args.fresh:
        _logger.debug(
            "Launching application in default mode. Loading previous settings."
        )

        window.loadSettings()

    if args.input:
        raw_data = os.path.abspath(args.input)
        if os.path.isfile(raw_data) and raw_data.endswith(_FILE_EXTENSIONS):
            window.addRawDataFile(raw_data)
        else:
            _logger.error(f"Invalid raw data file path or format: {raw_data}")

    if args.output_dir:
        window._outputWidget.setOutputDirName(args.output_dir)

    if args.pyfai_config:
        config_file = os.path.abspath(args.pyfai_config)
        if os.path.isfile(config_file):
            window.setConfigFilePath(config_file)
        else:
            _logger.error(f"Invalid config file path: {config_file}")

    window.show()
    app.exec_()
