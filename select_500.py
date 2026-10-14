"""Select the final 500 items from the validated candidates.

Survivors are items where both blind labelers match the key and neither
flagged ambiguity, minus items dropped by manual review (DROP below).
Selection is stratified random by topic batch and author difficulty
(30/40/30) with a fixed seed. It never looks at model results.
"""

import json
import random

SEED = 20261014
DROP = {36: "contested superlative (celebrísimo is also used)",
        38: "contested grammatical function of «tres accidentes» with impersonal haber",
        77: "borderline foreign word status, flagged by a labeler",
        89: "typographic variants EE. UU. vs EE.UU. flagged by a labeler",
        94: "aún/aun flagged by a labeler",
        104: "disputed authorship of La Celestina",
        169: "vague wording, flagged by both labelers",
        279: "Switzerland has no de jure capital"}

cands = json.load(open("items_candidates.json"))
lab = json.load(open("items_labels.json"))
ok = []
for c in cands:
    i = str(c["id"])
    a, b = lab["a"][i], lab["b"][i]
    if a["label"] == c["answer"] == b["label"] and not a["ambigua"] and not b["ambigua"] and c["id"] not in DROP:
        ok.append(c)
print(len(cands), "candidates,", len(ok), "survivors")

rng = random.Random(SEED)
batches = sorted({c["batch"] for c in ok})
base, extra = divmod(500, len(batches))
quota = {b: base + (1 if k < extra else 0) for k, b in enumerate(batches)}
final = []
for b in batches:
    items = [c for c in ok if c["batch"] == b]
    q = quota[b]
    want = {"easy": round(q * 0.3), "medium": round(q * 0.4)}
    want["hard"] = q - want["easy"] - want["medium"]
    for d in ("easy", "medium", "hard"):
        pool = [c for c in items if c["difficulty"] == d]
        rng.shuffle(pool)
        final += pool[:want[d]]
    short = q - sum(1 for c in final if c["batch"] == b)
    if short > 0:
        rest = [c for c in items if c not in final]
        rng.shuffle(rest)
        final += rest[:short]

final.sort(key=lambda c: c["id"])
for n, c in enumerate(final, 1):
    c["final_id"] = n
json.dump(final, open("benchpress_es_500.json", "w"), ensure_ascii=False, indent=1)
print(len(final), "selected")
for k in ("difficulty", "batch"):
    cnt = {}
    for c in final:
        cnt[c[k]] = cnt.get(c[k], 0) + 1
    print(k, dict(sorted(cnt.items())))
print("answers", {L: sum(c["answer"] == L for c in final) for L in "ABCD"})
