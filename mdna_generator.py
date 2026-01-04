from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

# -------------------------------------------------
# Initialize Hugging Face LLM (Open-source, Free)
# -------------------------------------------------
# FLAN-T5 is a text-to-text model with ~512 token limit
# So we must control context size carefully

hf_pipeline = pipeline(
    task="text2text-generation",
    model="google/flan-t5-base",
    max_new_tokens=400
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)

# -------------------------------------------------
# Helper: Truncate context to avoid token overflow
# -------------------------------------------------

def truncate_text(text: str, max_chars: int = 800) -> str:
    """
    Truncate text to keep input within FLAN-T5 limits.
    ~1200 characters is safe for 512 tokens.
    """
    return text[:max_chars]

# -------------------------------------------------
# Generate ONE MD&A Section (RAG + KPIs)
# -------------------------------------------------

def generate_mdna_section(
    section_title: str,
    query: str,
    vectorstore,
    metrics: dict
) -> str:
    """
    Generates a single MD&A section using:
    - Retrieved financial context (RAG)
    - Computed KPIs
    """

    # Retrieve limited number of chunks (RAG guardrail)
    docs = vectorstore.similarity_search(query, k=3)

    raw_context = "\n\n".join([d.page_content for d in docs])
    context = truncate_text(raw_context)

    prompt = prompt = f"""
You are a financial analyst writing the {section_title} section of an MD&A report.

Context (derived from financial KPIs):
{context}

Instructions:
- Focus ONLY on the purpose of the "{section_title}" section
- Do NOT repeat sentences from other sections
- Use analytical, professional language
- Do NOT invent numbers or facts
- Output concise Markdown paragraphs

Guidance:
- If section is Financial Performance Overview: summarize overall trends and performance
- If section is Revenue Drivers: explain possible causes behind revenue changes
- If section is Risk Factors: highlight financial risks and their implications
"""

    return llm.invoke(prompt)

# -------------------------------------------------
# Generate FULL MD&A Draft
# -------------------------------------------------

def generate_full_mdna(vectorstore, metrics: dict) -> str:
    """
    Generates the complete MD&A draft.
    """

    mdna = "# MD&A Draft\n\n"

    mdna += "## Financial Performance Overview\n"
    mdna += generate_mdna_section(
        "Financial Performance Overview",
        "overall financial performance and profitability trends",
        vectorstore,
        metrics
    )

    mdna += "\n\n## Revenue Drivers\n"
    mdna += generate_mdna_section(
        "Revenue Drivers",
        "revenue growth drivers and business segments",
        vectorstore,
        metrics
    )

    mdna += "\n\n## Risk Factors\n"
    mdna += generate_mdna_section(
        "Risk Factors",
        "business risks and uncertainties",
        vectorstore,
        metrics
    )

    mdna += "\n\n⚠️ Disclaimer\n"
    mdna += (
        "This MD&A draft is AI-generated for decision-support purposes only. "
        "Forecasts and interpretations are indicative and based on historical patterns. "
        "Human review is required before regulatory or investment use."
    )

    return mdna
