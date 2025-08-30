"""Quick check of model sizes and configs."""

from transformers import AutoModelForCausalLM, AutoConfig


MODELS = [
    "gpt2",
    "gpt2-medium",
    "gpt2-large",
    "EleutherAI/pythia-160m",
    "EleutherAI/pythia-410m",
]


def get_model_info(model_name):
    """Get model config without downloading weights."""
    config = AutoConfig.from_pretrained(model_name)
    n_params = None

    # estimate params from config
    vocab = getattr(config, "vocab_size", 0)
    hidden = getattr(config, "n_embd", 0) or getattr(config, "hidden_size", 0)
    layers = getattr(config, "n_layer", 0) or getattr(config, "num_hidden_layers", 0)
    heads = getattr(config, "n_head", 0) or getattr(config, "num_attention_heads", 0)

    # rough param estimate
    if hidden and layers:
        n_params = vocab * hidden + layers * (12 * hidden**2) + vocab * hidden
        n_params = n_params // 1_000_000

    return {
        "model": model_name.split("/")[-1],
        "vocab": vocab,
        "hidden": hidden,
        "layers": layers,
        "heads": heads,
        "params_M": n_params,
    }


def print_model_table(models=None):
    """Print a comparison table of model configs."""
    if models is None:
        models = MODELS

    infos = [get_model_info(m) for m in models]

    try:
        from tabulate import tabulate
        print(tabulate(infos, headers="keys", tablefmt="github"))
    except ImportError:
        for info in infos:
            print(info)


if __name__ == "__main__":
    print_model_table()
