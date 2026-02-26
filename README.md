# 📄 Financial Document Analyzer – Debug & Enhancement Project

## 📌 Overview

This project is a **Financial Document Analyzer API** built using **FastAPI** and **CrewAI**.
It allows users to upload financial PDF documents (e.g., earnings reports), analyze them using an LLM, and receive a concise financial summary.

As part of an **AI Internship Debug Challenge**, the original codebase contained:

* deterministic bugs
* dependency conflicts
* inefficient prompts
* architectural issues

This repository contains a **fully debugged, stabilized, and enhanced version** of the system, with **database integration as a bonus feature**.

---

## 🎯 Key Features

* 📤 Upload financial PDF documents
* 🤖 LLM-powered financial analysis
* 📉 Investment and risk insights
* 🗄️ Persistent storage of analysis results (SQLite)
* 📜 Swagger UI for easy testing
* 🧠 Production-grade fixes and design decisions

---

## 🧱 Tech Stack

* **Backend**: FastAPI
* **Agent Framework**: CrewAI (`0.130.0`)
* **LLM Provider**: OpenAI (`gpt-4o-mini`)
* **ORM / Database**: SQLAlchemy + SQLite
* **PDF Parsing**: LangChain Community (`PyPDFLoader`)
* **Server**: Uvicorn

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <your-github-repo-link>
cd financial-document-analyzer-debug
```

### 2️⃣ Create and activate virtual environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

> **Important dependency note**
> FastAPI file uploads require:

```bash
pip install python-multipart
```

---

### 4️⃣ Environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

### 5️⃣ Run the application

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🔍 API Endpoints

### ▶️ POST `/analyze`

Upload a financial PDF and receive an analysis.

**Inputs**

* `file`: PDF document
* `query`: Optional analysis prompt

**Output**

* Financial summary
* Analysis stored in database

---

### ▶️ GET `/history` 

Retrieve past analysis results stored in SQLite.

---

## 🐞 Bugs Found & Fixes 

### 1️⃣ CrewAI Tool Compatibility Bug

**Issue**

* `crewai_tools.Tool` objects were incompatible with CrewAI `0.130.0`

**Root Cause**

* CrewAI strictly requires tools to subclass `BaseTool` and implement `_run()`

**Fix**

* Refactored all tools to inherit from `BaseTool`

---

### 2️⃣ `crewai.rag` Import Error

**Issue**

* `ModuleNotFoundError: crewai.rag`

**Root Cause**

* Version mismatch between `crewai` and `crewai-tools`

**Fix**

* Pinned compatible versions
* Removed unused RAG dependencies

---

### 3️⃣ LangChain Version Conflicts

**Issue**

* `ModelProfile` import errors

**Root Cause**

* Breaking changes in newer LangChain versions

**Fix**

* Pinned stable LangChain `0.1.x` versions compatible with CrewAI

---

### 4️⃣ FastAPI Multipart Error

**Issue**

* File upload failed with `python-multipart` error

**Fix**

* Added `python-multipart` dependency

---

### 5️⃣ PDF Not Reaching the LLM

**Issue**

* LLM responded with generic text (“I don’t have the file”)

**Root Cause**

* Uploaded `file_path` was never passed to CrewAI

**Fix**

* Passed `file_path` into `Crew.kickoff()`
* Updated task instructions to explicitly read the PDF

---

### 6️⃣ LLM Provider Misconfiguration

**Issue**

* `LLM Provider NOT provided` error

**Root Cause**

* LiteLLM requires explicit provider identification

**Fix**

* Switched to CrewAI native `LLM` wrapper
* Explicitly defined OpenAI model

---

### 7️⃣ Groq Rate Limit (TPM) Error

**Issue**

* Large PDFs exceeded Groq token limits

**Fix**

* Switched to **OpenAI `gpt-4o-mini`**
* Truncated PDF text before inference

---

### 8️⃣ Excessively Large Output

**Issue**

* Very long analysis responses

**Fix**

* Improved task prompts with:

  * word limits
  * bullet-point constraints
* Updated agent goals to favor concise summaries

---

## 🧠 Prompt Optimization

### Before

* Open-ended instructions
* Encouraged verbose output

### After

* Explicit limits:

  * 5–7 bullet points
  * ≤ 200 words
* Executive-summary style responses

---

## 🗄️ Database Integration 

### Why Database?

* Persist analysis results
* Enable auditability
* Support future analytics

### Implementation

* **SQLite** for lightweight storage
* **SQLAlchemy ORM**
* Automatic table creation on app start

### Stored Fields

* File name
* User query
* Generated summary
* Model used
* Timestamp

### Design Choice Rationale

> SQLite is ideal for demos and early-stage systems.
> The architecture can be migrated to PostgreSQL by changing the connection string without modifying business logic.

---

## 📐 Architecture Flow

```
User uploads PDF
        ↓
FastAPI endpoint
        ↓
CrewAI agent execution
        ↓
LLM analysis (OpenAI)
        ↓
Result saved to SQLite
        ↓
Response returned to user
```

---

## 🧪 Cost Optimization

* Used **OpenAI `gpt-4o-mini`**
* Low-cost summarization model
* Approx. $0.01–$0.03 per analysis
* Suitable for limited credits

---

## 📦 requirements.txt (Key Dependencies)

```txt
crewai==0.130.0
fastapi
uvicorn
sqlalchemy
python-multipart
langchain==0.1.20
langchain-core==0.1.53
langchain-community==0.0.38
litellm
python-dotenv
```

---

## 🚀 Future Improvements

* Chunk-based summarization (true RAG pipeline)
* PostgreSQL integration
* Async task queue (Celery / Redis)
* Frontend dashboard

---

## 🏁 Conclusion

This project demonstrates:

* Real-world debugging skills
* Deep understanding of GenAI frameworks
* Clean backend architecture
* Production-oriented decision making

> All original issues were resolved **without downgrading CrewAI** respecting project constraints.

---
