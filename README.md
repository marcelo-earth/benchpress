# BenchPress

Evaluate language models with lm-eval-harness and build a custom benchmark.

## What is this?

Running evals on LLMs is harder than it looks. Prompt format, few-shot count, and metric choice all change the results. This project runs standard benchmarks (MMLU, HellaSwag, ARC) and builds a custom one to understand the pitfalls.

## What we do

1. Set up lm-eval-harness and run standard benchmarks on small models
2. Test how prompt format changes results
3. Build a custom Spanish language benchmark
4. Compare models on a mini leaderboard

## Setup

```bash
pip install -r requirements.txt
python run_eval.py --model gpt2 --tasks hellaswag --limit 100
```

## Files

| File | What it does |
|------|-------------|
| `run_eval.py` | Wrapper around lm-eval-harness |
| `custom_bench.py` | Build and run custom benchmarks |
| `prompt_sensitivity.py` | Test how prompt format affects scores |
| `benchpress.ipynb` | Full analysis with leaderboard |
