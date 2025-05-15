from __future__ import annotations

from typing import Optional, Any
import os
import h5py
from silx.gui import qt
from ewoksutils.task_utils import task_inputs


def generateInputs(
    newFlat: str,
    oldFlat: str,
    energy: float,
    pyfaiConfig: dict,
    pyfaiMethod: str,
    datasetFilename: str,
    scanNumber: int,
    monitorName: str,
    referenceCounts: int,
    detectorName: str,
    outputDirectory: str,
    sigmaClippingThreshold: Optional[float],
    asciiExport: bool,
    unit: str,
    tomoEnabled: bool = False,
    tomoScanEntryUrl: str = "",
    rotName: str = "",
    yName: str = "",
    tomoOutputFilename: str = "",
) -> dict:
    """
    Generate input parameters for the EWOKS workflow, including optional tomo export.
    """
    baseDirName = os.path.splitext(os.path.basename(datasetFilename))[0]
    outputUnitSuffix = unit.split("_")[0]
    outputFilePathH5 = os.path.join(outputDirectory, f"{baseDirName}.h5")

    externalOutputFilePathH5 = os.path.join(
        outputDirectory, f"{baseDirName}_{outputUnitSuffix}.h5"
    )
    nxProcessName = f"{detectorName}_{outputUnitSuffix}_integrate"
    nxMeasurementName = f"{detectorName}_{outputUnitSuffix}_integrated"

    outputAsciiFileTemplate = os.path.join(
        f"{baseDirName}_{scanNumber:04d}_{detectorName}_{outputUnitSuffix}_%04d.xye",
    )

    outputArchiveFilename = os.path.join(
        outputDirectory,
        "export",
        f"{baseDirName}_{scanNumber:04d}_{detectorName}_{outputUnitSuffix}.zip",
    )

    integrationOptions: dict[str, Any] = {
        "method": pyfaiMethod,
        "unit": unit,
    }
    if sigmaClippingThreshold is not None:
        integrationOptions["extra_options"] = {
            "thres": sigmaClippingThreshold,
            "max_iter": 10,
            "error_model": "azimuthal",
        }
        integrationOptions["integrator_name"] = "sigma_clip_ng"

    inputs = [
        {
            "task_identifier": "FlatFieldFromEnergy",
            "name": "newflat",
            "value": newFlat,
        },
        {
            "task_identifier": "FlatFieldFromEnergy",
            "name": "oldflat",
            "value": oldFlat,
        },
        {
            "task_identifier": "FlatFieldFromEnergy",
            "name": "energy",
            "value": energy,
        },
        {
            "task_identifier": "PyFaiConfig",
            "name": "filename",
            "value": pyfaiConfig,
        },
        {
            "task_identifier": "PyFaiConfig",
            "name": "integration_options",
            "value": integrationOptions,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "filename",
            "value": datasetFilename,
        },
        {"task_identifier": "IntegrateBlissScan", "name": "scan", "value": scanNumber},
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "output_filename",
            "value": outputFilePathH5,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "monitor_name",
            "value": monitorName,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "reference",
            "value": referenceCounts,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "maximum_persistent_workers",
            "value": 1,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "retry_timeout",
            "value": 3600,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "detector_name",
            "value": detectorName,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "nxprocess_name",
            "value": nxProcessName,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "nxmeasurement_name",
            "value": nxMeasurementName,
        },
        {
            "task_identifier": "IntegrateBlissScan",
            "name": "external_output_filename",
            "value": externalOutputFilePathH5,
        },
        {
            "task_identifier": "SaveNexusPatternsAsAscii",
            "name": "enabled",
            "value": asciiExport,
        },
        {
            "task_identifier": "SaveNexusPatternsAsAscii",
            "name": "output_filename_template",
            "value": outputAsciiFileTemplate,
        },
        {
            "task_identifier": "SaveNexusPatternsAsAscii",
            "name": "output_archive_filename",
            "value": outputArchiveFilename,
        },
        {
            "name": "overwrite",
            "value": True,
            "all": True,
        },
    ]

    inputs += task_inputs(
        task_identifier="SaveNexusPatternsAsId31TomoHdf5",
        inputs={
            "enabled": tomoEnabled,
            "scan_entry_url": tomoScanEntryUrl,
            "rot_name": rotName,
            "y_name": yName,
            "output_filename": tomoOutputFilename,
        },
    )

    return {
        "inputs": inputs,
        "convert_destination": os.path.join(
            outputDirectory,
            f"{baseDirName}_{scanNumber}_{detectorName}_{outputUnitSuffix}.json",
        ),
    }


def extractScanNumber(h5path: str) -> int:
    """
    Extracts the scan number from the h5path from a selected node.

    Example: '/2.1/measurement/p3" -> returns 2'
    """
    parts = h5path.split("/")
    if len(parts) > 1:
        scanNumberPart = parts[1].split(".")[0]
        try:
            return int(scanNumberPart)
        except ValueError:
            pass
    return -1


def generateUniquePath(basePath: str) -> str:
    """
    Generates a unique path by adding an incremantal suffix if necessary.

    Args:
        basePath: Base path (file or directory)

    Returns:
        unique path
    """
    isFile = os.path.isfile(basePath)
    dirName = os.path.dirname(basePath)
    baseName, ext = (
        os.path.splitext(os.path.basename(basePath)) if isFile else (basePath, "")
    )

    parts = baseName.rsplit("_", 1)
    if len(parts) == 2 and parts[1].isdigit():
        baseName, counter = parts[0], int(parts[1]) + 1
    else:
        counter = 1

    generatedName = os.path.join(dirName, f"{baseName}_{counter}{ext}")
    while os.path.exists(generatedName):
        counter += 1
        generatedName = os.path.join(dirName, f"{baseName}_{counter}{ext}")
    return generatedName


def getScanEnergy(h5Filename: str, scanNumber: int) -> Optional[float]:
    """
    Retrieves the energy for a specific scan in an HDF5 file.

    Args:
        h5Filename: Path to the HDF5 file.
        scanNumber: Scan number to retrieve energy for.

    Returns:
        Energy value for a given scan.
    """
    scanPath = f"{scanNumber}.1/instrument/positioners"

    with h5py.File(h5Filename, "r") as h5file:
        scan_group = h5file.get(scanPath)
        if not isinstance(scan_group, h5py.Group):
            return None
        energy_dset = scan_group.get("energy")
        if not isinstance(energy_dset, h5py.Dataset):
            return None
        return energy_dset[()]

    return None


class FilenameCompleterLineEdit(qt.QLineEdit):
    """
    Heritage from QLineEdit widget that provides autocompletion for file paths.

    This widget uses a QFileSystemModel to suggest file and directory paths,
    starting from the root of the filesystem.
    """

    def __init__(self, parent: qt.QWidget | None = None, **kwargs) -> None:
        super().__init__(parent=parent, **kwargs)

        completer = qt.QCompleter()
        model = qt.QFileSystemModel(completer)
        model.setOption(qt.QFileSystemModel.Option.DontWatchForChanges, True)
        model.setRootPath("/")

        completer.setModel(model)
        completer.setCompletionRole(qt.QFileSystemModel.Roles.FileNameRole)
        self.setCompleter(completer)


def get_scan_url(workflow_parameters):
    datasetFilename = None
    scanNumber = None
    for item in workflow_parameters["inputs"]:
        if item.get("task_identifier") != "IntegrateBlissScan":
            continue
        if item["name"] == "filename":
            datasetFilename = item["value"]
        if item["name"] == "scan":
            scanNumber = item["value"]

    return datasetFilename, scanNumber
