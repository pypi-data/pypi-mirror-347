import json

import numpy
import pytest

from ..tasks.multi_geometry_integrate import Integrate2DMultiGeometry
from . import xrpd_theory


@pytest.fixture
def gonio_file(tmp_path):
    gonio_json = {
        "content": "Goniometer calibration v2",
        "detector": "Pilatus1M",
        "wavelength": 2.6379616687914948e-11,
        "param": [
            2.0062960356379422,
            0.015883422992655393,
            0.8216006393975213,
            0.002164173240804926,
            -0.0031180017089310853,
            0.0063336570464145835,
            0.004297460651999008,
        ],
        "param_names": ["dist", "poni1", "poni2", "rot1", "rot2", "rot_x", "rot_y"],
        "pos_names": ["pos"],
        "trans_function": {
            "content": "GeometryTransformation",
            "param_names": ["dist", "poni1", "poni2", "rot1", "rot2", "rot_x", "rot_y"],
            "pos_names": ["pos"],
            "dist_expr": "dist",
            "poni1_expr": "poni1 + rot_x*cos(pos) - rot_y*sin(pos)",
            "poni2_expr": "poni2 + rot_x*sin(pos) + rot_y*cos(pos)",
            "rot1_expr": "+rot1*cos(pos) - rot2*sin(pos)",
            "rot2_expr": "+rot1*sin(pos) + rot2*cos(pos)",
            "rot3_expr": "pos",
            "constants": {"pi": 3.141592653589793},
        },
    }
    filename = tmp_path / "gonio.json"
    with open(filename, "w") as f:
        json.dump(gonio_json, f)

    return filename


def test_multi_geometry_task(imageSetup1Calibrant1, gonio_file):
    assert isinstance(imageSetup1Calibrant1, xrpd_theory.Calibration)
    images = numpy.zeros(shape=(10, *imageSetup1Calibrant1.image.shape))
    for i in range(10):
        images[i] = imageSetup1Calibrant1.image

    task = Integrate2DMultiGeometry(
        inputs={
            "goniometer_file": gonio_file,
            "integration_options": {"npt_rad": 300, "npt_azim": 180},
            "images": images,
            "positions": [*numpy.linspace(0, 360, 10)],
        }
    )

    task.execute()

    assert task.get_output_value("radial").shape == (300,)
    assert task.get_output_value("azimuthal").shape == (180,)
    assert task.get_output_value("intensity").shape == (180, 300)
