import mplcursors  # Import the mplcursors library



import numpy as np
import random
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
                quadrant = int(input(f"Enter quadrant \n1= H importance H satisfaction\n2=H importance L satisfaction\n3=L importance L satisfaction\n4=L importance H satisfaction for {value}: "))
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

# # Create a new table schema for user inputs with UUID
# cursor.execute('DROP TABLE IF EXISTS user_input;')

column_definitions = ', '.join([f"{value.lower().replace(' ', '_')}_score INTEGER, {value.lower().replace(' ', '_')}_quadrant INTEGER" for value in values])
column_names = ', '.join([f"{value.lower().replace(' ', '_')}_score, {value.lower().replace(' ', '_')}_quadrant" for value in values])

# cursor.execute(f'''
#     CREATE TABLE user_input (
#         id TEXT PRIMARY KEY,
#         user_name TEXT,
#         {column_definitions}
#     )
# ''')

# Get user inputs
user_name, user_inputs = get_user_inputs()

# Define a UUID for the new input record
input_id = str(uuid.uuid4())

# Prepare data for insertion
data = [input_id, user_name] + [item for sublist in user_inputs for item in sublist]

# Insert the data into the table with a UUID
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
colors = plt.cm.rainbow(np.linspace(0, 1, len(values)))  # Unique colors for each value

def randomize_position(quadrant):
    if quadrant == 1:
        return (random.uniform(0, 10), random.uniform(0, 10))
    elif quadrant == 2:
        return (random.uniform(-10, 0), random.uniform(0, 10))
    elif quadrant == 3:
        return (random.uniform(-10, 0), random.uniform(-10, 0))
    elif quadrant == 4:
        return (random.uniform(0, 10), random.uniform(-10, 0))
    


# Create scatter plots for each value and keep track of them
scatter_plots = []
for (value, score, quadrant), color in zip(zip(values, *[iter([item for sublist in user_inputs for item in sublist])] * 2), colors):
    x, y = randomize_position(quadrant)
    scatter_plot = ax.scatter(x, y, s=20 * score, alpha=0.5, color=color, label=value)
    scatter_plots.append((scatter_plot, value, score))

# Add labels with color key
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', markerscale=0.5)


# Label quadrants in the middle
ax.text(5, 5, "H importance H satisfaction", fontsize=12, ha='center', va='center')
ax.text(-5, 5, "H importance L satisfaction", fontsize=12, ha='center', va='center')
ax.text(-5, -5, "L importance L satisfaction", fontsize=12, ha='center', va='center')
ax.text(5, -5, "L importance H satisfaction", fontsize=12, ha='center', va='center')

# Print user's name at the bottom
plt.text(0, -12, user_name, fontsize=12, ha='center')


# Add hover functionality
cursor = mplcursors.cursor(hover=True)
@cursor.connect("add")
def on_add(sel):
    for scatter_plot, value, score in scatter_plots:
        if sel.artist == scatter_plot:
            sel.annotation.set(text=f"{value}: {score}")
            break


# Show the graph
plt.show()