import sqlite3
import random
import matplotlib.pyplot as plt

import uuid

# Connect to the existing SQLite database
conn = sqlite3.connect('user_inputs.db')
cursor = conn.cursor()

# Create a new table for user inputs with UUID
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_input (
        id TEXT PRIMARY KEY,
        user_name TEXT,
        input1 INTEGER, input2 INTEGER, input3 INTEGER, input4 INTEGER,
        input5 INTEGER, input6 INTEGER, input7 INTEGER, input8 INTEGER,
        input9 INTEGER, input10 INTEGER, input11 INTEGER, input12 INTEGER,
        input13 INTEGER, input14 INTEGER, input15 INTEGER, input16 INTEGER
    )
''')

# Simulating user's name and 16 random integer inputs
user_name = "Alice"
inputs = [random.randint(1, 10) for _ in range(16)]

# Insert the data into the table with a UUID
input_id = str(uuid.uuid4())
cursor.execute('''
    INSERT INTO user_input (id, user_name, input1, input2, input3, input4, 
                            input5, input6, input7, input8, input9, input10,
                            input11, input12, input13, input14, input15, input16)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (input_id, user_name, *inputs))

# Commit and close the connection
conn.commit()
conn.close()

# Generate a bubble graph
x = [random.uniform(-10, 10) for _ in range(16)]
y = [random.uniform(-10, 10) for _ in range(16)]
sizes = [20 * input for input in inputs]

plt.scatter(x, y, s=sizes, alpha=0.5)

# Label quadrants
plt.text(5, 5, '1', fontsize=12)
plt.text(-5, 5, '2', fontsize=12)
plt.text(-5, -5, '3', fontsize=12)
plt.text(5, -5, '4', fontsize=12)

# Print user's name at the bottom
plt.text(0, -12, user_name, fontsize=12, ha='center')

# Show the graph
plt.show()
