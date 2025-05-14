#!/usr/bin/env python
import argparse
import json
import os
import sys
from pathlib import Path
from tqdm import tqdm
import pandas as pd
import yaml
import lamini
from lamini import Lamini

import numpy as np
import openai
import torch
from transformers import AutoTokenizer, AutoModel
import matplotlib.pyplot as plt
import pyarrow.parquet as pq

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from utils.utils import (
    reduce_dimensionality,
    similarity_check,
    save_results_to_jsonl,
    load_config,
    format_glossary,
    read_jsonl,
)
from lamini.experiment.error_analysis_eval import SQLExecutionPipeline

DEFAULT_SYSTEM_MESSAGE = (
    "You are a SQL‐generation assistant.  "
    "Given a natural‐language question and table/schema glossary, output only the "
    "corresponding SQL query (no prose)."
)


def get_text_embeddings(
    text_list,
    project_name=None,
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    batch_size=32,
):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(torch.device("cpu"))

    pieces = []
    for i in range(0, len(text_list), batch_size):
        batch = text_list[i : i + batch_size]
        with torch.no_grad():
            inputs = tokenizer(
                batch, padding=True, truncation=True, return_tensors="pt"
            )
            outputs = model(**inputs)
            pieces.append(outputs.last_hidden_state[:, 0, :])
    embs = torch.cat(pieces, dim=0).numpy()
    return embs


def get_embeddings_from_strings(strings, project_name):
    cfg = load_config(PROJECT_ROOT / "projects" / project_name / "ymls" / "project.yml")
    client = openai.OpenAI(
        api_key=cfg["Lamini"]["api_key"],
        base_url=cfg["Lamini"]["base_url_inf"],
    )
    embs = []
    for s in strings:
        resp = client.embeddings.create(model="text-embedding-3-small", input=s)[
            "data"
        ][0]["embedding"]
        embs.append(resp)
    return embs


def cosine_similarity_of_embeddings(ans_ref, ans_gen, project_name):
    cfg = load_config(PROJECT_ROOT / "projects" / project_name / "ymls" / "project.yml")
    client = openai.OpenAI(
        api_key=cfg["Lamini"]["api_key"],
        base_url=cfg["Lamini"]["base_url_inf"],
    )

    def _embed(text):
        return np.array(
            client.embeddings.create(model="text-embedding-3-small", input=[text])[
                "data"
            ][0]["embedding"]
        )

    e1, e2 = _embed(ans_ref), _embed(ans_gen)
    return float(np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2)))


def make_prompt(user_input, system_message):
    p = "<|start_header_id|>system<|end_header_id|>" + system_message
    p += "<|eot_id|><|start_header_id|>user<|end_header_id|>" + user_input
    p += "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    return p


def initialize_llm(project_name):
    cfg = load_config(PROJECT_ROOT / "projects" / project_name / "ymls" / "project.yml")
    os.environ["LAMINI_API_KEY"] = cfg["Lamini"]["api_key"]
    os.environ["LAMINI_API_URL"] = cfg["Lamini"]["base_url_inf"]
    return Lamini(
        cfg["Project"]["model"],
        api_key=cfg["Lamini"]["api_key"],
        api_url="https://api.lamini.ai",
    )


def llm_sql_evaluator(ref_sql: str, gen_sql: str, question: str, project_name: str):
    system = (
        "You are a SQL evaluation assistant.  "
        "Given a natural-language question and two SQL queries "
        "(the ground-truth and the generated), determine "
        "whether the generated SQL correctly answers the question.  "
        "Respond with valid JSON: "
        "{'explanation': <detailed rationale>, 'correct': <true|false>}."
    )
    user = (
        f"========== Question ==========\n{question}\n\n"
        f"====== Ground-Truth SQL ======\n{ref_sql}\n\n"
        f"====== Generated SQL ========\n{gen_sql}\n\n"
        "Does the generated SQL correctly implement the intent of the ground-truth? "
        "Answer only with the JSON object as specified above."
    )
    llm = initialize_llm(project_name)
    prompt = make_prompt(user, system)

    try:
        response = llm.generate(
            prompt, output_type={"explanation": "str", "correct": "bool"}
        )
    except:
        response = {"explanation": "could not evaluate", "correct": "false"}

    return response


def _to_plain_text(resp):
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        if "generated_text" in resp:
            return resp["generated_text"]
        if "choices" in resp and resp["choices"]:
            return resp["choices"][0].get("text", "")
    return str(resp)


