# extract.py — Step E in ETL
# This file fetches live weather data for 5 UAE cities

import requests
import pandas as pd
from datetime import datetime
from config import API_KEY, UAE_CITIES

def extract_weather():
    # This list will hold one dictionary per city
    records = []

    # Loop through each city in our list from config.py
    for city in UAE_CITIES:

        # Build the API URL
        # q = city name, appid = your key, units = metric for Celsius
        url    = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q":     city,
            "appid": API_KEY,
            "units": "metric"
        }

        # Send the request to the API
        # response is the raw reply from the server
        response = requests.get(url, params=params)

        # Check if the request worked (200 = success)
        if response.status_code != 200:
            print(f"ERROR fetching {city}: {response.status_code}")
            continue   # skip to next city if this one fails

        # Convert the JSON response to a Python dictionary
        data = response.json()

        # Extract the specific values we want from the response
        # data["main"] contains temperature and humidity
        # data["wind"] contains wind speed
        # data["weather"][0] contains description like "clear sky"
        records.append({
            "city":        city.split(",")[0],  # "Dubai" not "Dubai,AE"
            "temp_c":      data["main"]["temp"],
            "feels_like":  data["main"]["feels_like"],
            "humidity":    data["main"]["humidity"],
            "wind_speed":  data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"  Fetched: {city.split(',')[0]}")

    # Convert our list of dictionaries into a pandas DataFrame
    # This is the same as converting it to a table
    return pd.DataFrame(records)

# This block runs only when you run extract.py directly
# Use it to test that the API connection works
if __name__ == "__main__":
    print("Testing extract...")
    df = extract_weather()
    print(df)
    print(f"\nSuccessfully fetched {len(df)} city records")