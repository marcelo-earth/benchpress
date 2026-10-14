"""Score local models on pilot_50.json and pilot_hard_50.json.

Scores the letter token with a leading space (the token that really follows
"Respuesta:"), unlike custom_bench.py. Writes results_sets.json.
"""

import json
import math
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODELS = sys.argv[1:] or ["EleutherAI/pythia-70m", "gpt2", "Qwen/Qwen2.5-0.5B"]
SETS = {"pilot": "pilot_50.json", "hard": "pilot_hard_50.json"}
PROMPT = "Pregunta: {q}\n{c}\nRespuesta:"


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return center - half, center + half


results = []
for name in MODELS:
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name).eval()
    ids = {}
    for L in "ABCD":
        t = tok.encode(" " + L, add_special_tokens=False)
        assert len(t) == 1, (name, L, t)
        ids[L] = t[0]
    for set_name, path in SETS.items():
        items = json.load(open(path))
        per_cat, correct = {}, 0
        for it in items:
            prompt = PROMPT.format(q=it["question"], c="\n".join(it["choices"]))
            x = tok(prompt, return_tensors="pt")
            with torch.no_grad():
                logits = model(**x).logits[0, -1]
            pred = max(ids, key=lambda L: logits[ids[L]].item())
            ok = pred == it["answer"]
            correct += ok
            c = per_cat.setdefault(it["category"], [0, 0])
            c[0] += ok
            c[1] += 1
        lo, hi = wilson(correct, len(items))
        print(f"{name:24s} {set_name:6s} {correct}/{len(items)} = {correct/len(items):.0%} [{lo:.0%}, {hi:.0%}]")
        results.append({"model": name, "set": set_name, "correct": correct, "n": len(items), "ci": [lo, hi], "per_category": per_cat})

json.dump(results, open("results_sets.json", "w"), indent=1)