def read_test_set(parquet_path: Path):
    df = pd.read_parquet(parquet_path)
    return [
        {"question": row["input"], "gold_query": row.get("output", "")}
        for _, row in df.iterrows()
    ]


def run_inference(test_cases, model_id: str):
    llm = Lamini(
        model_name=model_id,
        api_key=os.environ["LAMINI_API_KEY"],
        api_url="https://api.lamini.ai",
    )
    results = []
    total = len(test_cases)
    for idx, tc in tqdm(enumerate(test_cases, start=1)):
        prompt = (
            "<|start_header_id|>user<|end_header_id|>"
            f"{tc['question']}"
            "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
        )
        try:
            resp = llm.generate(prompt)
            gen = _to_plain_text(resp)
        except Exception as e:
            gen = f"Error: {e}"
        results.append(
            {
                "question": tc["question"],
                "gold_query": tc.get("gold_query", ""),
                "generated_query": gen,
            }
        )
        if idx % 25 == 0 or idx == total:
            print(f"Processed {idx}/{total}")
    return results


def prepare_for_evaluation(inference_results):
    return [
        r for r in inference_results if not r["generated_query"].startswith("Error:")
    ]


def visualize_embeddings(strings, project_name, title="2D Embeddings"):
    embs = get_text_embeddings(strings, project_name=project_name)
    pts = reduce_dimensionality(embs)
    plt.figure(figsize=(8, 6))
    for txt, (x, y) in zip(strings, pts):
        plt.scatter(x, y)
        plt.annotate(txt[:15] + "…", (x, y), fontsize=8)
    plt.title(title)
    plt.show()


def main(project):
    cfg = load_config(PROJECT_ROOT / "projects" / project / "ymls" / "project.yml")
    os.environ["LAMINI_API_KEY"] = cfg["Lamini"]["api_key"]
    os.environ["LAMINI_API_URL"] = cfg["Lamini"]["base_url_inf"]
    analysis_model = cfg["Project"]["model"]

    proj_dir = PROJECT_ROOT / "projects" / project
    data_dir = proj_dir / "data"
    local_db = PROJECT_ROOT / "local-db"
    results_dir = proj_dir / "experiment_results"
    results_dir.mkdir(exist_ok=True)

    parquet_path = local_db / "evalset.parquet"
    sqlite_files = list(data_dir.glob("*.sqlite"))
    if not sqlite_files:
        sys.exit(f"No SQLite file found in {data_dir}")
    db_path = sqlite_files[0]

    model_id = input("Enter the fine-tuned model ID to use for inference: ").strip()
    print("➜ Reading test set…")
    test_cases = read_test_set(parquet_path)
    print(f"   {len(test_cases)} cases loaded")
    print("➜ Running inference…")
    inference_results = run_inference(test_cases, model_id)

    evaluations = []
    for test_case, inference_result in tqdm(zip(test_cases, inference_results)):
        eval_result = llm_sql_evaluator(
            test_case["gold_query"],
            inference_result["generated_query"],
            test_case["question"],
            project,
        )
        evaluations.append(eval_result)
    inf_out = results_dir / "inference_results.jsonl"
    save_results_to_jsonl(inference_results, inf_out)
    print(f"   Inference results saved to {inf_out}")

    eval_cases = prepare_for_evaluation(inference_results)
    print(f"➜ Evaluating {len(eval_cases)} cases…")
    pipeline = SQLExecutionPipeline(model=analysis_model, db_type="sqlite")
    eval_results = pipeline.evaluate_queries(
        eval_cases, connection_params={"db_path": str(db_path)}
    )
    eval_out = results_dir / "analysis_results_with_data.jsonl"
    save_results_to_jsonl(eval_results, eval_out)
    print(f"   Evaluation results saved to {eval_out}")

    report_md = pipeline.generate_report(eval_results)
    report_path = results_dir / "analysis_report.md"
    report_path.write_text(report_md, encoding="utf-8")

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n\n#### LLM SQL Evaluations\n")
        for eval_result in evaluations:
            f.write(json.dumps(eval_result) + "\n")
    print(f"✅ Report written to {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run inference + SQL evaluation for a Lamini Text-to-SQL project"
    )
    parser.add_argument(
        "--project_name", required=True, help="Project name to evaluate"
    )
    args = parser.parse_args()
    main(args.project_name)
