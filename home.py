import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape match outcomes from a website
def scrape_match_outcomes(url, num_matches):
    outcomes = []

    for i in range(1, num_matches + 1):
        response = requests.get(f"{url}/match-{i}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Modify the following line based on the actual HTML structure
            result_element = soup.find('span', class_='match-result')
            
            # Extract match outcome or set to 'Unknown' if not found
            result = result_element.text.strip() if result_element else 'Unknown'

            outcomes.append({'Match': i, 'Outcome': result})
        else:
            print(f"Failed to fetch data for match-{i}. Status code: {response.status_code}")

    return outcomes


# Example usage
url = 'https://www.betika.com/en-ke/virtuals/results/6'
num_matches_to_scrape = 5

# Scrape match outcomes
match_outcomes = scrape_match_outcomes(url, num_matches_to_scrape)

# Create a DataFrame from the scraped data
df = pd.DataFrame(match_outcomes)

# Print the DataFrame
print(df)
