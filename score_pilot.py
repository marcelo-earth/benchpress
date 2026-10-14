"""Score blind labels against the pilot answer key: agreement and Cohen's kappa."""

import json
import sys
from collections import Counter

gold = {g["id"]: g for g in json.load(open("pilot_50.json"))}
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
