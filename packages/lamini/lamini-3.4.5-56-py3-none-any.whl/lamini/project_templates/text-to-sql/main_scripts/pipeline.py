import os
from tqdm import tqdm
import argparse
import sys
import pandas as pd
import logging
from pathlib import Path
import yaml
import types
import json
from lamini.experiment.pipeline.base_agentic_pipeline import BaseAgenticPipeline
from lamini.experiment.generators import (
    SubQuestionSQLGenerator,
    BaseSQLGenerator,
    SchemaToSQLGenerator,
)
import types, json, re
from lamini.experiment.validators.sql_validator import SQLValidator
from lamini.experiment.generators.sql_debugger_generator import SQLDebuggerGenerator

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from lamini.experiment.base_experiment_object import ExperimentObject
from models.project.projectdb import ProjectDB
from main_scripts.experiment_prep import build_experiment_pipeline
from utils.utils import build_prompts_from_dataframe, save_results
import re
from datetime import datetime
import uuid
import types
from copy import deepcopy
from lamini.generation.base_prompt_object import PromptObject


def generate_experiment_id():
    """Generate a unique experiment ID using timestamp and UUID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}"


def get_experiment_config(
    experiment_name,
    project_name,
    description,
    data_dir="data",
    results_dir="experiment_results",
):
    experiment_id = generate_experiment_id()

    ExperimentDefinition = {
        "experiment_id": experiment_id,
        "project_name": project_name,
        "description": description,
        "experiment_name": experiment_name,
        "results_dir": results_dir,
        "data_dir": data_dir,
    }

    return ExperimentDefinition


def _safe_run_pipeline(self, exp_objs, debug=False, start_from=0):

    def _pad(child):
        if "is_valid" not in child.data:
            child.data["is_valid"] = False
        if "corrected_sql" not in child.data:
            child.data["corrected_sql"] = None
        if child.data.get("is_valid") is False and child.data.get("error"):
            print(
                f"[{child.data.get('question')[:60]}…] validator error → {child.data['error']}"
            )
        return child

    results, step_outputs = [], {} if self.return_step_outputs else None
    self.order[start_from].queue.extend(exp_objs)

    for step_ in self.order[start_from:]:
        step_results = []

        with tqdm(total=len(step_.queue), desc=f"{step_.worker.name} Execution") as bar:
            while step_.queue:
                exp_obj = step_.queue.pop(0)

                try:
                    output = step_.worker(exp_obj, debug=debug)

                except Exception as e:
                    self.logger.warning(f"{step_.worker.name} failed: {e}")
                    bar.update(1)
                    continue
                if output is None:
                    bar.update(1)
                    continue

                outs = output if isinstance(output, list) else [output]
                outs = [_pad(o) for o in outs if o is not None]

                if not outs:
                    bar.update(1)
                    continue

                # ── Fan-out / push to next step ────────────────────────────
                if step_.next:
                    step_.next.queue.extend(
                        [
                            ExperimentObject(
                                experiment_step=exp_obj.step.next,
                                data=deepcopy(o.data),
                            )
                            for o in outs
                        ]
                    )
                else:
                    results.extend(outs)
                step_results.extend(outs)
                self._record_step(output, step_.worker.name)
                bar.update(1)

        if self.return_step_outputs and step_.worker.name != "save":
            step_outputs[step_.worker.name] = step_results

    return (results, step_outputs) if self.return_step_outputs else results


def flatten_results(results):
    flat = []
    for r in results:
        if r is None:
            continue
        if isinstance(r, list):
            flat.extend([x.data for x in r if x is not None])
        else:
            flat.append(r.data)
    return flat


def _load_glossary(project_name: str) -> str:
    gdf = pd.read_parquet(Path("local-db") / "glossary.parquet")
    gdf = gdf[gdf["project_id"] == project_name]
    return "\n".join([f"{row['input']}: {row['output']}" for _, row in gdf.iterrows()])


def make_branch(
    branch_name: str,
    multi_gen,
    schema: str,
    db_type: str,
    db_params: str,
    results_root: str,
) -> BaseAgenticPipeline:
    """
    pattern / variation / decomposer →  (n) questions
    → SchemaToSQLGenerator
    → SQLValidator (v1)
    → SQLDebugger
    → SQLValidator (v2)
    """
    sql_gen = SchemaToSQLGenerator(
        name=f"{branch_name}_sqlgen",
        model=multi_gen.model,
        schema=schema,
        db_type=db_type,
        db_params=db_params,
        instruction="""
                    You are an expert SQLite analyst: \n
        
                    Schema (tables & columns ONLY):\n
                    {schema}
                    
                    (Natural-language glossary - NOT table names):\n
                    {glossary}
                    
                    Example - learn format only
                    Original Question:\n
                    {original_question}
                    
                    Original SQL:\n
                    {original_sql}
                    
                    Now consider the following sub-question:\n
                    {question}

                    Write one complete SQL query (SQLite-compatible) that answers Sub Question.
                    It must reference only columns that exist in the Schema.

                    -- Guidelines ---------------------------------------------------------
                    • **Do NOT** emit any DDL (CREATE, ALTER, DROP, etc.) or data‑definition statements.
                    • It **must** begin with SELECT or WITH and end with a semicolon.
                    • Only reference columns that exist in the provided schema.
                    • Use Original Question and Original SQL as sample to learn from
                    • Return **only** a JSON object
                    """,
        output_type={"sql_query": "str"},
    )

    v1 = SQLValidator(
        name=f"{branch_name}_val1",
        model=multi_gen.model,
        instruction="Validate {sql} against schema.\nSchema:\n{schema}",
        db_type=db_type,
        db_params=db_params,
        schema=schema,
        # sql_key="generated_sql",
        sql_key="sql",
        skip_autofixes=["fix_dates"],
        output_type={"error": "str", "explanation": "str", "is_valid": "bool"},
        is_valid_field="is_valid",
    )

    dbg = SQLDebuggerGenerator(
        name=f"{branch_name}_debug",
        model=multi_gen.model,
        role="You are a SQL debugging expert. Output only the corrected SQL.",
        instruction=(
            "Fix query if invalid.\n"
            "Question: {question}\n"
            "Bad SQL: {sql}\n"
            "Error: {error}\n"
            "Explanation: {explanation}"
        ),
        db_type=db_type,
        db_params=db_params,
        schema=schema,
    )

    v2 = SQLValidator(
        name=f"{branch_name}_val2",
        model=multi_gen.model,
        instruction="Validate {corrected_sql} against schema.\nSchema:\n{schema}",
        db_type=db_type,
        db_params=db_params,
        schema=schema,
        sql_key="corrected_sql",
        skip_autofixes=["fix_dates"],
        output_type={"error": "str", "explanation": "str", "is_valid": "bool"},
        is_valid_field="is_valid",
    )

    gens = {
        branch_name: multi_gen,
        sql_gen.name: sql_gen,
        dbg.name: dbg,
    }
    vals = {
        v1.name: v1,
        v2.name: v2,
    }

    order = [
        branch_name,
        sql_gen.name,
        v1.name,
        dbg.name,
        v2.name,
    ]

    return BaseAgenticPipeline(
        generators=gens,
        validators=vals,
        order=order,
        record_dir=os.path.join(results_root, branch_name),
        record_step=True,
        record_results=True,
        save_keys=[
            "question",
            "sql",
            "corrected_sql",
            "is_valid",
        ],
        quiet=True,
    )


def main(args, config, project_dir, experiment_config):

    # _original_run_pipeline = BaseAgenticPipeline.run_pipeline

    project_name = config["Project"]["project_name"]
    results_dir = os.path.join(
        Path(__file__).parent.parent, "projects", project_name, "experiment_results"
    )
    data_dir = os.path.join(
        Path(__file__).parent.parent, "projects", project_name, "data"
    )

    # ------------------------------------------------------------------ #
    # prep experiment metadata                                           #
    # ------------------------------------------------------------------ #

    experiment_id = generate_experiment_id()
    ExperimentDefinition = {
        "experiment_id": experiment_id,
        "project_name": project_name,
        "description": config["Project"]["description"],
        "experiment_name": args["experiment_name"],
        "results_dir": results_dir,
        "data_dir": data_dir,
    }

    # ------------------------------------------------------------------ #
    # build the "outer" experiment structure (gets us schema + gens)     #
    # ------------------------------------------------------------------ #
    experiment_config["project_name"] = project_name
    pipeline_components = build_experiment_pipeline(experiment_config)

    # we only need the three multi-gens; ignore the monolithic pipeline
    pattern_gen = pipeline_components["generators"]["pattern"]
    variation_gen = pipeline_components["generators"]["variation"]
    decomposer_gen = pipeline_components["generators"]["decomposer"]
    schema = pipeline_components["schema"]

    BaseAgenticPipeline.run_pipeline = _safe_run_pipeline

    # ------------------------------------------------------------------ #
    # load example_set → DataFrame                                       #
    # ------------------------------------------------------------------ #
    example_path = Path(__file__).parent.parent / "local-db" / "example_set.parquet"
    example_df = pd.read_parquet(example_path)
    example_df = example_df[example_df["project_id"] == project_name]

    if example_df.empty:
        print(f"No example_set entries for project '{project_name}'")
        return

    # renaming / enrichment for prompt columns
    sqlite_path = next(Path(data_dir).glob("*.sqlite"))
    prompts_df = example_df.rename(
        columns={"input": "question", "output": "sql"}
    ).assign(
        original_question=lambda d: d["question"],
        original_sql=lambda d: d["sql"],
        db_type="sqlite",
        db_params=str(sqlite_path),
        schema=schema,
        glossary=lambda d: _load_glossary(project_name),
        error_sql="",
        error_message="",
        error_explanation="",
    )

    extract_cols = [
        "question",
        "sql",
        "original_question",
        "original_sql",
        "schema",
        "glossary",
        "db_type",
        "db_params",
        "error_sql",
        "error_message",
        "error_explanation",
    ]
    prompts = build_prompts_from_dataframe(prompts_df, extract_cols, {})

    # ------------------------------------------------------------------ #
    # instantiate three pipelines                                        #
    # ------------------------------------------------------------------ #
    branch_pipes = {
        "pattern": make_branch(
            "pattern", pattern_gen, schema, "sqlite", str(sqlite_path), results_dir
        ),
        "variation": make_branch(
            "variation", variation_gen, schema, "sqlite", str(sqlite_path), results_dir
        ),
        "decomposer": make_branch(
            "decomposer",
            decomposer_gen,
            schema,
            "sqlite",
            str(sqlite_path),
            results_dir,
        ),
    }

    # disable internal spot-checks to speed things up
    for bp in branch_pipes.values():
        bp.pipeline_step_logic = lambda *_, **__: None  # static key check
        bp.pipline_spotcheck = (
            lambda *_, **__: None
        )  # live 1-shot run   ---> Do NOT change this to pipeline---> first BaseAgenticPipeline method needs to be modified

    # ------------------------------------------------------------------ #
    # run the three pipelines                                            #
    # ------------------------------------------------------------------ #
    all_outputs = []
    for name, bp in branch_pipes.items():
        print(f"Running {name} branch …")
        out = bp(prompts)
        all_outputs.extend(out)

    results_df = pd.DataFrame(flatten_results(all_outputs))

    save_results(results_df, ExperimentDefinition["experiment_name"])
    print(f"Generated {len(results_df)} rows ({len(example_df)} inputs × 7).")

    # ------------------------------------------------------------------ #
    # keep only final valid pairs & store in parquet                      #
    # ------------------------------------------------------------------ #
    valid_df = (
        results_df.query("is_valid")  # keep only rows that passed Val-2
        .assign(
            sql=lambda d: (
                d["corrected_sql"].fillna(d["generated_sql"]).fillna(d["sql_query"])
            )
        )
        .loc[:, ["question", "sql", "is_valid"]]  # final shape
    )
    out_parquet = Path(os.path.join("local-db", "datasets.parquet"))

    print(f"Wrote/updated {len(valid_df)} validated pairs → {out_parquet}")

    # ------------------------------------------------------------------ #
    # optional DB registration                                           #
    # ------------------------------------------------------------------ #
    if not args["test_run"]:
        db = ProjectDB()
        for col in ("parameters", "model_config"):
            if col in valid_df.columns:
                valid_df[col] = valid_df[col].apply(json.dumps)
        dataset_id = db.create_dataset(
            name=ExperimentDefinition["experiment_name"],
            description=ExperimentDefinition["description"],
            qa_pairs=valid_df[["question", "sql"]],
        )
        db.register_experiment(
            project_id=project_name,
            experiment_id=ExperimentDefinition["experiment_id"],
            experiment_name=ExperimentDefinition["experiment_name"],
            description=ExperimentDefinition["description"],
            parameters={"dummy": None},
            model_config={"dummy": None},
            generators=None,
            validators=None,
            schema_id=None,
            tuning_job_id=None,
            dataset_id=dataset_id,
        )
        print(f"Dataset '{dataset_id}' registered.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_name", help="Project name")
    parser.add_argument("-e", "--experiment_name", help="Experiment name")
    parser.add_argument(
        "-b", "--batches", type=int, default=1, help="Number of batches"
    )
    parser.add_argument("-k", "--api_key", required=False, help="API key for Lamini")
    parser.add_argument(
        "-n",
        "--num_prompts",
        type=int,
        help="Number of prompts to process (default: all)",
    )
    parser.add_argument(
        "-tr",
        "--test_run",
        action="store_true",
        help="Test run - skip database operations",
    )

    args = vars(parser.parse_args())

    project_dir = f'projects/{args["project_name"]}'

    with open(f"{project_dir}/ymls/project.yml", "r") as f:
        proj_cfg = yaml.safe_load(f)
    with open(f"{project_dir}/ymls/experiment.yml", "r") as f:
        exp_cfg = yaml.safe_load(f)

    # API key plumbing
    if "LAMINI_API_KEY" not in os.environ:
        if proj_cfg["Lamini"]["api_key"] == "<your_api_key>":
            raise ValueError("Set a real API key in the config or env")
        os.environ["LAMINI_API_KEY"] = proj_cfg["Lamini"]["api_key"]
    os.environ["OPENAI_API_KEY"] = os.getenv("LAMINI_API_KEY")

    main(args, proj_cfg, project_dir, exp_cfg)
