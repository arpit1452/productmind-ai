# ProductMind AI

AI-powered Product Management Agent that generates:

* 📊 Market Research
* 📄 Product Requirement Documents (PRD)
* 📈 Feature Prioritization (RICE)
* 🔍 Critical Product Review

---

## Tech Stack

* LangChain
* Groq LLM
* FastAPI (Backend)
* Streamlit (Frontend)
* RAG (Retrieval-Augmented Generation)

---

## Features

* Multi-agent tool-based reasoning
* Search + RAG integration
* End-to-end product planning pipeline
* PDF export of generated outputs

---

## Project Structure

```
app/         → Backend (agents, tools, pipelines)
frontend/    → Streamlit UI
```

---

## How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run backend

```
uvicorn app.main:app --reload
```

### 3. Run frontend

```
streamlit run frontend/app.py
```

---

## Example Use Case

Input:

```
AI fitness app for college students
```

Output:

* Market analysis
* PRD
* Feature roadmap
* Prioritization
* Recommendations

---

## Future Improvements

* Better UI/UX
* Real-time tool outputs
* Multi-user support
* Deployment (AWS / Docker)

---

## Author

Arpit Kumar
