import yaml
import json
from pathlib import Path
import sqlite3
import pandas as pd  # for loading glossary parquet

# --- Lamini experiment primitives ------------------------------------------
from lamini.experiment.pipeline.base_agentic_pipeline import BaseAgenticPipeline
from lamini.experiment import BaseMemoryExperiment


from lamini.experiment.validators import SQLValidator


def build_experiment_pipeline(ExperimentDefinition: dict):
    """
    Assemble an agentic pipeline from the JSON stored at
    ExperimentDefinition["pipeline"]["path"], patching db_params to point to the
    first *.sqlite file in the project’s data folder.

    Returns a dict with:
        - pipeline      : the BaseAgenticPipeline instance
        - generators    : pipeline.generators   (dict[str, BaseGenerator])
        - validators    : pipeline.validators   (dict[str, BaseValidator])
        - experiment    : BaseMemoryExperiment wrapper
        - schema        : raw DB schema string
    """

    # ------------------------------------------------------------------ #
    # locate project and DB                                              #
    # ------------------------------------------------------------------ #
    project_dir = Path("projects") / ExperimentDefinition["project_name"]
    proj_path = project_dir / "ymls" / "project.yml"

    with proj_path.open() as f:
        project_file = yaml.safe_load(f)

    data_dir = project_dir / "data"
    sqlite_files = list(data_dir.glob("*.sqlite"))
    if not sqlite_files:
        raise FileNotFoundError("No *.sqlite files found in project data folder.")

    db_path = sqlite_files[0]

    # extract schema text
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        db_schema = "\n".join(row[0] for row in cursor.fetchall())

    # ------------------------------------------------------------------ #
    # load + patch pipeline JSON                                         #
    # ------------------------------------------------------------------ #
    pipeline_json_path = ExperimentDefinition["pipeline"]["path"]
    with open(pipeline_json_path, "r") as f:
        pipeline_cfg = json.load(f)

    # patch db_params → absolute path to first sqlite
    db_params_str = str(db_path)
    for group in ("generators", "validators"):
        for step_cfg in pipeline_cfg.get(group, {}).values():
            if "db_params" in step_cfg:
                step_cfg["db_params"] = db_params_str

    # build the pipeline
    pipeline = BaseAgenticPipeline.from_json(pipeline_cfg)

    # ------------------------------------------------------------------ #
    # wrap in BaseMemoryExperiment (unchanged)                           #
    # ------------------------------------------------------------------ #
    experiment = BaseMemoryExperiment(agentic_pipeline=pipeline)

    # ------------------------------------------------------------------ #
    # return richer bundle                                               #
    # ------------------------------------------------------------------ #
    return {
        "pipeline": pipeline,
        "generators": pipeline.generators,
        "validators": pipeline.validators,
        "experiment": experiment,
        "schema": db_schema,
    }
