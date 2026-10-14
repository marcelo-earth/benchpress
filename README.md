# BenchPress

Evaluate language models with lm-eval-harness and build a custom benchmark.

## What is this?

Running evals on LLMs is harder than it looks. Prompt format, few-shot count, and metric choice all change the results. This project runs standard benchmarks (MMLU, HellaSwag, ARC) and builds a custom one to understand the pitfalls.

## Key findings

- Changing prompt format alone can swing scores by 20-40%
- Adding a chain-of-thought prefix sometimes helps, sometimes hurts
- Few-shot examples help but the effect varies a lot by task
- Small models (GPT-2) perform near random chance on Spanish questions
- Asking in English vs Spanish changes results even on the same questions
- lm-eval-harness makes running standard benchmarks easy, but interpreting results is the hard part

## What we do

1. Set up lm-eval-harness and run standard benchmarks on small models
2. Test how prompt format changes results (6 templates including chain-of-thought)
3. Build a custom Spanish language benchmark (20 questions)
4. Compare models on a mini leaderboard
5. Compare template language (Spanish vs English) on same questions

## Pipeline

```mermaid
flowchart LR
    A[Write items<br/>build_pilot.py] --> B[pilot_50.json<br/>key + justification]
    A --> C[pilot_blind.json<br/>no key]
    C --> D[Blind labeler<br/>fresh Claude session]
    D --> E[pilot_labels.json]
    B --> F[score_pilot.py<br/>agreement + kappa]
    E --> F
    F -->|90% or more| G[Scale to 500 items<br/>and 10 models]
    F -->|under 90%| H[Fix writing process<br/>rerun pilot]
    H --> A
```

## Pilot (2026-10-14)

50 Spanish multiple choice items with a balanced answer key (A 13, B 13, C 12, D 12). A blind labeler answers without the key and `score_pilot.py` reports agreement and Cohen's kappa. Result: 50/50, kappa 1.0, provisional because the items are easy and labeler and author share a model family. Pre-registration lives in the experiment hub (`projects/benchpress.md`).

```bash
python build_pilot.py
python score_pilot.py pilot_labels.json
```

## Hard set (2026-10-14)

A second set of 50 harder items (`pilot_hard_50.json`: multi step reasoning, orthography and grammar traps, less common facts). Two independent blind Claude Sonnet 5.5 labelers matched the key on 50/50 and each other on 50/50, so the key is sound. That also means the set is **not hard for Claude**. Difficulty shows only on small local models:

![Accuracy of local models on both sets](plots/sets_accuracy.png)

| Model | Pilot | Hard |
|-------|-------|------|
| pythia-70m | 26% | 28% |
| gpt2 | 22% | 26% |
| Qwen2.5-0.5B | 42% | 30% |

Random is 25%. With 50 items each interval is about 25 points wide: pythia-70m and gpt2 are at chance on both sets, and Qwen's drop from 42% to 30% is not significant (z = 1.26). The hard set shows the direction we want but does not yet separate models; more items and larger models are needed. `custom_bench.py` scores the letter token without the leading space; `run_sets.py` fixes that.

```bash
python run_sets.py
```

## Setup

```bash
pip install -r requirements.txt
python run_eval.py --model gpt2 --tasks hellaswag --limit 100
python run_eval.py --compare --tasks quick --limit 200
python prompt_sensitivity.py --model gpt2
python custom_bench.py --model gpt2 --template plain
python compare_templates.py --model gpt2
python model_info.py
```

## Files

| File | What it does |
|------|-------------|
| `run_eval.py` | Wrapper around lm-eval-harness |
| `custom_bench.py` | Build and run custom Spanish benchmark (20 Q) |
| `prompt_sensitivity.py` | Test how prompt format affects scores |
| `compare_templates.py` | Compare Spanish vs English templates |
| `model_info.py` | Model size and config comparison |
| `benchpress.ipynb` | Full analysis with leaderboard |
| `build_pilot.py` | Build the 50 item pilot, its key and the blind copy |
| `score_pilot.py` | Agreement and kappa between blind labels and key |
| `build_pilot_hard.py` | Build the harder 50 item set, its key and blind copy |
| `run_sets.py` | Score local models on both sets, writes `results_sets.json` |
