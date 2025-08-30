# BenchPress

Evaluate language models with lm-eval-harness and build a custom benchmark.

## What is this?

Running evals on LLMs is harder than it looks. Prompt format, few-shot count, and metric choice all change the results. This project runs standard benchmarks (MMLU, HellaSwag, ARC) and builds a custom one to understand the pitfalls.

## Key findings

- Changing prompt format alone can swing scores by 20-40%
- Few-shot examples help but the effect varies a lot by task
- Small models (GPT-2) perform near random chance on Spanish questions
- lm-eval-harness makes running standard benchmarks easy, but interpreting results is the hard part

## What we do

1. Set up lm-eval-harness and run standard benchmarks on small models
2. Test how prompt format changes results (5 different templates)
3. Build a custom Spanish language benchmark (15 questions)
4. Compare models on a mini leaderboard

## Setup

```bash
pip install -r requirements.txt
python run_eval.py --model gpt2 --tasks hellaswag --limit 100
python run_eval.py --compare --tasks quick --limit 200
python prompt_sensitivity.py --model gpt2
python custom_bench.py --model gpt2 --template plain
```

## Files

| File | What it does |
|------|-------------|
| `run_eval.py` | Wrapper around lm-eval-harness |
| `custom_bench.py` | Build and run custom Spanish benchmark |
| `prompt_sensitivity.py` | Test how prompt format affects scores |
| `benchpress.ipynb` | Full analysis with leaderboard |
