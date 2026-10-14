"""Score local models on an item file and save per item correctness.

Usage: python run_items.py items.json out.json [model ...]
Scores the letter token with a leading space after "Respuesta:". Models of
1B parameters or more run in bfloat16 on MPS; smaller ones in float32.
"""

import json
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

path, out = sys.argv[1], sys.argv[2]
MODELS = sys.argv[3:] or ["EleutherAI/pythia-70m", "gpt2", "Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-1.5B", "Qwen/Qwen2.5-3B"]
PROMPT = "Pregunta: {q}\n{c}\nRespuesta:"
device = "mps" if torch.backends.mps.is_available() else "cpu"
items = json.load(open(path))
res = {}

for name in MODELS:
    big = any(t in name for t in ("1.5B", "3B"))
    dtype = torch.bfloat16 if big else torch.float32
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=dtype).to(device).eval()
    ids = {}
    for L in "ABCD":
        t = tok.encode(" " + L, add_special_tokens=False)
        assert len(t) == 1, (name, L, t)
        ids[L] = t[0]
    preds = {}
    for it in items:
        prompt = PROMPT.format(q=it["question"], c="\n".join(it["choices"]))
        x = tok(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            logits = model(**x).logits[0, -1].float().cpu()
        preds[it["id"]] = max(ids, key=lambda L: logits[ids[L]].item())
    acc = sum(preds[it["id"]] == it["answer"] for it in items) / len(items)
    print(f"{name:24s} {device} {dtype} accuracy {acc:.1%}", flush=True)
    res[name] = {"dtype": str(dtype), "preds": preds}
    json.dump(res, open(out, "w"), indent=1)
    del model
    if device == "mps":
        torch.mps.empty_cache()
