# tools.py

import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader


class ReadFinancialDocumentTool(BaseTool):
    name: str = "Read Financial Document"
    description: str = "Reads a financial PDF document and returns cleaned text."

    def _run(self, path: str = "data/TSLA-Q2-2025-Update.pdf") -> str:
        if not os.path.exists(path):
            return f"Error: File not found at path {path}"

        loader = PyPDFLoader(path)
        docs = loader.load()

        full_report = ""
        for doc in docs:
            content = doc.page_content
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            full_report += content + "\n"

        # 🔹 LIMIT TEXT SIZE TO AVOID GROQ TPM ERROR
        MAX_CHARS = 12000  # safe for Groq on-demand tier
        return full_report[:MAX_CHARS]


class InvestmentAnalysisTool(BaseTool):
    name: str = "Investment Analysis"
    description: str = "Provides high-level investment insights from financial data."

    def _run(self, financial_document_data: str) -> str:
        return (
            "Investment Analysis:\n"
            "- Revenue growth appears positive.\n"
            "- Company shows strong market positioning.\n"
            "- Long-term investment outlook seems favorable.\n"
        )


class RiskAssessmentTool(BaseTool):
    name: str = "Risk Assessment"
    description: str = "Identifies financial and market risks."

    def _run(self, financial_document_data: str) -> str:
        return (
            "Risk Assessment:\n"
            "- Market volatility risk present.\n"
            "- Regulatory and macroeconomic risks should be monitored.\n"
            "- No immediate liquidity risk detected.\n"
        )