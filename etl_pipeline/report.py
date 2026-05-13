# report.py — auto-generates daily weather summary report

import pandas as pd
import os
from datetime import datetime
from load import query_db
from config import REPORTS_DIR

def generate_report():
    today = datetime.now().strftime("%Y-%m-%d")

    # SQL query to summarise today's data per city
    # ROUND() makes numbers clean in the output
    # AVG() = average, MAX() = highest, MIN() = lowest
    # The LIKE with % means "starts with today's date"
    sql = f"""
        SELECT
            city,
            ROUND(AVG(temp_c), 1)          AS avg_temp_c,
            ROUND(MAX(temp_c), 1)          AS max_temp_c,
            ROUND(MIN(temp_c), 1)          AS min_temp_c,
            ROUND(AVG(humidity), 0)        AS avg_humidity_pct,
            ROUND(AVG(wind_speed), 1)      AS avg_wind_ms,
            ROUND(AVG(felt_heat_index), 1) AS avg_felt_heat,
            heat_category,
            SUM(CASE WHEN high_wind_alert = 1
                THEN 1 ELSE 0 END)         AS high_wind_readings,
            COUNT(*)                        AS total_readings
        FROM weather_readings
        WHERE extracted_at LIKE '{today}%'
        GROUP BY city
        ORDER BY avg_temp_c DESC
    """

    report_df = query_db(sql)

    # Create reports folder if it does not exist yet
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Save report as CSV with today's date in filename
    filename = f"{REPORTS_DIR}/weather_report_{today}.csv"
    report_df.to_csv(filename, index=False)

    print(f"\n=== DAILY REPORT: {today} ===")
    print(report_df.to_string(index=False))
    print(f"\nReport saved: {filename}")
    return report_df

if __name__ == "__main__":
    generate_report()