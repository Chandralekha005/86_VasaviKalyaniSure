import pandas as pd
from rag_pipeline import build_vectorstore
from mdna_generator import generate_full_mdna
from build_kpi_context import build_kpi_context

# -----------------------------
# 1. Load financial metrics
# -----------------------------
df = pd.read_csv("outputs/financial_metrics.csv")

# Pick latest valid record
metrics = df.dropna().iloc[-1].to_dict()

print("Using metrics for company:", metrics.get("name"))

# -----------------------------
# 2. Build KPI-based narrative context
# -----------------------------
context_text = build_kpi_context(metrics)

# -----------------------------
# 3. Build vector store (RAG)
# -----------------------------
vectorstore = build_vectorstore(context_text)

# -----------------------------
# 4. Generate MD&A
# -----------------------------
mdna_text = generate_full_mdna(vectorstore, metrics)

# -----------------------------
# 5. Save output
# -----------------------------
with open("outputs/mdna_draft.md", "w", encoding="utf-8") as f:
    f.write(mdna_text)

print("✅ MD&A draft generated successfully")
