# Error
# raceback (most recent call last):
#   File "C:\Users\denni\OneDrive\Documents\life_strategy\main.py", line 
# 66, in <module>
#     data = [input_id, user_name] + [item for sublist in user_inputs for item in sublist]
# NameError: name 'input_id' is not defined

import sqlite3
import matplotlib.pyplot as plt
import uuid

# List of 16 values
values = [
    "Trust", "Tolerance", "Community", "Healthy_life_expectancy",
    "Financial_stability", "Freedom", "Social_relationships",
    "Positive_thinking_styles", "Temperament_Adaptation",
    "Society_and_culture", "Physical_health_and_attractiveness",
    "Love", "Exercise", "Relaxation", "Career_satisfaction", "Sleep"
]

# Function to prompt for user inputs with validation
def get_user_inputs():
    user_name = input("Enter your name: ")
    inputs = []
    for value in values:
        while True:
            try:
                score = int(input(f"Enter score (1-10) for {value}: "))
                if 1 <= score <= 10:
                    break
                else:
                    print("Score must be between 1 and 10.")
            except ValueError:
                print("Please enter a valid integer.")

        while True:
            try:
                quadrant = int(input(f"Enter quadrant (1-4) for {value}: "))
                if 1 <= quadrant <= 4:
                    break
                else:
                    print("Quadrant must be between 1 and 4.")
            except ValueError:
                print("Please enter a valid integer.")

        inputs.append((score, quadrant))
    return user_name, inputs



# Connect to the existing SQLite database
conn = sqlite3.connect('user_inputs.db')
cursor = conn.cursor()

# Create a new table schema for user inputs with UUID
cursor.execute('DROP TABLE IF EXISTS user_input;')

column_definitions = ', '.join([f"{value.lower().replace(' ', '_')}_score INTEGER, {value.lower().replace(' ', '_')}_quadrant INTEGER" for value in values])
column_names = ', '.join([f"{value.lower().replace(' ', '_')}_score, {value.lower().replace(' ', '_')}_quadrant" for value in values])

cursor.execute(f'''
    CREATE TABLE user_input (
        id TEXT PRIMARY KEY,
        user_name TEXT,
        {column_definitions}
    )
''')

# Get user inputs
user_name, user_inputs = get_user_inputs()

# Prepare data for insertion
data = [input_id, user_name] + [item for sublist in user_inputs for item in sublist]

# Insert the data into the table with a UUID
input_id = str(uuid.uuid4())
placeholders = ', '.join(['?'] * len(data))
cursor.execute(f'''
    INSERT INTO user_input (id, user_name, {column_names})
    VALUES ({placeholders})
''', data)

# Commit and close the connection
conn.commit()
conn.close()

# Generate a bubble graph
fig, ax = plt.subplots()
quadrant_positions = {
    1: (5, 5), 2: (-5, 5), 3: (-5, -5), 4: (5, -5)
}

for (value, score, quadrant) in zip(values, *[iter([item for sublist in user_inputs for item in sublist])] * 2):
    x, y = quadrant_positions[quadrant]
    ax.scatter(x, y, s=20 * score, alpha=0.5, label=value)

# Add labels
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Print user's name at the bottom
plt.text(0, -12, user_name, fontsize=12, ha='center')

# Show the graph
plt.show()
