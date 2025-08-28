"""Test how prompt format changes benchmark scores."""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


PROMPT_TEMPLATES = {
    "plain": "{question}\n{choices}\nAnswer:",
    "instruction": "Answer the following question.\n\nQuestion: {question}\nChoices: {choices}\nAnswer:",
    "chat": "User: {question}\n{choices}\nAssistant: The answer is",
    "numbered": "Q: {question}\n{choices}\nA:",
    "spanish": "Pregunta: {question}\nOpciones: {choices}\nRespuesta:",
    "cot": "Let's think step by step.\n\nQuestion: {question}\n{choices}\n\nThe answer is",
}

SAMPLE_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "choices": ["A) London", "B) Paris", "C) Berlin", "D) Madrid"],
        "answer": "B",
    },
    {
        "question": "Which planet is closest to the Sun?",
        "choices": ["A) Venus", "B) Earth", "C) Mercury", "D) Mars"],
        "answer": "C",
    },
    {
        "question": "What is 2 + 2?",
        "choices": ["A) 3", "B) 4", "C) 5", "D) 6"],
        "answer": "B",
    },
    {
        "question": "Which gas do plants absorb from the atmosphere?",
        "choices": ["A) Oxygen", "B) Nitrogen", "C) Carbon dioxide", "D) Hydrogen"],
        "answer": "C",
    },
    {
        "question": "Who wrote Romeo and Juliet?",
        "choices": ["A) Dickens", "B) Shakespeare", "C) Hemingway", "D) Twain"],
        "answer": "B",
    },
]


def format_prompt(template_name, question_data):
    """Format a question using a prompt template."""
    template = PROMPT_TEMPLATES[template_name]
    choices_str = "\n".join(question_data["choices"])
    return template.format(
        question=question_data["question"],
        choices=choices_str,
    )


def get_answer_logprobs(model, tokenizer, prompt, answer_tokens=None):
    """Get log probabilities for answer tokens given a prompt."""
    if answer_tokens is None:
        answer_tokens = ["A", "B", "C", "D"]

    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    # get logprobs at last position
    last_logits = outputs.logits[0, -1, :]
    logprobs = torch.log_softmax(last_logits, dim=-1)

    results = {}
    for token in answer_tokens:
        token_id = tokenizer.encode(token, add_special_tokens=False)
        if token_id:
            results[token] = logprobs[token_id[0]].item()
        else:
            results[token] = float("-inf")

    return results


def test_sensitivity(model_name="gpt2"):
    """Test how different prompt formats affect model answers."""
    print(f"Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    results = []
    for q in SAMPLE_QUESTIONS:
        q_results = {"question": q["question"], "correct": q["answer"]}
        for template_name in PROMPT_TEMPLATES:
            prompt = format_prompt(template_name, q)
            logprobs = get_answer_logprobs(model, tokenizer, prompt)
            predicted = max(logprobs, key=logprobs.get)
            q_results[f"{template_name}_pred"] = predicted
            q_results[f"{template_name}_correct"] = predicted == q["answer"]
        results.append(q_results)

    return results


def print_sensitivity_report(results):
    """Print a summary of prompt sensitivity."""
    templates = list(PROMPT_TEMPLATES.keys())
    print("\nPrompt sensitivity report")
    print("=" * 60)

    # per-template accuracy
    for t in templates:
        correct = sum(1 for r in results if r.get(f"{t}_correct", False))
        total = len(results)
        print(f"  {t:>15}: {correct}/{total} ({100*correct/total:.0f}%)")

    # agreement: how often do all templates agree?
    agree = 0
    for r in results:
        preds = [r.get(f"{t}_pred") for t in templates]
        if len(set(preds)) == 1:
            agree += 1
    print(f"\n  All templates agree: {agree}/{len(results)} ({100*agree/len(results):.0f}%)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt2")
    args = parser.parse_args()

    results = test_sensitivity(args.model)
    print_sensitivity_report(results)
