# agents.py

import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from tools import (
    ReadFinancialDocumentTool,
    InvestmentAnalysisTool,
    RiskAssessmentTool
)

# -------------------------------
# Load LLM (Groq - LLaMA 3.3 70B)
# -------------------------------
from crewai.llm import LLM

llm = LLM(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)
# llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0,
#     api_key=os.getenv("GROQ_API_KEY")
# )

# Instantiate tools (IMPORTANT)
read_tool = ReadFinancialDocumentTool()
investment_tool = InvestmentAnalysisTool()
risk_tool = RiskAssessmentTool()

# -------------------------------
# Financial Analyst Agent
# -------------------------------
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
    "Analyze financial documents and provide concise, structured insights. "
    "Always keep responses brief, focused, and suitable for executive summaries."
),   
    backstory=(
        "You are an experienced financial analyst with deep knowledge of corporate "
        "financial statements, market trends, and investment fundamentals."
    ),
    tools=[read_tool, investment_tool],
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False
)

# -------------------------------
# Risk Assessment Agent
# -------------------------------
risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Identify and explain financial and market risks based on company data.",
    backstory=(
        "You specialize in identifying market, operational, and regulatory risks "
        "from financial disclosures."
    ),
    tools=[risk_tool],
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=False
)

# -------------------------------
# Document Verification Agent
# -------------------------------
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify whether a document is a valid financial report.",
    backstory=(
        "You ensure documents are relevant financial disclosures "
        "such as earnings reports, annual reports, or filings."
    ),
    tools=[read_tool],
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=False
)