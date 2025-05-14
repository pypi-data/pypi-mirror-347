"""Airfoil problem.

Filename convention is that folder paths do not end with /. For example, /path/to/folder is correct, but /path/to/folder/ is not.

             .:-===+=+==-:
     .==.                        .:-++=:....
 .-:                                           .:--:::.
-            Airfoil v.0                        :====--:-===
:-                                    .:==:.
   .-::.                     ::::-:.
          ..::::----::::..

+-+-+-+-+-+-+-+-+-+
|E|n|g|i|B|e|n|c|h|
+-+-+-+-+-+-+-+-+-+
"""

from dataclasses import dataclass
from dataclasses import field
import os
import shutil
from typing import Annotated, Any

from gymnasium import spaces
import numpy as np
import numpy.typing as npt
import pandas as pd

from engibench.constraint import bounded
from engibench.constraint import constraint
from engibench.constraint import IMPL
from engibench.constraint import THEORY
from engibench.core import ObjectiveDirection
from engibench.core import OptiStep
from engibench.core import Problem
from engibench.problems.airfoil.pyopt_history import History
from engibench.problems.airfoil.utils import calc_area
from engibench.problems.airfoil.utils import calc_off_wall_distance
from engibench.problems.airfoil.utils import reorder_coords
from engibench.problems.airfoil.utils import scale_coords
from engibench.utils import container
from engibench.utils.files import clone_dir
from engibench.utils.files import replace_template_values

DesignType = dict[str, Any]


def self_intersect(curve: npt.NDArray[np.float64]) -> tuple[int, npt.NDArray[np.float64], npt.NDArray[np.float64]] | None:
    """Determines if two segments a and b intersect."""
    # intersection: find t such that (p + t dp - q) x dq = 0 with 0 <= t <= 1
    # and (q + s dq - p) x dp = 0, 0 <= s <= 1
    # dp x dq = 0 => parallel => no intersection
    #
    # t = (q-p) x dq / dp x dq
    # s = (q-p) x dp / dp x dq
    #
    # Also use the fact that 2 consecutive segments always intersect (at their common point)
    # => never check consecutive segments
    segments = curve[1:] - curve[:-1]
    n = segments.shape[0]
    for i in range(n - 1):
        p, dp = curve[i], segments[i]
        end = n - 1 if i == 0 else n
        q, dq = curve[i + 2 : end], segments[i + 2 : end]
        x = np.cross(dp, dq)
        parallel = x == 0.0
        t = np.cross(q[~parallel] - p, dq[~parallel]) / x[~parallel]
        s = np.cross(q[~parallel] - p, dp) / x[~parallel]
        if np.any((t >= 0.0) & (t <= 1.0) & (s >= 0.0) & (s <= 1.0)):
            return i, p, curve[i + 1]
    return None


@constraint(categories=IMPL)
def does_not_self_intersect(design: DesignType) -> None:
    """Check if a curve has no self intersections."""
    intersection = self_intersect(design["coords"])
    assert intersection is None, (
        f"design: Curve does self intersect at segment {intersection[0]}: {intersection[1]} -- {intersection[2]}"
    )


