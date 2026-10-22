"""Draw the 15 item human spot check from the final 500.

One item per topic batch plus 3 more at random, fixed seed. The sheet has no
answers; the key goes to a separate file so the check stays blind.
"""

import json
import random

SEED = 20261022

items = json.load(open("benchpress_es_500.json"))
rng = random.Random(SEED)
picked = []
for b in sorted({c["batch"] for c in items}):
    picked.append(rng.choice([c for c in items if c["batch"] == b]))
picked += rng.sample([c for c in items if c not in picked], 3)
picked.sort(key=lambda c: c["final_id"])

lines = ["# Revisión humana de BenchPress: 15 ítems", "",
         "Responde cada pregunta sin buscar la respuesta. Escribe la letra que elijas y marca «ambigua» "
         "si hay más de una respuesta defendible o ninguna. La clave está en `key.json`; no la abras hasta terminar.", ""]
for n, c in enumerate(picked, 1):
    lines += [f"## {n}. Ítem {c['final_id']} ({c['category']})", "", c["question"], ""]
    lines += [f"- {ch}" for ch in c["choices"]]
    lines += ["", "Tu respuesta: ___  ¿Ambigua? ___", ""]
open("spot_check/sheet.md", "w").write("\n".join(lines))
key = [{"n": n, "final_id": c["final_id"], "answer": c["answer"], "difficulty": c["difficulty"],
        "justification": c["justification"]} for n, c in enumerate(picked, 1)]
json.dump(key, open("spot_check/key.json", "w"), ensure_ascii=False, indent=1)
print(len(picked), "items:", [c["final_id"] for c in picked])
print("difficulty:", {d: sum(c["difficulty"] == d for c in picked) for d in ("easy", "medium", "hard")})
