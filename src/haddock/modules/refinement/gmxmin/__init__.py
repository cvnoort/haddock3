"""HADDOCK3 GROMACS minimization module."""
from os import linesep
from pathlib import Path

from haddock.gear.haddockmodel import HaddockModel
from haddock.libs.libcns import prepare_cns_input, prepare_expected_pdb
from haddock.libs.libontology import ModuleIO, PDBFile
from haddock.libs.libsubprocess import JobInputFirst
from haddock.modules import get_engine
from haddock.modules import BaseHaddockModule


RECIPE_PATH = Path(__file__).resolve().parent
DEFAULT_CONFIG = Path(RECIPE_PATH, "defaults.yaml")


class HaddockModule(BaseHaddockModule):
    """HADDOCK3 module to perform minimization with GROMACS."""

    name = RECIPE_PATH.name

    def __init__(
            self,
            order,
            path,
            *ignore,
            init_params=DEFAULT_CONFIG,
            **everything,
            ):
        super().__init__(order, path, init_params)

    @classmethod
    def confirm_installation(cls):
        """Confirm module is installed."""
        # TODO:
        return

    def _run(self):
        """Execute module."""
        models_to_minimize = self.previous_io.retrieve_models(individualize=True)

        models_minimized = []
        jobs = []
        for idx, model in enumerate(models_to_minimize, start=1):
            output_pdb_fname = PDBFile(f"{self.name}_{idx}.pdb", path=self.path)
            models_minimized.append(output_pdb_fname)
            job = JobInputFirst(model.rel_path, Path("out"), "cp", output_pdb_fname.rel_path)
            jobs.append(job)

        self.log(f"Running minimization jobs n={len(jobs)}")
        Engine = get_engine(self.params['mode'], self.params)
        engine = Engine(jobs)
        engine.run()
        self.log("jobs have finished")

        # Save module information
        io = ModuleIO()
        io.add(models_minimized, "o")
        faulty = io.check_faulty()
        tolerance = self.params["tolerance"]
        if faulty > tolerance:
            _msg = (
                f"{faulty:.2f}% of output was not generated for this module "
                f"and tolerance was set to {tolerance:.2f}%.")
            self.finish_with_error(_msg)
        io.save()
