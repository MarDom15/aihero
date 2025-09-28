# 🦾 AI Engineering Journey — Days 1 to 5  

Welcome to my personal journey of learning **AI Engineering** step by step.  
This repository contains the code, experiments, and notes I built while following the course.  

---

## 📅 Progress Overview  

### 🚀 Day 1 — Environment Setup  
- Installed **Python 3.13** and created a virtual environment (`venv`).  
- Installed essential packages:  
  - `transformers` 🤗  
  - `huggingface_hub`  
  - `pydantic`, `pandas`, `tqdm`  
- Created a first test script to check that everything runs properly.  

---

### 🚀 Day 2 — First AI Agent  
- Built a simple **FAQ Agent** with hardcoded answers.  
- The agent could:  
  - Accept user input (`question`)  
  - Search through a small FAQ list  
  - Return a matching answer if found  

👉 This was the foundation for building smarter agents.  

---

### 🚀 Day 3 — Logging & Evaluation  
- Added a **logging system** that saves all interactions in JSON files.  
- Each log entry includes:  
  - `timestamp`  
  - `question`  
  - `answer`  
  - `source` (user or AI-generated)  
- Implemented a **basic evaluator** to check:  
  - If the answer is relevant  
  - If it contains references/citations  

---

### 🚀 Day 4 — AI-Generated Test Data  
- Extended the FAQ agent to **generate synthetic questions** using Hugging Face models.  
- Implemented `generate_questions()` to create realistic student-style queries.  
- Automated batch evaluation by running generated questions against the FAQ system.  

---

### 🚀 Day 5 — Hugging Face Integration  
- Connected the FAQ Agent to a Hugging Face **LLM** (`tiiuae/falcon-7b-instruct`).  
- Added pipeline for **text generation** with context from FAQ.  
- Now the agent can:  
  - Search FAQs  
  - Use AI to generate a more natural answer  
  - Log + evaluate the interaction automatically  

✅ Example:  
```text
Question: How do I install Kafka in Python?  
Answer: To install Kafka in Python, use `pip install kafka-python`. (source: faq1.md)
