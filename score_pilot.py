"""Score blind labels against an answer key: agreement and Cohen's kappa.

Usage: python score_pilot.py labels.json [key.json]  (key defaults to pilot_50.json)
"""

import json
import sys
from collections import Counter

key = sys.argv[2] if len(sys.argv) > 2 else "pilot_50.json"
gold = {g["id"]: g for g in json.load(open(key))}
labels = {l["id"]: l for l in json.load(open(sys.argv[1]))}

ids = sorted(gold)
agree = [i for i in ids if labels[i]["label"] == gold[i]["answer"]]
po = len(agree) / len(ids)
cg = Counter(gold[i]["answer"] for i in ids)
cl = Counter(labels[i]["label"] for i in ids)
pe = sum(cg[c] / len(ids) * cl[c] / len(ids) for c in "ABCD")
kappa = (po - pe) / (1 - pe)
print(f"agreement {len(agree)}/{len(ids)} = {po:.0%}, kappa {kappa:.3f}")
for i in ids:
    l = labels[i]
    if l["label"] != gold[i]["answer"] or l.get("ambigua"):
        print(i, "gold", gold[i]["answer"], "label", l["label"], "ambigua", l.get("ambigua"), l.get("nota", ""))
