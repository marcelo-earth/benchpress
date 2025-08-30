"""Wrapper around lm-eval-harness for running standard benchmarks."""

import argparse
import json
import os

import lm_eval


STANDARD_TASKS = {
    "quick": ["hellaswag", "arc_easy"],
    "medium": ["hellaswag", "arc_easy", "arc_challenge", "winogrande"],
    "full": ["hellaswag", "arc_easy", "arc_challenge", "winogrande", "mmlu"],
}

MODELS_TO_TEST = [
    "gpt2",
    "gpt2-medium",
    "gpt2-large",
    "EleutherAI/pythia-160m",
    "EleutherAI/pythia-410m",
]


def run_benchmark(model_name, tasks, limit=None, num_fewshot=0, batch_size="auto"):
    """Run lm-eval-harness on a model.

    Args:
        model_name: HuggingFace model name
        tasks: list of task names or a preset name ("quick", "medium", "full")
        limit: max samples per task (None = all)
        num_fewshot: number of few-shot examples
        batch_size: batch size for inference

    Returns:
        results dict from lm-eval
    """
    if isinstance(tasks, str) and tasks in STANDARD_TASKS:
        tasks = STANDARD_TASKS[tasks]

    print(f"\nEvaluating: {model_name}")
    print(f"Tasks: {tasks}")
    print(f"Few-shot: {num_fewshot}, Limit: {limit}")

    results = lm_eval.simple_evaluate(
        model="hf",
        model_args=f"pretrained={model_name}",
        tasks=tasks,
        num_fewshot=num_fewshot,
        limit=limit,
        batch_size=batch_size,
    )

    return results


def extract_scores(results):
    """Pull out the key metrics from lm-eval results."""
    scores = {}
    if "results" not in results:
        return scores

    for task_name, task_results in results["results"].items():
        # lm-eval uses different metric names per task
        for metric in ["acc", "acc_norm", "acc,none", "acc_norm,none"]:
            if metric in task_results:
                clean_metric = metric.replace(",none", "")
                scores[f"{task_name}/{clean_metric}"] = task_results[metric]
                break

    return scores


def run_comparison(models=None, tasks="quick", limit=100, num_fewshot=0):
    """Run the same benchmark on multiple models and compare."""
    if models is None:
        models = MODELS_TO_TEST

    all_scores = {}
    for model in models:
        try:
            results = run_benchmark(model, tasks, limit=limit, num_fewshot=num_fewshot)
            all_scores[model] = extract_scores(results)
        except Exception as e:
            print(f"  Error with {model}: {e}")
            all_scores[model] = {"error": str(e)}

    return all_scores


def save_results(scores, output_dir="results"):
    """Save comparison results to JSON."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "comparison.json")
    with open(path, "w") as f:
        json.dump(scores, f, indent=2)
    print(f"\nResults saved to {path}")


def print_leaderboard(scores):
    """Print a simple leaderboard."""
    try:
        from tabulate import tabulate
    except ImportError:
        for model, s in scores.items():
            print(f"{model}: {s}")
        return

    # get all unique metrics
    all_metrics = set()
    for s in scores.values():
        all_metrics.update(s.keys())
    all_metrics.discard("error")
    all_metrics = sorted(all_metrics)

    headers = ["Model"] + [m.split("/")[-1] for m in all_metrics] + ["Avg"]
    rows = []
    for model, s in scores.items():
        if "error" in s:
            rows.append([model] + ["ERR"] * (len(all_metrics) + 1))
            continue
        vals = [s.get(m, 0) for m in all_metrics]
        avg = sum(vals) / len(vals) if vals else 0
        row = [model] + [f"{v:.3f}" for v in vals] + [f"{avg:.3f}"]
        rows.append(row)

    # sort by average (last column)
    rows.sort(key=lambda r: float(r[-1]) if r[-1] != "ERR" else 0, reverse=True)
    print("\n" + tabulate(rows, headers=headers, tablefmt="github"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LLM benchmarks")
    parser.add_argument("--model", type=str, default="gpt2", help="Model name")
    parser.add_argument("--tasks", type=str, nargs="+", default=["hellaswag"], help="Task names or preset")
    parser.add_argument("--limit", type=int, default=100, help="Max samples per task")
    parser.add_argument("--num-fewshot", type=int, default=0, help="Few-shot examples")
    parser.add_argument("--compare", action="store_true", help="Compare multiple models")
    parser.add_argument("--batch-size", type=str, default="auto")
    args = parser.parse_args()

    if args.compare:
        scores = run_comparison(tasks=args.tasks[0] if len(args.tasks) == 1 else args.tasks, limit=args.limit)
        print_leaderboard(scores)
        save_results(scores)
    else:
        results = run_benchmark(
            args.model,
            args.tasks,
            limit=args.limit,
            num_fewshot=args.num_fewshot,
            batch_size=args.batch_size,
        )
        scores = extract_scores(results)
        for k, v in scores.items():
            print(f"  {k}: {v:.4f}")
