from dataclasses import dataclass
import logging

import os
import h5py
import numpy
from silx.io.nxdata import NXdata

from ewoksxrpd.tasks.data_access import TaskWithDataAccess
from ewoksxrpd.tasks.utils.ascii_utils import ensure_parent_folder


logger = logging.getLogger(__name__)


@dataclass
class IntegratedPatterns:
    """Store multiple pyFAI integrated patterns"""

    radial: numpy.ndarray
    radial_name: str
    radial_units: str
    intensities: numpy.ndarray


class SaveNexusPatternsAsId31TomoHdf5(
    TaskWithDataAccess,
    input_names=[
        "scan_entry_url",
        "rot_name",
        "y_name",
        "nxdata_url",
        "output_filename",
    ],
    optional_input_names=["enabled", "overwrite"],
    output_names=["filename"],
):
    """Save integrated XRD patterns into an HDF5 file compatible with ID31 tomography workflow.

    Inputs:
    - scan_entry_url (str): HDF5 URL to the NXentry group containing the "measurement" group.
    - rot_name (str): Dataset name in "measurement" for rotation angles (e.g. "nth").
    - y_name (str): Dataset name in "measurement" for horizontal positions (e.g. "ny").
    - nxdata_url (str): HDF5 URL to the NXdata group containing integrated patterns.
    - output_filename (str): Path to the output HDF5 file.

    Optional inputs:
    - enabled (bool | Optional): True to enable saving, False to skip task (default: True).

    Output:
    - filename (str): Path to the written HDF5 file, or empty string if skipped.
    """

    def run(self):
        if not self.get_input_value("enabled", True):
            logger.info(
                f"Task {self.__class__.__qualname__} is disabled: No file is saved"
            )
            self.outputs.filename = ""
            return

        output_filename = self.inputs.output_filename
        ensure_parent_folder(output_filename)

        with self.open_h5item(self.inputs.scan_entry_url) as scan_entry:
            measurement = scan_entry["measurement"]

            th_angles_dataset = measurement[self.inputs.rot_name]
            th_angles = th_angles_dataset[()]
            th_angles_units = th_angles_dataset.attrs.get("units", None)

            y_positions_dataset = measurement[self.inputs.y_name]
            y_positions = y_positions_dataset[()]
            y_positions_units = y_positions_dataset.attrs.get("units", None)

        with self.open_h5item(self.inputs.nxdata_url) as group:
            patterns = _read_nexus_integrated_patterns(group)

        if self.get_input_value("overwrite", False):
            mode = "w"
        else:
            mode = "a"

        if os.path.exists(output_filename) and not self.get_input_value(
            "overwrite", False
        ):
            raise FileExistsError(
                f"{output_filename} already exists. Use overwrite=True to replace it."
            )

        with h5py.File(output_filename, mode) as h5f:
            h5f["XRD"] = patterns.intensities

            h5f[patterns.radial_name] = patterns.radial
            if patterns.radial_units:
                h5f[patterns.radial_name].attrs["units"] = patterns.radial_units

            h5f["y"] = y_positions
            if y_positions_units is not None:
                h5f["y"].attrs["units"] = y_positions_units

            h5f["th"] = th_angles
            if th_angles_units is not None:
                h5f["th"].attrs["units"] = th_angles_units

        self.outputs.filename = output_filename


def _read_nexus_integrated_patterns(group: h5py.Group) -> IntegratedPatterns:
    """Read integrated patterns from a HDF5 NXdata group.

    It reads from both single (1D signal) or multi (2D signal) NXdata.
    """
    nxdata = NXdata(group)
    if not nxdata.is_valid:
        raise RuntimeError(
            f"Cannot parse NXdata group: {group.file.filename}::{group.name}"
        )
    if not (nxdata.signal_is_1d or nxdata.signal_is_2d):
        raise RuntimeError(
            f"Signal is not a 1D or 2D dataset: {group.file.filename}::{group.name}"
        )

    if nxdata.axes[-1] is None:
        radial = numpy.arange(nxdata.signal.shape[-1])
        radial_name = "radial"
        radial_units = ""
    else:
        axis_dataset = nxdata.axes[-1]
        radial = axis_dataset[()]
        radial_name = nxdata.axes_dataset_names[-1]
        radial_units = axis_dataset.attrs.get("units", "")

    intensities = numpy.atleast_2d(nxdata.signal)

    return IntegratedPatterns(radial, radial_name, radial_units, intensities)
