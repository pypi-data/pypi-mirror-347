import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from tqdm import tqdm
import pandas as pd
import yaml
import lamini
from lamini import Lamini

# Make imports more resilient to different entry points
PROJECT_ROOT_DEFAULT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT_DEFAULT))

try:
    from utils.utils import (
        save_results_to_jsonl,
        load_config,
        format_glossary,
        read_jsonl,
    )
    from lamini.experiment.error_analysis_eval import SQLExecutionPipeline
except ImportError:
    # Fallback for when running from CLI
    # These might be None if running from CLI without proper project structure
    save_results_to_jsonl = None
    load_config = None
    format_glossary = None
    read_jsonl = None
    SQLExecutionPipeline = None


def read_test_set(file_path: str) -> List[Dict[str, str]]:
    """Return list of {'question', 'gold_query'} from a file."""
    # Handle file extension
    file_path_obj = Path(file_path)
    if file_path_obj.suffix == ".parquet":
        df = pd.read_parquet(file_path)
        required_cols = {"input"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"{file_path_obj.name} missing columns: {missing}")
        return [
            {
                "question": row["input"],
                "gold_query": row.get("output", ""),
            }
            for _, row in df.iterrows()
        ]
    elif file_path_obj.suffix == ".jsonl":
        if read_jsonl:
            return read_jsonl(file_path)
        else:
            # Fallback implementation if utils.read_jsonl is not available
            with open(file_path, "r") as f:
                return [json.loads(line) for line in f]
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def _to_plain_text(resp: Any) -> str:
    """Normalize Lamini response into a plain SQL string."""
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        if "generated_text" in resp:
            return resp["generated_text"]
        if "choices" in resp and resp["choices"]:
            return resp["choices"][0].get("text", str(resp))
    return str(resp)


def run_inference(
    test_cases: List[Dict[str, str]],
    model_id: str,
    system_message: Optional[str] = None,
) -> List[Dict[str, str]]:
    llm = Lamini(
        model_name=model_id,
        api_key=os.environ["LAMINI_API_KEY"],
        api_url="https://api.lamini.ai",
    )
    results: List[Dict[str, str]] = []

    total = len(test_cases)
    print(f"Running inference on {total} test cases with model {model_id}")

    for idx, tc in tqdm(enumerate(test_cases, 1)):
        if system_message:
            prompt = (
                f"<|start_header_id|>system<|end_header_id|>{system_message}<|eot_id|>"
                "<|start_header_id|>user<|end_header_id|>"
                f"{tc['question']}"
                "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
            )
        else:
            prompt = (
                "<|start_header_id|>user<|end_header_id|>"
                f"{tc['question']}"
                "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
            )

        try:
            resp = llm.generate(prompt)
            generated_query = _to_plain_text(resp)
        except Exception as exc:
            generated_query = f"Error: {exc}"

        results.append(
            {
                "question": tc["question"],
                "gold_query": tc.get("gold_query", ""),
                "generated_query": generated_query,
            }
        )
        if idx % 25 == 0 or idx == total:
            print(f"Processed {idx}/{total}")

    return results


def save_results_locally(results: List[Dict], output_path: str) -> None:
    """Save results to a JSONL file, implementation used when utils.save_results_to_jsonl is not available."""
    with open(output_path, "w") as f:
        for item in results:
            f.write(json.dumps(item) + "\n")


