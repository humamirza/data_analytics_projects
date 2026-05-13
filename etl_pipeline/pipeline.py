# pipeline.py — runs the complete ETL pipeline
# This is the only file you need to run

from extract   import extract_weather
from transform import transform_weather
from load      import load_to_db
from report    import generate_report
import schedule
import time
from datetime import datetime

def run_pipeline():
    # Print a timestamp so you can see when each run happens
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*50}")
    print(f"Pipeline started at {now}")
    print(f"{'='*50}")

    # STEP 1: EXTRACT — pull from API
    print("\n[1/4] Extracting data from OpenWeatherMap...")
    raw_df = extract_weather()
    print(f"Extracted {len(raw_df)} records")

    # STEP 2: TRANSFORM — clean and enrich
    print("\n[2/4] Transforming data...")
    clean_df = transform_weather(raw_df)

    # STEP 3: LOAD — save to database
    print("\n[3/4] Loading to database...")
    load_to_db(clean_df)

    # STEP 4: REPORT — generate daily summary
    print("\n[4/4] Generating report...")
    generate_report()

    print(f"\nPipeline complete. Next run in 6 hours.")

# Run immediately when you start the script
run_pipeline()

# Then run every 6 hours automatically after that
# schedule.every(6).hours means: add this job to the scheduler
schedule.every(6).hours.do(run_pipeline)

# Keep the script running and check every 60 seconds
# if a scheduled job is due to run
while True:
    schedule.run_pending()
    time.sleep(60)