"""Merge items/batch_*.json into the 500 item candidate pool.

Drops duplicate items (same question and same correct answer) (within the pool and against the pilot and hard
sets), assigns ids, shuffles option positions with a fixed seed so the key is
balanced across A to D, and writes items_candidates.json (key and metadata)
plus blind chunks of 100 items for the labelers.

Usage: python build_items.py BLIND_DIR
"""

import glob
import json
import random
import re
import sys

SEED = 20261014
LETTERS = "ABCD"
blind_dir = sys.argv[1]


def norm(s):
    return re.sub(r"\W+", " ", s.lower()).strip()


def key(question, correct):
    return norm(question) + "|" + norm(correct)


seen = set()
for n in ("pilot_50.json", "pilot_hard_50.json"):
    for x in json.load(open(n)):
        right = x["choices"][LETTERS.index(x["answer"])][3:]
        seen.add(key(x["question"], right))
pool, dropped = [], []
for f in sorted(glob.glob("items/batch_*.json")):
    for x in json.load(open(f)):
        k = key(x["question"], x["correct"])
        if k in seen:
            dropped.append((f, x["question"]))
            continue
        seen.add(k)
        x["batch"] = f.split("_")[-1].split(".")[0]
        pool.append(x)

rng = random.Random(SEED)
positions = [i % 4 for i in range(len(pool))]
rng.shuffle(positions)

cands, blind = [], []
for i, (x, pos) in enumerate(zip(pool, positions)):
    opts = list(x["distractors"])
    rng.shuffle(opts)
    opts.insert(pos, x["correct"])
    choices = [f"{LETTERS[k]}) {o}" for k, o in enumerate(opts)]
    cands.append({"id": i + 1, "batch": x["batch"], "category": x["category"], "difficulty": x["difficulty"],
                  "question": x["question"], "choices": choices, "answer": LETTERS[pos], "justification": x["justification"]})
    blind.append({"id": i + 1, "question": x["question"], "choices": choices})

json.dump(cands, open("items_candidates.json", "w"), ensure_ascii=False, indent=1)
for c in range(0, len(blind), 100):
    json.dump(blind[c:c + 100], open(f"{blind_dir}/blind_{c // 100 + 1:02d}.json", "w"), ensure_ascii=False, indent=1)
print(len(cands), "candidates;", len(dropped), "dropped as duplicates")
for f, q in dropped:
    print("  dropped", f, q[:70])
print({L: sum(c["answer"] == L for c in cands) for L in LETTERS})
