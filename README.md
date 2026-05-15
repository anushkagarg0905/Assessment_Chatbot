# Conversational SHL Assessment Recommender

An AI-powered conversational recommendation system built for the SHL AI Intern Take-Home Assignment.

The system helps recruiters and hiring managers discover relevant SHL assessments through natural language conversation instead of manual keyword search.

---

# Features

- Conversational SHL assessment recommendations
- Semantic search using FAISS vector retrieval
- FastAPI backend with REST API
- SHL catalog grounded responses only
- Prompt injection protection
- Off-topic refusal handling
- Assessment comparison support
- Stateless conversation handling
- JSON schema-compliant responses

---

# Tech Stack

| Component | Technology |
|---|---|
| Backend API | FastAPI |
| Embedding Model | sentence-transformers |
| Vector Database | FAISS |
| Web Scraping | BeautifulSoup |
| Language Model | Gemini (optional) |
| Deployment | Render |

---

# Project Structure

```text
shl-assessment/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── catalog/
│   ├── assessments.json
│   ├── faiss.index
│   └── metadata.pkl
│
├── scraper/
│   └── scrape_shl.py
│
├── rag/
│   ├── __init__.py
│   ├── embed.py
│   └── retrieve.py
│
├── prompts/
│
├── tests/
│   ├── __init__.py
│   └── test_retrieval.py
│
└── utils/

