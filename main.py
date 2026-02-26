# main.py

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from database import init_db, SessionLocal, AnalysisResult

from crewai import Crew, Process

from agents import financial_analyst, risk_assessor, verifier
from task import (
    analyze_financial_document,
    investment_analysis,
    risk_assessment,
    verification
)

app = FastAPI(title="Financial Document Analyzer")

init_db()


# ---------------------------------
# Crew Runner
# ---------------------------------
def run_crew(query: str, file_path: str):
    """
    Run CrewAI pipeline on uploaded financial document
    """
    financial_crew = Crew(
        agents=[financial_analyst, risk_assessor, verifier],
        tasks=[
            analyze_financial_document,
            investment_analysis,
            risk_assessment,
            verification
        ],
        process=Process.sequential,
        verbose=True
    )

    result = financial_crew.kickoff(
        inputs={
            "query": query,
            "file_path": file_path
        }
    )

    return result


# ---------------------------------
# Health Check
# ---------------------------------
@app.get("/")
def root():
    return {"message": "Financial Document Analyzer API is running"}


# ---------------------------------
# Analyze Financial Document
# ---------------------------------
@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        if not query:
            query = "Analyze this financial document"

        # 🔹 1. RUN CREW (this already exists)
        response = run_crew(query=query.strip(), file_path=file_path)

        # 🔹 2. SAVE RESULT TO DATABASE (STEP 3 — ADD HERE)
        db = SessionLocal()
        db_record = AnalysisResult(
            file_name=file.filename,
            query=query,
            summary=str(response),
            model_used="gpt-4o-mini"
        )
        db.add(db_record)
        db.commit()
        db.close()

        # 🔹 3. RETURN API RESPONSE
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}"
        )

    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

@app.get("/history")
def get_analysis_history():
    db = SessionLocal()
    records = db.query(AnalysisResult).order_by(AnalysisResult.created_at.desc()).all()
    db.close()

    return records


# ---------------------------------
# Local Development Runner
# ---------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)