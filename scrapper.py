import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Function to scrape match outcomes from a dynamic website using Selenium
def scrape_match_outcomes_dynamic(url_pattern, num_matches):
    outcomes = []

    # Set up the webdriver (make sure to download the appropriate driver for your browser)
    driver = webdriver.Chrome()

    for i in range(1, num_matches + 1):
        # Replace {} in url_pattern with the match number
        dynamic_url = url_pattern.format(i)
        
        # Visit the dynamic URL
        driver.get(dynamic_url)

        # Use explicit wait for the element to be present
        wait = WebDriverWait(driver, 30)
        
        # Adjust the locator to use XPath with text content
        result_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Teams")]')))

        # Extract match outcome
        result = result_element.text.strip() if result_element else 'Unknown'

        outcomes.append({'Match': i, 'Outcome': result})

        # Wait for 2 minutes before moving to the next match
        time.sleep(120)  # 120 seconds is 2 minutes

    # Close the webdriver
    driver.quit()

    return outcomes

# Function to predict match outcomes using logistic regression
def predict_match_outcomes(data, num_matches):
    df = pd.DataFrame(data)

    # Convert categorical variables to numerical
    df['Outcome'] = pd.Categorical(df['Outcome']).codes

    # Separate features and target variable
    X = df[['Match']]
    y = df['Outcome']

    # Check if we have both classes represented
    if len(df['Outcome'].unique()) < 2:
        print("Error: Not enough variety in historical data. Please provide more diverse data.")
        return None

    # Create a logistic regression model
    model = LogisticRegression()

    # Train the model (for simplicity, using the same data for training)
    model.fit(X, y)

    # Make predictions for future matches
    future_matches = pd.DataFrame({'Match': range(num_matches + 1, num_matches + 6)})
    future_matches['Predicted_Outcome'] = model.predict(future_matches[['Match']])

    return future_matches

# Example usage
url_pattern = 'https://www.betika.com/en-ke/virtuals/results/6{}'
num_matches_to_monitor = 8

# Scrape match outcomes from dynamic URLs
match_outcomes_data = scrape_match_outcomes_dynamic(url_pattern, num_matches_to_monitor)

# Print the scraped data
print(pd.DataFrame(match_outcomes_data))

# Predict future match outcomes
future_match_predictions = predict_match_outcomes(match_outcomes_data, num_matches_to_monitor)

# Check if predictions are available before printing
if future_match_predictions is not None:
    # Print the predicted outcomes for future matches
    print(future_match_predictions)
