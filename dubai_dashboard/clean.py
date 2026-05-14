# # Step 1: Import pandas — this is the library that reads CSV files
# import pandas as pd

# # Step 2: Load your CSV file into a DataFrame
# # A DataFrame is like an Excel table inside Python
# df = pd.read_csv('data/raw_data.csv')

# # Step 3: See the first 5 rows
# # This shows you what the data actually looks like
# print("=== FIRST 5 ROWS ===")
# print(df.head())

# # Step 4: See column names and data types
# # int64 = whole numbers, float64 = decimals, object = text
# print("\n=== COLUMNS AND TYPES ===")
# print(df.info())

# # Step 5: Count missing values in each column
# # Any column showing a number has that many empty cells
# print("\n=== MISSING VALUES PER COLUMN ===")
# print(df.isnull().sum())

# # Step 6: Basic statistics for number columns
# # Shows min, max, average of each numeric column
# print("\n=== STATISTICS ===")
# print(df.describe())

# # Step 7: Total rows and columns
# print(f"\nTotal rows: {df.shape[0]}, Total columns: {df.shape[1]}")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
# ── 1. Load ────────────────────────────────────────────────────────────────────
df = pd.read_csv("data/raw_data.csv")
print(f"Original shape: {df.shape}")
 
# ── 2. Drop exact duplicates ───────────────────────────────────────────────────
df.drop_duplicates(inplace=True)
print(f"After dropping duplicates: {df.shape}")
 
# ── 3. Parse dates ─────────────────────────────────────────────────────────────
df["instance_date"] = pd.to_datetime(df["instance_date"], errors="coerce")
 
# ── 4. Strip whitespace from all string columns ────────────────────────────────
str_cols = df.select_dtypes(include="object").columns
df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())
 
# ── 5. Standardise categorical casing ─────────────────────────────────────────
cat_cols = [
    "trans_group_en", "property_type_en", "property_sub_type_en",
    "property_usage_en", "reg_type_en", "area_name_en",
    "nearest_landmark_en", "rooms_en",
]
for col in cat_cols:
    if col in df.columns:
        df[col] = df[col].str.title()
 
# ── 6. Handle missing values ───────────────────────────────────────────────────
# property_sub_type_en — high null count (~70k); fill with "Unknown"
df["property_sub_type_en"] = df["property_sub_type_en"].fillna("Unknown")
 
# nearest_landmark_en — optional field; fill with "Not Specified"
df["nearest_landmark_en"] = df["nearest_landmark_en"].fillna("Not Specified")
 
# rooms_en — optional for non-residential; fill with "Not Applicable"
df["rooms_en"] = df["rooms_en"].fillna("Not Applicable")
 
# actual_worth — ~1117 nulls; impute with median (robust to outliers)
median_worth = df["actual_worth"].median()
df["actual_worth"] = df["actual_worth"].fillna(median_worth)
 
# ── 7. Fix data types ─────────────────────────────────────────────────────────
# year was float because of nulls; now safe to cast to int
df["year"] = df["year"].astype(int)
 
# has_parking is already int (0/1); convert to bool for clarity
df["has_parking"] = df["has_parking"].astype(bool)
 
# ── 8. Remove outliers in numeric columns ──────────────────────────────────────
# Use IQR-based capping (Winsorisation) rather than dropping rows
 
def cap_outliers(series: pd.Series, lower_pct=0.01, upper_pct=0.99) -> pd.Series:
    """Cap values outside [lower_pct, upper_pct] quantiles."""
    lo = series.quantile(lower_pct)
    hi = series.quantile(upper_pct)
    return series.clip(lower=lo, upper=hi)
 
for col in ["procedure_area", "actual_worth", "meter_sale_price"]:
    df[col] = cap_outliers(df[col])
 
# ── 9. Validate business rules ─────────────────────────────────────────────────
# Drop rows where actual_worth or meter_sale_price is zero or negative
df = df[(df["actual_worth"] > 0) & (df["meter_sale_price"] >= 0)]
print(f"After business-rule validation: {df.shape}")
 
# ── 10. Consistent column ordering ────────────────────────────────────────────
desired_order = [
    "instance_date", "year",
    "trans_group_en", "reg_type_en",
    "property_type_en", "property_sub_type_en", "property_usage_en",
    "area_name_en", "nearest_landmark_en",
    "rooms_en", "has_parking",
    "procedure_area", "actual_worth", "meter_sale_price",
]
df = df[[c for c in desired_order if c in df.columns]]
 
# ── 11. Save cleaned file ──────────────────────────────────────────────────────
output_path = "cleaned_data.csv"
df.to_csv(output_path, index=False)
print(f"\nCleaned file saved → {output_path}")
print(f"Final shape: {df.shape}")
print("\nRemaining nulls:")
print(df.isnull().sum())
print("\nDtypes:")
print(df.dtypes)

# ── QUICK PREVIEW CHART ────────────────────────────────────────────────────────
top10 = (
    df.groupby("area_name_en")["actual_worth"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 5))
top10.plot(kind="bar", color="#185FA5")
plt.title("Top 10 Areas by Total Transaction Value — Dubai Property")
plt.ylabel("Total Value (AED)")
plt.xlabel("Area")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("screenshots/top10_preview.png")
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"{x/1e9:.0f}B AED")
)
plt.show()
print("Preview chart saved → screenshots/top10_preview.png")
 