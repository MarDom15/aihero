# day5_hf_faq_agent_corrected.py

import os
import json
import secrets
import random
from pathlib import Path
from datetime import datetime, timezone
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from pydantic import BaseModel

# -------------------------------
# 1️⃣ Configuration Hugging Face
# -------------------------------
os.environ["HF_API_KEY"] = "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"
MODEL_NAME = "tiiuae/falcon-7b-instruct"  # Hugging Face modèle open source
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200)

# -------------------------------
# 2️⃣ Base FAQ
# -------------------------------
faq_index = [
    {"filename": "faq1.md", "content": "To install Kafka in Python, use pip install kafka-python."},
    {"filename": "faq2.md", "content": "You can join late and still get a certificate if you finish the capstone projects."},
    {"filename": "faq3.md", "content": "Docker on Windows can be installed via Docker Desktop."},
]

def search_faq(query, num_results=5):
    query_lower = query.lower()
    results = []
    for doc in faq_index:
        if any(word in doc["content"].lower() for word in query_lower.split() if len(word) > 2):
            results.append(doc)
    return results[:num_results]

# -------------------------------
# 3️⃣ Logging
# -------------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def log_interaction(question, answer, source="user", context=None):
    ts = datetime.now(timezone.utc)
    rand_hex = secrets.token_hex(3)
    filename = f"faq_agent_{ts.strftime('%Y%m%d_%H%M%S')}_{rand_hex}.json"
    filepath = LOG_DIR / filename
    entry = {
        "timestamp": ts.isoformat(),
        "question": question,
        "answer": answer,
        "source": source,
        "context": context,
    }
    with open(filepath, "w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)
    return filepath

# -------------------------------
# 4️⃣ Question Answering
# -------------------------------
def answer_question(question):
    results = search_faq(question)
    if results:
        context = "\n".join([f"{r['content']} (source: {r['filename']})" for r in results])
    else:
        context = "No relevant FAQ found. Use your knowledge to answer the question."
    prompt = f"Use the FAQ context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    output = generator(prompt, max_new_tokens=200, do_sample=True)[0]["generated_text"]
    return output, context

# -------------------------------
# 5️⃣ Evaluation
# -------------------------------
class EvaluationCheck(BaseModel):
    check_name: str
    justification: str
    check_pass: bool

class EvaluationChecklist(BaseModel):
    checklist: list[EvaluationCheck]
    summary: str

def simple_evaluator(question, answer, context):
    checklist = []
    # Check 1: relevance
    check_pass = any(word.lower() in answer.lower() for word in question.split() if len(word) > 3)
    checklist.append(EvaluationCheck(
        check_name="answer_relevant",
        justification="Answer contains keywords from the question.",
        check_pass=check_pass
    ))
    # Check 2: references
    check_pass = "source:" in answer
    checklist.append(EvaluationCheck(
        check_name="answer_citations",
        justification="Answer includes source references from FAQ.",
        check_pass=check_pass
    ))
    summary = f"{sum(c.check_pass for c in checklist)}/{len(checklist)} checks passed."
    return EvaluationChecklist(checklist=checklist, summary=summary)

# -------------------------------
# 6️⃣ AI-generated Test Data
# -------------------------------
question_generation_prompt = """
You are helping to create test questions for an AI agent that answers questions about a data engineering course.
Based on the provided FAQ content, generate realistic questions that students might ask.
The questions should be natural and varied in style, and include both technical and general questions.
"""

def generate_questions(num_questions=5):
    prompts = [doc['content'] for doc in random.sample(faq_index, min(num_questions, len(faq_index)))]
    questions = []
    for p in prompts:
        prompt = f"{question_generation_prompt}\nFAQ content:\n{p}\nQuestion:"
        q = generator(prompt, max_new_tokens=50, do_sample=True)[0]["generated_text"]
        questions.append(q.strip().split("\n")[-1])
    return questions

# -------------------------------
# 7️⃣ Main Interactive Loop
# -------------------------------
if __name__ == "__main__":
    print("HF FAQ Agent ready! Type 'exit' to quit.")
    while True:
        question = input("Question: ")
        if question.lower() in ["exit", "quit"]:
            break

        answer, context = answer_question(question)
        print("\nAnswer:\n", answer, "\n")

        # Log the interaction
        log_file = log_interaction(question, answer, context=context)
        print("Logged interaction to:", log_file)

        # Evaluate
        evaluation = simple_evaluator(question, answer, context)
        print("Evaluation Summary:", evaluation.summary)
        for check in evaluation.checklist:
            print(check)
        print("\n---\n")
