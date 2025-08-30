"""Build and run a custom Spanish language benchmark."""

import json
import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


# Custom Spanish multiple choice questions
SPANISH_BENCH = [
    {
        "question": "Cual es la capital de Colombia?",
        "choices": ["A) Lima", "B) Bogota", "C) Quito", "D) Caracas"],
        "answer": "B",
    },
    {
        "question": "Que rio es el mas largo de Sudamerica?",
        "choices": ["A) Orinoco", "B) Parana", "C) Amazonas", "D) Magdalena"],
        "answer": "C",
    },
    {
        "question": "En que ano llego Colon a America?",
        "choices": ["A) 1492", "B) 1500", "C) 1485", "D) 1510"],
        "answer": "A",
    },
    {
        "question": "Cual es el elemento quimico con simbolo Fe?",
        "choices": ["A) Fluor", "B) Fosforo", "C) Hierro", "D) Francio"],
        "answer": "C",
    },
    {
        "question": "Quien escribio Cien Anos de Soledad?",
        "choices": ["A) Borges", "B) Neruda", "C) Garcia Marquez", "D) Vargas Llosa"],
        "answer": "C",
    },
    {
        "question": "Cual es el pais mas grande de Centroamerica?",
        "choices": ["A) Guatemala", "B) Honduras", "C) Nicaragua", "D) Panama"],
        "answer": "C",
    },
    {
        "question": "Que planeta del sistema solar es conocido como el planeta rojo?",
        "choices": ["A) Jupiter", "B) Venus", "C) Marte", "D) Saturno"],
        "answer": "C",
    },
    {
        "question": "Cual es la moneda oficial de Mexico?",
        "choices": ["A) Dolar", "B) Euro", "C) Peso", "D) Sol"],
        "answer": "C",
    },
    {
        "question": "En que continente esta Egipto?",
        "choices": ["A) Asia", "B) Europa", "C) Africa", "D) Oceania"],
        "answer": "C",
    },
    {
        "question": "Cual es el hueso mas largo del cuerpo humano?",
        "choices": ["A) Humero", "B) Tibia", "C) Femur", "D) Radio"],
        "answer": "C",
    },
    {
        "question": "Que gas es necesario para la combustion?",
        "choices": ["A) Nitrogeno", "B) Oxigeno", "C) Hidrogeno", "D) Helio"],
        "answer": "B",
    },
    {
        "question": "Quien pinto La Noche Estrellada?",
        "choices": ["A) Picasso", "B) Dali", "C) Van Gogh", "D) Monet"],
        "answer": "C",
    },
    {
        "question": "Cual es el oceano mas grande del mundo?",
        "choices": ["A) Atlantico", "B) Indico", "C) Artico", "D) Pacifico"],
        "answer": "D",
    },
    {
        "question": "En que pais esta la Torre Eiffel?",
        "choices": ["A) Italia", "B) Francia", "C) Espana", "D) Alemania"],
        "answer": "B",
    },
    {
        "question": "Cuantos lados tiene un hexagono?",
        "choices": ["A) 5", "B) 6", "C) 7", "D) 8"],
        "answer": "B",
    },
]


def evaluate_custom(model_name="gpt2", questions=None, template="plain"):
    """Run custom benchmark on a model."""
    if questions is None:
        questions = SPANISH_BENCH

    print(f"Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    templates = {
        "plain": "Pregunta: {question}\n{choices}\nRespuesta:",
        "english": "Question: {question}\n{choices}\nAnswer:",
        "instruction": "Responde la siguiente pregunta.\n\nPregunta: {question}\nOpciones:\n{choices}\nRespuesta correcta:",
    }

    prompt_template = templates.get(template, templates["plain"])
    correct = 0
    total = len(questions)
    results = []

    for q in questions:
        choices_str = "\n".join(q["choices"])
        prompt = prompt_template.format(question=q["question"], choices=choices_str)

        inputs = tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        last_logits = outputs.logits[0, -1, :]
        logprobs = torch.log_softmax(last_logits, dim=-1)

        answer_probs = {}
        for letter in ["A", "B", "C", "D"]:
            token_ids = tokenizer.encode(letter, add_special_tokens=False)
            if token_ids:
                answer_probs[letter] = logprobs[token_ids[0]].item()

        predicted = max(answer_probs, key=answer_probs.get)
        is_correct = predicted == q["answer"]
        if is_correct:
            correct += 1

        results.append({
            "question": q["question"],
            "correct_answer": q["answer"],
            "predicted": predicted,
            "is_correct": is_correct,
            "probs": answer_probs,
        })

    accuracy = correct / total
    print(f"\nResults for {model_name} (template: {template}):")
    print(f"  Accuracy: {correct}/{total} ({accuracy:.1%})")

    return {"model": model_name, "accuracy": accuracy, "correct": correct, "total": total, "details": results}


def save_benchmark(questions=None, path="custom_bench.json"):
    """Save custom benchmark to JSON for sharing."""
    if questions is None:
        questions = SPANISH_BENCH
    with open(path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"Benchmark saved to {path} ({len(questions)} questions)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt2")
    parser.add_argument("--template", type=str, default="plain", choices=["plain", "english", "instruction"])
    parser.add_argument("--save", action="store_true", help="Save benchmark to JSON")
    args = parser.parse_args()

    if args.save:
        save_benchmark()
    else:
        evaluate_custom(model_name=args.model, template=args.template)
