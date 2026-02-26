# task.py

from crewai import Task
from agents import financial_analyst, verifier


# ---------------------------------
# Task 1: Analyze Financial Document
# ---------------------------------
analyze_financial_document = Task(
    description="""
You are given a financial PDF document stored at the following path:

{file_path}

Steps:
1. Read the financial document using the Read Financial Document tool.
2. Identify key financial metrics such as revenue, profit, and guidance.
3. Summarize the company’s financial performance.

IMPORTANT:
- Keep the final response concise.
- Limit the summary to **5–7 bullet points**.
- Do NOT exceed **200 words**.

User Query:
{query}
""",
    expected_output="""
A concise financial summary containing:
- Company overview (1–2 lines)
- Key financial highlights (5–7 bullet points)
""",
    agent=financial_analyst,
)

# ---------------------------------
# Task 2: Investment Analysis
# ---------------------------------
investment_analysis = Task(
    description="""
Based on the extracted financial data, provide high-level investment insights.

Steps:
1. Interpret financial performance.
2. Highlight potential growth opportunities.
3. Avoid speculative or unethical investment advice.
""",
    expected_output="""
Investment insights including:
- Growth outlook
- Strengths and weaknesses
- Long-term perspective
""",
    agent=financial_analyst,
    async_execution=False,
)

# ---------------------------------
# Task 3: Risk Assessment
# ---------------------------------
risk_assessment = Task(
    description="""
Assess potential risks based on the financial document.

Steps:
1. Identify market, operational, and regulatory risks.
2. Provide a balanced and realistic risk assessment.
""",
    expected_output="""
Risk assessment including:
- Key risk factors
- Risk severity (Low / Medium / High)
- Mitigation considerations
""",
    agent=financial_analyst,
    async_execution=False,
)

# ---------------------------------
# Task 4: Document Verification
# ---------------------------------
verification = Task(
    description="""
Verify whether the uploaded document is a valid financial document.

Steps:
1. Check document structure and content.
2. Confirm relevance to financial reporting.
""",
    expected_output="""
Verification result:
- Document type
- Confirmation of financial relevance
""",
    agent=verifier,
    async_execution=False,
)