import pandas as pd
from sklearn.linear_model import LogisticRegression

# Get user input for historical match data
num_matches = int(input("Enter the number of historical matches: "))
historical_data = []

for i in range(num_matches):
    team1_goals = int(input(f"Enter goals scored by Team 1 in match {i+1}: "))
    team2_goals = int(input(f"Enter goals scored by Team 2 in match {i+1}: "))
    result = input(f"Enter result (e.g., 'Under 3' or 'Over 3') for match {i+1}: ")

    historical_data.append({'goals_team1': team1_goals, 'goals_team2': team2_goals, 'result': result})

# Create a DataFrame from user input
df = pd.DataFrame(historical_data)

# Convert categorical variables to numerical
df['result'] = pd.Categorical(df['result']).codes

# Create a new column for total goals
df['total_goals'] = df['goals_team1'] + df['goals_team2']

# Define a threshold for over/under 3 goals
threshold = 3
df['outcome'] = df['total_goals'].apply(lambda x: 1 if x > threshold else 0)

# Separate features and target variable
X = df[['goals_team1', 'goals_team2']]
y = df['outcome']

# Create a logistic regression model
model = LogisticRegression()

# Train the model
model.fit(X, y)

# Get user input for the current match
current_team1_goals = int(input("Enter goals scored by Team 1 in the current match: "))
current_team2_goals = int(input("Enter goals scored by Team 2 in 1the current match: "))

# Make a prediction based on the current match data
current_match_outcome = model.predict([[current_team1_goals, current_team2_goals]])[0]

# Print the prediction
if current_match_outcome == 0:
    print("The model predicts the current match outcome will be Under 3 goals.")
else:
    print("The model predicts the current match outcome will be Over 3 goals.")
