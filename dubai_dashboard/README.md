# Dubai Property Transactions Dashboard

## Live Dashboard

[Click to view interactive dashboard](https://public.tableau.com/app/profile/huma.mirza/viz/Book2_17787716042080/Dashboard2?publish=yes)

## Project Overview

End-to-end data analytics project on Dubai real estate transactions. Raw data was cleaned using Python and visualised in Tableau Public. Dataset: 339,929 rows covering 2019 to 2023.

## Key Findings

1. **Marsa Dubai leads all areas** with AED 68.47B in total transaction value, followed by Palm Jumeirah (54.11B) and Burj Khalifa (45.51B)
2. **2022 was the peak year** — transaction value hit AED 290B, nearly 3x the 2020 low of AED 100B, reflecting Dubai's post-pandemic real estate boom
3. **Buildings command the highest average meter sale price** at ~16,000 AED/sqm, significantly above Villas, Land, and Units
4. **325,282 total transactions** recorded across the period with a combined value of AED 767B

## Data Cleaning (Python)

- Removed 14,646 duplicate rows
- Handled missing values across 5 columns (`property_sub_type_en`, `nearest_landmark_en`, `rooms_en`, `actual_worth`)
- Parsed and standardised date formats
- Applied IQR-based outlier capping on `procedure_area`, `actual_worth`, and `meter_sale_price`
- Removed invalid rows with zero or negative transaction values
- Standardised categorical casing and whitespace across all string columns

## Dashboard Features

- **KPI Cards** — Total transaction value, avg meter sale price, total transactions
- **Transaction Value by Year** — Area chart showing market trend 2019–2023
- **Top 10 Areas by Value** — Horizontal bar chart with gradient coloring
- **Avg Meter Sale Price by Property Type** — Grouped bar chart across Building, Unit, Land, Villa

## Skills Demonstrated

Python · Pandas · Data Cleaning · Outlier Detection · Tableau · Dashboard Design · UAE Real Estate Market

## Tools

- Python 3.11 with Pandas, NumPy and Matplotlib
- Tableau Public (free)
- Data source: Dubai Land Department (DLD)

## Repository Contents

- `clean_data.py` — full data cleaning pipeline
- `README.md` — project documentation
- Interactive dashboard available via Tableau Public link above
