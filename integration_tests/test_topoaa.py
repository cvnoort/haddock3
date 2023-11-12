import tempfile
from pathlib import Path

import pytest

from haddock.modules.topology.topoaa import DEFAULT_CONFIG as DEFAULT_TOPOAA_CONFIG
from haddock.modules.topology.topoaa import HaddockModule as TopoaaModule

from . import CNS_EXEC, DATA_DIR, has_cns


@pytest.fixture
def topoaa_module():
    with tempfile.TemporaryDirectory() as tmpdir:
        topoaa = TopoaaModule(
            order=0, path=tmpdir, initial_params=DEFAULT_TOPOAA_CONFIG
        )
        topoaa.__init__(path=tmpdir, order=0)
        topoaa.params["molecules"] = [
            Path(DATA_DIR, "docking-protein-protein/data/e2aP_1F3G.pdb"),
            Path(DATA_DIR, "docking-protein-protein/data/hpr_ensemble.pdb"),
        ]
        topoaa.params["mol1"] = {"prot_segid": "A"}
        topoaa.params["mol2"] = {"prot_segid": "B"}

        topoaa.params["cns_exec"] = CNS_EXEC

        yield topoaa


@has_cns
def test_topoaa_default(topoaa_module):
    """Test the topoaa module."""

    topoaa_module.run()

    expected_inp = Path(topoaa_module.path, "e2aP_1F3G.inp")
    expected_psf = Path(topoaa_module.path, "e2aP_1F3G_haddock.psf")
    expected_pdb = Path(topoaa_module.path, "e2aP_1F3G_haddock.pdb")
    expected_gz = Path(topoaa_module.path, "e2aP_1F3G.out.gz")

    assert expected_inp.exists(), f"{expected_inp} does not exist"
    assert expected_psf.exists(), f"{expected_psf} does not exist"
    assert expected_gz.exists(), f"{expected_gz} does not exist"
    assert expected_pdb.exists(), f"{expected_pdb} does not exist"

    assert expected_inp.stat().st_size > 0, f"{expected_inp} is empty"

    for i in range(1, 10 + 1):
        expected_inp = Path(topoaa_module.path, f"hpr_ensemble_{i}.inp")
        expected_psf = Path(topoaa_module.path, f"hpr_ensemble_{i}_haddock.psf")
        expected_pdb = Path(topoaa_module.path, f"hpr_ensemble_{i}_haddock.pdb")
        expected_gz = Path(topoaa_module.path, f"hpr_ensemble_{i}.out.gz")

        assert expected_inp.exists(), f"{expected_inp} does not exist"
        assert expected_psf.exists(), f"{expected_psf} does not exist"
        assert expected_pdb.exists(), f"{expected_pdb} does not exist"
        assert expected_gz.exists(), f"{expected_gz} does not exist"

        assert expected_inp.stat().st_size > 0, f"{expected_inp} is empty"
        assert expected_psf.stat().st_size > 0, f"{expected_psf} is empty"
        assert expected_pdb.stat().st_size > 0, f"{expected_pdb} is empty"
        assert expected_gz.stat().st_size > 0, f"{expected_gz} is empty"
