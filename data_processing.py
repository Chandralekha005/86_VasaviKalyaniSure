import pandas as pd
import os

# -----------------------------
# PATH CONFIGURATION
# -----------------------------

DATA_DIR = "data/sec_data/extracted_2019q1"
OUTPUT_DIR = "outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "financial_metrics.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# LOAD SEC DATASETS
# -----------------------------

print("Loading SEC TXT files...")

num = pd.read_csv(f"{DATA_DIR}/num.txt", sep="\t", low_memory=False)
pre = pd.read_csv(f"{DATA_DIR}/pre.txt", sep="\t", low_memory=False)
sub = pd.read_csv(f"{DATA_DIR}/sub.txt", sep="\t", low_memory=False)

print("num shape:", num.shape)
print("pre shape:", pre.shape)
print("sub shape:", sub.shape)

# -----------------------------
# FILTER INCOME STATEMENT DATA
# -----------------------------

# Keep only Income Statement entries
pre_is = pre[pre["stmt"] == "IS"]

# Join NUM with PRE to get statement context
num_is = num.merge(
    pre_is[["adsh", "tag", "version"]],
    on=["adsh", "tag", "version"],
    how="inner"
)

# -----------------------------
# EXTRACT KEY FINANCIAL METRICS
# -----------------------------

KEY_TAGS = ["Revenues", "NetIncomeLoss"]

financials = num_is[num_is["tag"].isin(KEY_TAGS)]

financials = financials.merge(
    sub[["adsh", "name", "fy", "fp"]],
    on="adsh",
    how="left"
)

# -----------------------------
# PIVOT INTO ANALYSIS TABLE
# -----------------------------

pivot_df = financials.pivot_table(
    index=["name", "fy", "fp"],
    columns="tag",
    values="value",
    aggfunc="first"
).reset_index()

pivot_df.rename(
    columns={
        "Revenues": "revenue",
        "NetIncomeLoss": "net_income"
    },
    inplace=True
)

# -----------------------------
# COMPUTE KPIs
# -----------------------------

pivot_df = pivot_df.sort_values(["name", "fy", "fp"])

pivot_df["revenue_yoy"] = pivot_df.groupby("name")["revenue"].pct_change(4)
pivot_df["revenue_qoq"] = pivot_df.groupby("name")["revenue"].pct_change(1)
pivot_df["profit_margin"] = pivot_df["net_income"] / pivot_df["revenue"]

# -----------------------------
# SAVE OUTPUT
# -----------------------------

pivot_df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ Data processing completed successfully.")
print(f"📁 Financial metrics saved to: {OUTPUT_FILE}")
