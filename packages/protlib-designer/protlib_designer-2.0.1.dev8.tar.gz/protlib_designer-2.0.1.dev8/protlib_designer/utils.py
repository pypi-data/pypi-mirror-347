import json
import sys
from pathlib import Path

import pandas as pd

from protlib_designer import logger

amino_acids = [
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
]

aromatic_amino_acids = [
    "F",
    "Y",
    "W",
]


def format_and_validate_parameters(
    output_folder,
    data,
    min_mut,
    max_mut,
    nb_iterations,
    forbidden_aa,
    max_arom_per_seq,
    dissimilarity_tolerance,
    interleave_mutant_order,
    force_mutant_order_balance,
    schedule,
    schedule_param,
    objective_constraints,
    objective_constraints_param,
    weighted_multi_objective,
    debug,
    data_normalization,
):
    """Format and validate the parameters.

    Parameters
    ----------
    data : str
        The path to the data file.
    nb_iterations : int
        The number of iterations to run.
    forbidden_aa : str
        The forbidden amino acids.
    max_arom_per_seq : int
        The maximum number of aromatic amino acids per sequence.
    schedule : int
        The schedule to use.
    schedule_param : str
        The scheduling parameters.
    objective_constraints : str
        The objective constraints.
    objective_constraints_param : str
        The objective constraints parameters.
    """
    if nb_iterations > 5000:
        logger.warning("Maximum number of iterations is 5000. Setting to 5000.")
        nb_iterations = 5000

    if forbidden_aa is not None:
        forbidden_aa = [x.strip() for x in forbidden_aa.split(",")]
        logger.info(f"Forbidden amino acids: {forbidden_aa}")
    else:
        forbidden_aa = []

    if max_arom_per_seq is not None and max_arom_per_seq < 0:
        logger.error("max_arom_per_seq must be a positive integer.")
        exit()

    if schedule_param is not None:
        schedule_param = [int(val) for val in schedule_param.split(",")]
    else:
        schedule_param = []
    validate_schedule_param(schedule, schedule_param)

    if objective_constraints is not None:
        objective_constraints = objective_constraints.split(",")
    else:
        objective_constraints = []

    if objective_constraints_param is not None:
        objective_constraints_param = [
            float(val) for val in objective_constraints_param.split(",")
        ]
    else:
        objective_constraints_param = []
    validate_objective_constraints(objective_constraints, objective_constraints_param)

    data_df = pd.read_csv(data)
    validate_data(data_df)

    return {
        "output_folder": output_folder,
        "data": data,
        "min_mut": min_mut,
        "max_mut": max_mut,
        "nb_iterations": nb_iterations,
        "forbidden_aa": forbidden_aa,
        "max_arom_per_seq": max_arom_per_seq,
        "dissimilarity_tolerance": dissimilarity_tolerance,
        "interleave_mutant_order": interleave_mutant_order,
        "force_mutant_order_balance": force_mutant_order_balance,
        "schedule": schedule,
        "schedule_param": schedule_param,
        "objective_constraints": objective_constraints,
        "objective_constraints_param": objective_constraints_param,
        "weighted_multi_objective": weighted_multi_objective,
        "debug": debug,
        "data_normalization": data_normalization,
    }, data_df


def validate_data(df: pd.DataFrame):
    """Validate the data file. The data file must have the following columns:
    Mutation, Target1, Target2, ..., TargetN

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing the data.
    """
    if "Mutation" not in df.columns:
        logger.error("Data file must have a Mutation column.")
        sys.exit(2)

    if len(df.columns) < 2:
        logger.error(
            "Data file must have at minimum the Mutation column and at least one Objective/Target."
        )
        sys.exit(3)


def validate_schedule_param(schedule: int, schedule_param: list):
    """Validate the scheduling parameters.

    Parameters
    ----------
    schedule : int
        The schedule to use.
    schedule_param : list
        The scheduling parameters.
    """
    if schedule == 0 and schedule_param:
        logger.error(
            "Scheduling = 0 needs no parameters. Please use 'schedule-param = none'."
        )
        exit()

    if schedule == 1 and len(schedule_param) != 2:
        logger.error(
            "Scheduling = 1 need 2 parameters in the form 'p0,p1'. p0 : Number of iterations to kill the commonest \
                mutation. p1 : Number of iterations to kill the commonest positions."
        )
        exit()

    if schedule == 2 and len(schedule_param) != 2:
        logger.error(
            "Scheduling = 2 need 2 parameters in the form 'p0,p1'. p0 : Number of occurrences of mutation to kill it. \
                p1 : Number of occurrences of position to kill it"
        )
        exit()


def validate_objective_constraints(
    objectives_constraints: list, objectives_constraints_param: list
):
    """Validate the objective constraints.

    Parameters
    ----------
    objectives_constraints : list
        The list of objective constraints.
    objectives_constraints_param : list
        The list of parameters for the objective constraints.
    """
    if len(objectives_constraints) != len(objectives_constraints_param):
        logger.error(
            "Number of objective constraint parameters does not match number of objective constraints"
        )
        exit()


def parse_mutation(mutation: str):
    """Parse wild-type, position, mutated amino acid information
    from compact mutation notation.

    Parameters
    ----------
    mutation : str

    Returns
    -------
    Tuple
        (WT, pos, mutation) as str values.

    """
    return mutation[0], mutation[1:-1], mutation[-1]


def extract_mutation_key(mutationbreak: str):
    """Extract the mutation key from the mutationbreak string.

    Parameters
    ----------
    mutationbreak : str
        The mutationbreak string.
    """
    chars = list(mutationbreak)  # Convert string to list of chars.
    return f"{chars[1]}_{chars[2]}"


def write_config(config: dict, output_dir: Path):
    """Write the parameters used to execute the program to disk.

    Parameters
    ----------
    config : dict
        The parameters used to execute the program.
    output_dir : str
        The output directory to write the config file to.
    """
    filepath = output_dir / "config.json"

    with open(filepath, "w") as fp:
        json.dump(config, fp, indent=4)
