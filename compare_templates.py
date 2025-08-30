"""Compare how different prompt templates affect Spanish benchmark scores."""

from custom_bench import evaluate_custom, SPANISH_BENCH


def compare_all_templates(model_name="gpt2"):
    """Run the Spanish benchmark with all available templates."""
    templates = ["plain", "english", "instruction"]
    results = {}

    for t in templates:
        result = evaluate_custom(model_name=model_name, template=t)
        results[t] = result["accuracy"]
        print()

    print("\nTemplate comparison:")
    print("-" * 40)
    for t, acc in results.items():
        bar = "#" * int(acc * 40)
        print(f"  {t:>15}: {acc:.1%} {bar}")

    best = max(results, key=results.get)
    worst = min(results, key=results.get)
    diff = results[best] - results[worst]
    print(f"\n  Best: {best} ({results[best]:.1%})")
    print(f"  Worst: {worst} ({results[worst]:.1%})")
    print(f"  Gap: {diff:.1%}")

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt2")
    args = parser.parse_args()
    compare_all_templates(args.model)
