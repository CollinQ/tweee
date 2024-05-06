import requests
import json
from datetime import datetime, timedelta

# Function to generate date range
def generate_date_range(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

# Define start and end dates
start_date = datetime(2023, 4, 1)
end_date = datetime(2023, 7, 11)

# Generate URLs for each date in the specified range
base_url = "https://alexlitel.github.io/congresstweets/data/"
urls = [f"{base_url}{date.strftime('%Y-%m-%d')}.json" for date in generate_date_range(start_date, end_date)]

# List to store all the JSON data
all_tweets = []

# Loop through the URLs and fetch data
for url in urls:
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        try:
            data = response.json()
            all_tweets.extend(data)  # Add the data to the list
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {url}: {e}")
    else:
        print(f"Error fetching data from {url}: Status code {response.status_code}")

# Optionally, you can save the concatenated data to a file or process it further
with open('concatenated_tweets.json', 'w') as outfile:
    json.dump(all_tweets, outfile, indent=4)

# Print or return the concatenated data for verification
print(f"Total tweets collected: {len(all_tweets)}")
