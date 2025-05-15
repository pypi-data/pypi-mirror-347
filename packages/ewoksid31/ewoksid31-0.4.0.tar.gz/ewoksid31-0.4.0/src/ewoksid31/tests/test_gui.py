import json
from dataclasses import dataclass
from pathlib import Path

import numpy
import pytest
import scipy.io

from ..app.integrate.id31_pyfai_ewoks import Id31FAIEwoksMainWindow
from .conftest import DETECTOR_SHAPE


@dataclass
class DummyH5Node:
    physical_filename: str
    physical_name: str


PONI = {
    "application": "pyfai-integrate",
    "version": 3,
    "wavelength": 1.6531226457760035e-11,
    "dist": 1.014612139238891,
    "poni1": 0.21340662994315895,
    "poni2": 0.13912764384981186,
    "rot1": -0.004822100080733148,
    "rot2": 0.0005542810978441514,
    "rot3": 0.0,
    "detector": "Pilatus_CdTe_2M",
}


def _create_flats(flat_dir: Path, n=5):
    energy = numpy.linspace(0, 10, n)
    flat = numpy.ones((*DETECTOR_SHAPE, n))
    scipy.io.savemat(flat_dir / "flats.mat", mdict={"E": energy, "F": flat})
    scipy.io.savemat(flat_dir / "flats_old.mat", mdict={"Eold": energy, "Fold": flat})


@pytest.mark.parametrize("overwrite", (True, False))
def test_integrate(qtbot, tmp_path, tomo_p3_scan, overwrite):
    window = Id31FAIEwoksMainWindow()
    qtbot.addWidget(window)

    with open(tmp_path / "config.json", "w") as cfg:
        json.dump(PONI, cfg)
    window.setConfigFilePath(str(tmp_path / "config.json"))

    _create_flats(tmp_path)
    window.setFlatFieldDirName(tmp_path)

    window._2thCheckBox.click()
    window._outputWidget.setTomoEnabled(False)

    output_dir = tmp_path / "PROCESSED_DATA"
    output_dir.mkdir()
    window._outputWidget.setOutputDirName(output_dir)

    integration_output_file = output_dir / f"{tomo_p3_scan.stem}.h5"

    # Launch processing manually (could be done via the GUI later)
    scan = DummyH5Node(physical_filename=str(tomo_p3_scan), physical_name="/2.1")
    inputParameters = window._prepareScans([scan])

    window._executeWorkflowForParams(inputParameters)
    inputParameters[0]["inputs"].append(
        {"name": "overwrite", "value": overwrite, "all": True}
    )

    # Try to overwrite the files just created
    if overwrite:
        window._executeWorkflowForParams(inputParameters)
    else:
        with pytest.raises(RuntimeError) as exc:
            window._executeWorkflowForParams(inputParameters)
        original_exc = exc.value.__cause__
        assert isinstance(original_exc, ValueError)
        assert (
            str(original_exc)
            == "Unable to synchronously create group (name already exists)"
        )

    assert integration_output_file.exists()