def prepare_for_evaluation(
    inference_results: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    """Drop rows whose model call failed."""
    return [
        r for r in inference_results if not r["generated_query"].startswith("Error:")
    ]


def run_cli_inference(args):
    """Entry point for CLI-based inference."""
    model_id = args.model_id
    input_file = args.eval_file_path
    output_file = args.output
    system_message = args.system_message

    # Ensure we have an input file
    if not input_file:
        print("Error: Input file is required.")
        return 1
    # Set default output file if not provided
    if not output_file:
        output_dir = os.path.dirname(input_file)
        output_file = os.path.join(output_dir, "inference_results.jsonl")
    print(f"➜ Reading test cases from {input_file} ...")
    try:
        test_cases = read_test_set(input_file)
        print(f"   {len(test_cases)} cases loaded")
    except Exception as e:
        print(f"Error reading test cases: {e}")
        return 1

    print(f"➜ Running inference with model {model_id} ...")
    try:
        inference_results = run_inference(test_cases, model_id, system_message)
    except Exception as e:
        print(f"Error during inference: {e}")
        return 1

    print(f"➜ Saving cresults to {output_file} ...")
    try:
        # Use the correct function based on what's available
        if save_results_to_jsonl:
            save_results_to_jsonl(inference_results, output_file)
        else:
            save_results_locally(inference_results, output_file)
    except Exception as e:
        print(f"Error saving results: {e}")
        return 1

    print("\n✅ Inference completed successfully!")
    print(f"• Results saved to: {output_file}")

    return 0


def run_project_inference(project_name: str) -> None:
    """Entry point for project-based inference, maintaining the original code's functionality."""
    project_root = PROJECT_ROOT_DEFAULT / "projects" / project_name
    yml_path = project_root / "ymls" / "project.yml"
    data_dir = project_root / "data"
    local_db_dir = PROJECT_ROOT_DEFAULT / "local-db"
    results_dir = project_root / "experiment_results"
    results_dir.mkdir(parents=True, exist_ok=True)

    if not yml_path.exists():
        sys.exit(f"Config file not found: {yml_path}")
    with open(yml_path, "r") as f:
        cfg = yaml.safe_load(f)

    try:
        lamini.api_url = cfg["Lamini"]["base_url_inf"]
        lamini.api_key = cfg["Lamini"]["api_key"]
        analysis_model_id = cfg["Project"]["model"]
    except KeyError as ke:
        sys.exit(f"project.yml missing key: {ke}")

    os.environ.update(
        LAMINI_API_URL=lamini.api_url,
        LAMINI_API_KEY=lamini.api_key,
    )

    # --- paths ---------------------------------------------------------------
    parquet_path = local_db_dir / "evalset.parquet"
    # Find any available SQLite file in the data directory
    sqlite_files = list(data_dir.glob("*.sqlite"))

    if not sqlite_files:
        sys.exit(f"No SQLite file found in {data_dir}")

    # Select the first available SQLite file
    db_path = sqlite_files[0]
    # --- run -----------------------------------------------------------------
    model_id = input("Enter the fine-tuned model ID to use for inference: ").strip()
    print("➜ Reading test set …")
    test_cases = read_test_set(str(parquet_path))
    print(f"   {len(test_cases)} cases loaded")

    print("➜ Running inference …")
    inference_results = run_inference(test_cases, model_id)
    inf_out = results_dir / "inference_results.jsonl"

    # Use the appropriate save function
    if save_results_to_jsonl:
        save_results_to_jsonl(inference_results, str(inf_out))
    else:
        save_results_locally(inference_results, str(inf_out))

    print("➜ Preparing evaluation set …")
    eval_cases = prepare_for_evaluation(inference_results)
    print(f"   {len(eval_cases)} cases will be evaluated against the database")

    if SQLExecutionPipeline:
        print("➜ Executing SQL & scoring …")
        pipeline = SQLExecutionPipeline(model=analysis_model_id, db_type="sqlite")
        evaluation_results = pipeline.evaluate_queries(
            eval_cases,
            connection_params={"db_path": str(db_path)},
        )
        eval_out = results_dir / "analysis_results_with_data.jsonl"

        if save_results_to_jsonl:
            save_results_to_jsonl(evaluation_results, str(eval_out))
        else:
            save_results_locally(evaluation_results, str(eval_out))

        print("➜ Generating markdown report …")
        report_md = pipeline.generate_report(evaluation_results)
        report_path = results_dir / "analysis_report.md"
        report_path.write_text(report_md, encoding="utf-8")

        print("\n✅ Finished!")
        print(f"• Inference results:  {inf_out}")
        print(f"• Evaluation results: {eval_out}")
        print(f"• Report:            {report_path}")
    else:
        print("\n✅ Inference completed")
        print(f"• Inference results:  {inf_out}")


if __name__ == "__main__":
    # Determine which entry point to use based on provided arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--project":
        # Original project-based entry point
        parser = argparse.ArgumentParser(description="Run inference + SQL evaluation")
        parser.add_argument("--project", required=True, help="Project name")
        run_project_inference(parser.parse_args().project)
    else:
        # New CLI-based entry point
        parser = argparse.ArgumentParser(description="Run inference with Lamini models")
        parser.add_argument(
            "--model-id", required=True, help="Model ID to use for inference"
        )
        parser.add_argument(
            "--eval-file-path",
            required=True,
            help="Path to evaluation file (parquet or jsonl)",
        )
        parser.add_argument(
            "--output",
            help="Path to save output results (default: alongside input file)",
        )
        parser.add_argument(
            "--system-message", help="Optional system message to use for inference"
        )

        args = parser.parse_args()
        sys.exit(run_cli_inference(args))