class Airfoil(Problem[DesignType]):
    r"""Airfoil 2D shape optimization problem.

    ## Problem Description
    This problem simulates the performance of an airfoil in a 2D environment. An airfoil is represented by a set of 192 points that define its shape. The performance is evaluated by the [MACH-Aero](https://mdolab-mach-aero.readthedocs-hosted.com/en/latest/) simulator that computes the lift and drag coefficients of the airfoil.

    ## Design space
    The design space is represented by a dictionary where one element (`coords`) is a numpy array (vector of 192 x,y coordinates in `[0., 1.)` per design) that define the airfoil shape, and the other element (`angle_of_attack`) is a scalar.

    ## Objectives
    The objectives are defined and indexed as follows:

    0. `cd`: Drag coefficient to minimize.

    ## Conditions
    The conditions are defined by the following parameters:
    - `mach`: Mach number.
    - `reynolds`: Reynolds number.
    - `area_ratio_min`: Minimum area ratio (ratio relative to initial area) constraint.
    - `area_initial`: Initial area.
    - `cl_target`: Target lift coefficient to satisfy equality constraint.

    ## Simulator
    The simulator is a docker container with the MACH-Aero software that computes the lift and drag coefficients of the airfoil. You can install gcc and gfortran on your system with your package manager.
    - On Ubuntu: `sudo apt-get install gcc gfortran`
    - On MacOS: `brew install gcc gfortran`
    - On Windows (WSL): `sudo apt install build-essential`

    ## Dataset
    The dataset linked to this problem is hosted on the [Hugging Face Datasets Hub](https://huggingface.co/datasets/IDEALLab/airfoil_v0).

    ### v0

    #### Fields
    The dataset contains optimal design, conditions, objectives and these additional fields:
    - `initial_design`: Design before the adjoint optimization.
    - `cl_con_violation`: # Constraint violation for coefficient of lift.
    - `area_ratio`: # Area ratio for given design.

    #### Creation Method
    Refer to paper in references for details on how the dataset was created.

    ## References
    If you use this problem in your research, please cite the following paper:
    C. Diniz and M. Fuge, "Optimizing Diffusion to Diffuse Optimal Designs," in AIAA SCITECH 2024 Forum, 2024. doi: 10.2514/6.2024-2013.

    ## Lead
    Cashen Diniz @cashend
    """

    version = 0
    objectives: tuple[tuple[str, ObjectiveDirection], ...] = (("cd", ObjectiveDirection.MINIMIZE),)
    conditions: tuple[tuple[str, Any], ...] = (
        ("mach", 0.8),
        ("reynolds", 1e6),
        ("area_initial", None),
        ("area_ratio_min", 0.7),
        ("cl_target", 0.5),
    )

    design_space = spaces.Dict(
        {
            "coords": spaces.Box(low=0.0, high=1.0, shape=(2, 192), dtype=np.float32),
            "angle_of_attack": spaces.Box(low=0.0, high=10.0, shape=(1,), dtype=np.float32),
        }
    )
    design_constraints = (does_not_self_intersect,)
    dataset_id = "IDEALLab/airfoil_v0"
    container_id = "mdolab/public:u22-gcc-ompi-stable"
    __local_study_dir: str

    @dataclass
    class Config:
        """Structured representation of configuration parameters for a numerical computation."""

        alpha: Annotated[float, bounded(lower=0.0, upper=10.0).category(THEORY)] = 0.0
        area_ratio_min: Annotated[float, bounded(lower=0.0, upper=1.2).category(THEORY)] = 0.7
        area_initial: None | float = None
        mach: Annotated[
            float, bounded(lower=0.0).category(IMPL), bounded(lower=0.1, upper=1.0).warning().category(IMPL)
        ] = 0.8
        reynolds: Annotated[
            float, bounded(lower=0.0).category(IMPL), bounded(lower=1e5, upper=1e9).warning().category(IMPL)
        ] = 1e6
        cl_target: float = 0.5
        altitude: float = 10000.0
        temperature: float = 300.0
        use_altitude: bool = False
        output_dir: str | None = None
        mesh_fname: str | None = None
        task: str = "'analysis'"
        opt: str = "'SLSQP'"
        opt_options: dict = field(default_factory=dict)
        ffd_fname: str | None = None
        area_input_design: float | None = None

        @constraint(categories=THEORY)
        @staticmethod
        def area_ratio_bound(area_ratio_min: float, area_initial: float | None, area_input_design: float | None) -> None:
            """Constraint for area_ratio_min <= area_ratio <= 1.2."""
            area_ratio_max = 1.2
            if area_input_design is None:
                return
            assert area_initial is not None
            area_ratio = area_input_design / area_initial
            assert area_ratio_min <= area_ratio <= area_ratio_max, (
                f"Config.area_ratio: {area_ratio} ∉ [area_ratio_min={area_ratio_min}, 1.2]"
            )

    def __init__(self, base_directory: str | None = None) -> None:
        """Initializes the Airfoil problem.

        Args:
            base_directory (str, optional): The base directory for the problem. If None, the current directory is selected.
        """
        # This is used for intermediate files
        # Local file are prefixed with self.local_base_directory
        if base_directory is not None:
            self.__local_base_directory = base_directory
        else:
            self.__local_base_directory = os.getcwd()
        self.__local_target_dir = self.__local_base_directory + "/engibench_studies/problems/airfoil"
        self.__local_template_dir = (
            os.path.dirname(os.path.abspath(__file__)) + "/templates"
        )  # These templates are shipped with the lib
        self.__local_scripts_dir = os.path.dirname(os.path.abspath(__file__)) + "/scripts"

        # Docker target directory
        # This is used for files that are mounted into the docker container
        self.__docker_base_dir = "/home/mdolabuser/mount/engibench"
        self.__docker_target_dir = self.__docker_base_dir + "/engibench_studies/problems/airfoil"

        super().__init__()

    def reset(self, seed: int | None = None, *, cleanup: bool = False) -> None:
        """Resets the simulator and numpy random to a given seed.

        Args:
            seed (int, optional): The seed to reset to. If None, a random seed is used.
            cleanup (bool): Deletes the previous study directory if True.
        """
        if cleanup:
            shutil.rmtree(self.__local_study_dir)

        super().reset(seed)
        self.current_study = f"study_{self.seed}"
        self.__local_study_dir = self.__local_target_dir + "/" + self.current_study
        self.__docker_study_dir = self.__docker_target_dir + "/" + self.current_study

        clone_dir(source_dir=self.__local_template_dir, target_dir=self.__local_study_dir)

    def __design_to_simulator_input(self, design: DesignType, config: dict[str, Any], filename: str = "design") -> str:
        """Converts a design to a simulator input.

        The simulator inputs are two files: a mesh file (.cgns) and a FFD file (.xyz). This function generates these files from the design.
        The files are saved in the current directory with the name "$filename.cgns" and "$filename_ffd.xyz".

        Args:
            design (dict): The design to convert.
            config (dict): A dictionary with configuration (e.g., boundary conditions) for the simulation.
            filename (str): The filename to save the design to.
        """
        tmp = os.path.join(self.__docker_study_dir, "tmp")

        base_config = {
            "design_fname": f"'{self.__docker_study_dir}/{filename}.dat'",
            "tmp_xyz_fname": f"'{tmp}'",
            "mesh_fname": "'" + self.__docker_study_dir + "/" + filename + ".cgns'",
            "ffd_fname": "'" + self.__docker_study_dir + "/" + filename + "_ffd'",
            "marchDist": 100.0,  # Distance to march the grid from the airfoil surface
            "N_sample": 180,
            "nTEPts": 4,
            "xCut": 0.99,
            "ffd_ymarginu": 0.05,
            "ffd_ymarginl": 0.05,
            "ffd_pts": 10,
            "N_grid": 100,
            "estimate_s0": True,
            "make_input_design_blunt": True,
            "input_blunted": False,
        }

        # Calculate the off-the-wall distance
        if base_config["estimate_s0"]:
            s0 = calc_off_wall_distance(
                mach=config["mach"], reynolds=config["reynolds"], freestreamTemp=config["temperature"]
            )
        else:
            s0 = 1e-5

        base_config["s0"] = s0

        # Adds the boundary conditions to the configuration
        base_config.update(self.conditions)

        # Scale the design to fit in the design space
        scaled_design, input_blunted = scale_coords(
            design["coords"],
            blunted=bool(base_config["input_blunted"]),
            xcut=base_config["xCut"],  # type: ignore[arg-type]
        )
        base_config["input_blunted"] = input_blunted

        # Save the design to a temporary file. Format to 1e-6 rounding
        np.savetxt(self.__local_study_dir + "/" + filename + ".dat", scaled_design.transpose())

        # Prepares the preprocess.py script with the design
        replace_template_values(
            self.__local_study_dir + "/pre_process.py",
            base_config,
        )

        # Launches a docker container with the pre_process.py script
        # The script generates the mesh and FFD files
        try:
            bash_command = (
                "source ~/.bashrc_mdolab && cd /home/mdolabuser/mount/engibench && python "
                + self.__docker_study_dir
                + "/pre_process.py"
                + " > "
                + self.__docker_study_dir
                + "/output_preprocess.log"
            )
            assert self.container_id is not None, "Container ID is not set"
            container.run(
                command=["/bin/bash", "-c", bash_command],
                image=self.container_id,
                name="machaero",
                mounts=[(self.__local_base_directory, self.__docker_base_dir)],
            )

        except Exception as e:
            # Verify output files exist
            mesh_file = self.__local_study_dir + "/" + filename + ".cgns"
            ffd_file = self.__local_study_dir + "/" + filename + "_ffd.xyz"
            msg = ""

            if not os.path.exists(mesh_file):
                msg += f"Mesh file not generated: {mesh_file}."
            if not os.path.exists(ffd_file):
                msg += f"FFD file not generated: {ffd_file}."
            raise RuntimeError(f"Pre-processing failed: {e!s}. {msg} Check logs in {self.__local_study_dir}") from e

        return filename

    def simulator_output_to_design(self, simulator_output: str | None = None) -> npt.NDArray[np.float32]:
        """Converts a simulator output to a design.

        Args:
            simulator_output (str): The simulator output to convert. If None, the latest slice file is used.

        Returns:
            np.ndarray: The corresponding design.
        """
        if simulator_output is None:
            # Take latest slice file
            files = os.listdir(self.__local_study_dir + "/output")
            files = [f for f in files if f.endswith("_slices.dat")]
            file_numbers = [int(f.split("_")[1]) for f in files]
            simulator_output = files[file_numbers.index(max(file_numbers))]

        slice_file = self.__local_study_dir + "/output/" + simulator_output

        # Define the variable names for columns
        var_names = [
            "CoordinateX",
            "CoordinateY",
            "CoordinateZ",
            "XoC",
            "YoC",
            "ZoC",
            "VelocityX",
            "VelocityY",
            "VelocityZ",
            "CoefPressure",
            "Mach",
        ]

        nelems = pd.read_csv(
            slice_file, sep=r"\s+", names=["fill1", "Nodes", "fill2", "Elements", "ZONETYPE"], skiprows=3, nrows=1
        )
        nnodes = int(nelems["Nodes"].iloc[0])

        # Read the main data and node connections
        slice_df = pd.read_csv(slice_file, sep=r"\s+", names=var_names, skiprows=5, nrows=nnodes, engine="c")
        nodes_arr = pd.read_csv(slice_file, sep=r"\s+", names=["NodeC1", "NodeC2"], skiprows=5 + nnodes, engine="c")

        # Concatenate node connections to the main data
        slice_df = pd.concat([slice_df, nodes_arr], axis=1)

        return reorder_coords(slice_df)

    def simulate(self, design: DesignType, config: dict[str, Any] | None = None, mpicores: int = 4) -> npt.NDArray:
        """Simulates the performance of an airfoil design.

        Args:
            design (dict): The design to simulate.
            config (dict): A dictionary with configuration (e.g., boundary conditions, filenames) for the simulation.
            mpicores (int): The number of MPI cores to use in the simulation.

        Returns:
            dict: The performance of the design - each entry of the dict corresponds to a named objective value.
        """
        # docker pull image if not already pulled
        if container.RUNTIME is not None and self.container_id is not None:
            container.pull(self.container_id)
        # pre-process the design and run the simulation

        # Prepares the airfoil_analysis.py script with the simulation configuration
        base_config = {
            "alpha": design["angle_of_attack"],
            "altitude": 10000,
            "temperature": 300,
            "use_altitude": False,
            "output_dir": "'" + self.__docker_study_dir + "/output/'",
            "mesh_fname": "'" + self.__docker_study_dir + "/design.cgns'",
            "task": "'analysis'",
            **dict(self.conditions),
            **(config or {}),
        }
        self.__design_to_simulator_input(design, base_config)
        replace_template_values(
            self.__local_study_dir + "/airfoil_analysis.py",
            base_config,
        )

        # Launches a docker container with the airfoil_analysis.py script
        # The script takes a mesh and ffd and performs an optimization
        try:
            bash_command = (
                "source ~/.bashrc_mdolab && cd /home/mdolabuser/mount/engibench && mpirun -np "
                + str(mpicores)
                + " python "
                + self.__docker_study_dir
                + "/airfoil_analysis.py > "
                + self.__docker_study_dir
                + "/output.log"
            )
            assert self.container_id is not None, "Container ID is not set"
            container.run(
                command=["/bin/bash", "-c", bash_command],
                image=self.container_id,
                name="machaero",
                mounts=[(self.__local_base_directory, self.__docker_base_dir)],
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to run airfoil analysis: {e!s}. Please check logs in {self.__local_study_dir}."
            ) from e

        outputs = np.load(self.__local_study_dir + "/output/outputs.npy")
        lift = float(outputs[3])
        drag = float(outputs[4])
        return np.array([drag, lift])

    def optimize(
        self, starting_point: DesignType, config: dict[str, Any] | None = None, mpicores: int = 4
    ) -> tuple[DesignType, list[OptiStep]]:
        """Optimizes the design of an airfoil.

        Args:
            starting_point (dict): The starting point for the optimization.
            config (dict): A dictionary with configuration (e.g., boundary conditions, filenames) for the optimization.
            mpicores (int): The number of MPI cores to use in the optimization.

        Returns:
            tuple[dict[str, Any], list[OptiStep]]: The optimized design and its performance.
        """
        # docker pull image if not already pulled
        if container.RUNTIME is not None and self.container_id is not None:
            container.pull(self.container_id)
        # pre-process the design and run the simulation
        filename = "candidate_design"

        # Prepares the optimize_airfoil.py script with the optimization configuration
        base_config = {
            "cl_target": 0.5,
            "alpha": starting_point["angle_of_attack"],
            "mach": 0.75,
            "reynolds": 1e6,
            "altitude": 10000,
            "temperature": 300,  # should specify either mach + altitude or mach + reynolds + reynoldsLength (default to 1) + temperature
            "use_altitude": False,
            "area_initial": None,  # actual initial airfoil area
            "area_ratio_min": 0.7,  # Minimum ratio the initial area is allowed to decrease to i.e minimum_area = area_initial*area_target
            "opt": "'SLSQP'",
            "opt_options": {},
            "output_dir": "'" + self.__docker_study_dir + "/output/'",
            "ffd_fname": "'" + self.__docker_study_dir + "/" + filename + "_ffd.xyz'",
            "mesh_fname": "'" + self.__docker_study_dir + "/" + filename + ".cgns'",
            "area_input_design": calc_area(starting_point["coords"]),
            **dict(self.conditions),
            **(config or {}),
        }
        self.__design_to_simulator_input(starting_point, base_config, filename)
        replace_template_values(
            self.__local_study_dir + "/airfoil_opt.py",
            base_config,
        )

        try:
            # Launches a docker container with the optimize_airfoil.py script
            # The script takes a mesh and ffd and performs an optimization
            bash_command = (
                "source ~/.bashrc_mdolab && cd /home/mdolabuser/mount/engibench && mpirun -np "
                + str(mpicores)
                + " python "
                + self.__docker_study_dir
                + "/airfoil_opt.py > "
                + self.__docker_study_dir
                + "/airfoil_opt.log"
            )
            assert self.container_id is not None, "Container ID is not set"
            container.run(
                command=["/bin/bash", "-c", bash_command],
                image=self.container_id,
                name="machaero",
                mounts=[(self.__local_base_directory, self.__docker_base_dir)],
            )
        except Exception as e:
            raise RuntimeError(f"Optimization failed: {e!s}. Check logs in {self.__local_study_dir}") from e

        # post process -- extract the shape and objective values
        optisteps_history = []
        history = History(self.__local_study_dir + "/output/opt.hst")
        iters = list(map(int, history.getCallCounters()[:]))

        for i in range(len(iters)):
            vals = history.read(int(iters[i]))
            if vals is not None and "funcs" in vals and "obj" in vals["funcs"] and not vals["fail"]:
                objective = history.getValues(names=["obj"], callCounters=[i], allowSens=False, major=False, scale=True)[
                    "obj"
                ]
                optisteps_history.append(OptiStep(obj_values=np.array(objective), step=vals["iter"]))

        history.close()

        opt_coords = self.simulator_output_to_design()

        return {"coords": opt_coords, "angle_of_attack": starting_point["angle_of_attack"]}, optisteps_history

    def render(self, design: DesignType, *, open_window: bool = False, save: bool = False) -> Any:
        """Renders the design in a human-readable format.

        Args:
            design (dict): The design to render.
            open_window (bool): If True, opens a window with the rendered design.
            save (bool): If True, saves the rendered design to a file in the study directory.

        Returns:
            Any: The rendered design.
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        coords = design["coords"]
        alpha = design["angle_of_attack"]
        ax.scatter(coords[0], coords[1], s=10, alpha=0.7)
        ax.set_title(r"$\alpha$=" + str(np.round(alpha, 2)) + r"$^\circ$")
        ax.axis("equal")
        ax.axis("off")
        ax.set_xlim((-0.005, 1.005))

        if open_window:
            plt.show()
        if save:
            plt.savefig(self.__local_study_dir + "/airfoil.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        return fig, ax

    def render_optisteps(self, optisteps_history: list[OptiStep], *, open_window: bool = False, save: bool = False) -> Any:
        """Renders the optimization step history.

        Args:
            optisteps_history (list[OptiStep]): The optimization steps to render.
            open_window (bool): If True, opens a window with the rendered design.
            save (bool): If True, saves the rendered design to a file in the study directory.

        Returns:
            Any: Rendered optimization step history.
        """
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        steps = np.array([step.step for step in optisteps_history])
        objectives = np.array([step.obj_values[0][0] for step in optisteps_history])
        ax.plot(steps, objectives, label="Drag Coefficient")
        ax.set_title("Optimization Steps")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Drag counts")
        if open_window:
            plt.show()
        if save:
            plt.savefig(self.__local_study_dir + "/optisteps.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        return fig, ax

    def random_design(self, dataset_split: str = "train", design_key: str = "initial_design") -> tuple[dict[str, Any], int]:
        """Samples a valid random initial design.

        Args:
            dataset_split (str): The key to use for the dataset. Defaults to "train".
            design_key (str): The key to use for the design in the dataset.
                Defaults to "initial_design".

        Returns:
            tuple[dict[str, Any], int]: The valid random design and the index of the design in the dataset.
        """
        rnd = self.np_random.integers(low=0, high=len(self.dataset[dataset_split][design_key]), dtype=int)
        initial_design = self.dataset[dataset_split][design_key][rnd]
        return {"coords": np.array(initial_design["coords"]), "angle_of_attack": initial_design["angle_of_attack"]}, rnd


if __name__ == "__main__":
    # Initialize the problem
    problem = Airfoil()
    problem.reset(seed=0, cleanup=True)

    # Retrieve the dataset
    dataset = problem.dataset

    # Get random initial design and optimized conditions from the dataset + the index
    design, idx = problem.random_design()

    # Get the config conditions from the dataset
    config = dataset["train"].select_columns(problem.conditions_keys)[idx]

    # Simulate the design
    print(problem.simulate(design, config=config, mpicores=8))

    # Cleanup the study directory; will delete the previous contents from simulate in this case
    problem.reset(seed=0, cleanup=False)

    # Get design and conditions from the dataset, render design
    opt_design, optisteps_history = problem.optimize(design, config=config, mpicores=8)

    # Render the final optimized design
    problem.render(opt_design, open_window=False, save=True)
