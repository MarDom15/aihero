<<<<<<< HEAD
# hf_faq_evaluation.py
import json
import secrets
from pathlib import Path
from datetime import datetime
import random
import pandas as pd

from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List, Any

# -----------------------------
# 1️⃣ Répertoire de logs
# -----------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# -----------------------------
# 2️⃣ Fonction de recherche (exemple)
# -----------------------------
def text_search(query: str) -> List[Any]:
    """
    Exemple de recherche dans un index FAQ.
    Remplace par ton vrai index.
    """
    return [{"filename": "example.md", "content": "Install Kafka using pip install kafka-python"}]

# -----------------------------
# 3️⃣ Agent FAQ Hugging Face
# -----------------------------
system_prompt = """
You are a helpful assistant for a course.

Use the search tool to find relevant information from the course materials before answering questions.
Always include references by citing the filename of the source material you used.
"""

faq_agent = Agent(
    name="faq_agent",
    instructions=system_prompt,
    tools=[text_search],
    model="tiiuae/falcon-7b-instruct"  # Hugging Face HF model
)

# -----------------------------
# 4️⃣ Logging des interactions
# -----------------------------
def log_entry(agent, messages, source="user"):
    tools = []
    for ts in agent.toolsets:
        tools.extend(ts.tools.keys())
    dict_messages = [m.dict() if hasattr(m, "dict") else m for m in messages]
    return {
        "agent_name": agent.name,
        "system_prompt": agent._instructions,
        "model": agent.model.model_name,
        "tools": tools,
        "messages": dict_messages,
        "source": source
    }

def serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def log_interaction_to_file(agent, messages, source="user"):
    entry = log_entry(agent, messages, source)
    ts = datetime.utcnow()
    ts_str = ts.strftime("%Y%m%d_%H%M%S")
    rand_hex = secrets.token_hex(3)
    filename = f"{agent.name}_{ts_str}_{rand_hex}.json"
    filepath = LOG_DIR / filename
    with filepath.open("w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)
    return filepath

# -----------------------------
# 5️⃣ Génération automatique de questions
# -----------------------------
question_generation_prompt = """
You are helping to create test questions for an AI agent that answers questions about a data engineering course.

Based on the provided FAQ content, generate realistic questions that students might ask.
"""

class QuestionsList(BaseModel):
    questions: List[str]

question_generator = Agent(
    name="question_generator",
    instructions=question_generation_prompt,
    model="tiiuae/falcon-7b-instruct",
    output_type=QuestionsList
)

# Exemple simple: on génère 5 questions à partir de notre "index"
sample_docs = [{"content": "How to install Kafka in Python?"}, {"content": "How to use Docker on Windows?"}]
prompt_docs = [d["content"] for d in sample_docs]
questions_result = question_generator.run_sync(json.dumps(prompt_docs))
questions = questions_result.output.questions

# -----------------------------
# 6️⃣ Boucle automatique d’interactions
# -----------------------------
for q in questions:
    print("Question:", q)
    result = faq_agent.run_sync(user_prompt=q)
    print("Answer:", result.output, "\n")
    log_interaction_to_file(faq_agent, result.new_messages(), source="ai-generated")

# -----------------------------
# 7️⃣ Évaluation automatique (LLM-as-a-Judge)
# -----------------------------
class EvaluationCheck(BaseModel):
    check_name: str
    justification: str
    check_pass: bool

class EvaluationChecklist(BaseModel):
    checklist: List[EvaluationCheck]
    summary: str

evaluation_prompt = """
Use this checklist to evaluate an AI agent's answer (<ANSWER>) to a user question (<QUESTION>):
- instructions_follow: Did the agent follow the system prompt instructions?
- tool_call_search: Was the search tool invoked?
- answer_relevant: Does the answer address the question?
- answer_clear: Is the answer clear and correct?
- answer_citations: Are proper citations included?

Provide True/False for each check with a short justification.
"""

eval_agent = Agent(
    name="eval_agent",
    model="tiiuae/falcon-7b-instruct",
    instructions=evaluation_prompt,
    output_type=EvaluationChecklist
)

def load_log_file(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_log(log_record):
    messages = log_record["messages"]
    instructions = log_record["system_prompt"]
    question = messages[0]["parts"][0]["content"]
    answer = messages[-1]["parts"][0]["content"]
    log_simplified = json.dumps(messages)

    user_prompt = f"<INSTRUCTIONS>{instructions}</INSTRUCTIONS>\n<QUESTION>{question}</QUESTION>\n<ANSWER>{answer}</ANSWER>\n<LOG>{log_simplified}</LOG>"

    result = eval_agent.run_sync(user_prompt)
    return result.output

# -----------------------------
# 8️⃣ Évaluation de tous les logs
# -----------------------------
eval_rows = []
for log_file in LOG_DIR.glob("*.json"):
    log_record = load_log_file(log_file)
    eval_result = evaluate_log(log_record)
    row = {c.check_name: c.check_pass for c in eval_result.checklist}
    row["file"] = log_file.name
    eval_rows.append(row)

if eval_rows:
    df_eval = pd.DataFrame(eval_rows)
    print("\n=== Evaluation summary ===")
    print(df_eval)
    print("\n=== Average pass rate ===")
    print(df_eval.mean(numeric_only=True))
else:
    print("No logs to evaluate.")
=======
# hf_faq_evaluation.py
import json
import secrets
from pathlib import Path
from datetime import datetime
import random
import pandas as pd

from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List, Any

# -----------------------------
# 1️⃣ Répertoire de logs
# -----------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# -----------------------------
# 2️⃣ Fonction de recherche (exemple)
# -----------------------------
def text_search(query: str) -> List[Any]:
    """
    Exemple de recherche dans un index FAQ.
    Remplace par ton vrai index.
    """
    return [{"filename": "example.md", "content": "Install Kafka using pip install kafka-python"}]

# -----------------------------
# 3️⃣ Agent FAQ Hugging Face
# -----------------------------
system_prompt = """
You are a helpful assistant for a course.

Use the search tool to find relevant information from the course materials before answering questions.
Always include references by citing the filename of the source material you used.
"""

faq_agent = Agent(
    name="faq_agent",
    instructions=system_prompt,
    tools=[text_search],
    model="tiiuae/falcon-7b-instruct"  # Hugging Face HF model
)

# -----------------------------
# 4️⃣ Logging des interactions
# -----------------------------
def log_entry(agent, messages, source="user"):
    tools = []
    for ts in agent.toolsets:
        tools.extend(ts.tools.keys())
    dict_messages = [m.dict() if hasattr(m, "dict") else m for m in messages]
    return {
        "agent_name": agent.name,
        "system_prompt": agent._instructions,
        "model": agent.model.model_name,
        "tools": tools,
        "messages": dict_messages,
        "source": source
    }

def serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def log_interaction_to_file(agent, messages, source="user"):
    entry = log_entry(agent, messages, source)
    ts = datetime.utcnow()
    ts_str = ts.strftime("%Y%m%d_%H%M%S")
    rand_hex = secrets.token_hex(3)
    filename = f"{agent.name}_{ts_str}_{rand_hex}.json"
    filepath = LOG_DIR / filename
    with filepath.open("w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)
    return filepath

# -----------------------------
# 5️⃣ Génération automatique de questions
# -----------------------------
question_generation_prompt = """
You are helping to create test questions for an AI agent that answers questions about a data engineering course.

Based on the provided FAQ content, generate realistic questions that students might ask.
"""

class QuestionsList(BaseModel):
    questions: List[str]

question_generator = Agent(
    name="question_generator",
    instructions=question_generation_prompt,
    model="tiiuae/falcon-7b-instruct",
    output_type=QuestionsList
)

# Exemple simple: on génère 5 questions à partir de notre "index"
sample_docs = [{"content": "How to install Kafka in Python?"}, {"content": "How to use Docker on Windows?"}]
prompt_docs = [d["content"] for d in sample_docs]
questions_result = question_generator.run_sync(json.dumps(prompt_docs))
questions = questions_result.output.questions

# -----------------------------
# 6️⃣ Boucle automatique d’interactions
# -----------------------------
for q in questions:
    print("Question:", q)
    result = faq_agent.run_sync(user_prompt=q)
    print("Answer:", result.output, "\n")
    log_interaction_to_file(faq_agent, result.new_messages(), source="ai-generated")

# -----------------------------
# 7️⃣ Évaluation automatique (LLM-as-a-Judge)
# -----------------------------
class EvaluationCheck(BaseModel):
    check_name: str
    justification: str
    check_pass: bool

class EvaluationChecklist(BaseModel):
    checklist: List[EvaluationCheck]
    summary: str

evaluation_prompt = """
Use this checklist to evaluate an AI agent's answer (<ANSWER>) to a user question (<QUESTION>):
- instructions_follow: Did the agent follow the system prompt instructions?
- tool_call_search: Was the search tool invoked?
- answer_relevant: Does the answer address the question?
- answer_clear: Is the answer clear and correct?
- answer_citations: Are proper citations included?

Provide True/False for each check with a short justification.
"""

eval_agent = Agent(
    name="eval_agent",
    model="tiiuae/falcon-7b-instruct",
    instructions=evaluation_prompt,
    output_type=EvaluationChecklist
)

def load_log_file(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_log(log_record):
    messages = log_record["messages"]
    instructions = log_record["system_prompt"]
    question = messages[0]["parts"][0]["content"]
    answer = messages[-1]["parts"][0]["content"]
    log_simplified = json.dumps(messages)

    user_prompt = f"<INSTRUCTIONS>{instructions}</INSTRUCTIONS>\n<QUESTION>{question}</QUESTION>\n<ANSWER>{answer}</ANSWER>\n<LOG>{log_simplified}</LOG>"

    result = eval_agent.run_sync(user_prompt)
    return result.output

# -----------------------------
# 8️⃣ Évaluation de tous les logs
# -----------------------------
eval_rows = []
for log_file in LOG_DIR.glob("*.json"):
    log_record = load_log_file(log_file)
    eval_result = evaluate_log(log_record)
    row = {c.check_name: c.check_pass for c in eval_result.checklist}
    row["file"] = log_file.name
    eval_rows.append(row)

if eval_rows:
    df_eval = pd.DataFrame(eval_rows)
    print("\n=== Evaluation summary ===")
    print(df_eval)
    print("\n=== Average pass rate ===")
    print(df_eval.mean(numeric_only=True))
else:
    print("No logs to evaluate.")
>>>>>>> f3c52142e37a8a9db9630f7cb12bc087864267d7
