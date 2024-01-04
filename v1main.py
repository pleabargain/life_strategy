import matplotlib.pyplot as plt
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random

# Define the database model
Base = declarative_base()

class UserInput(Base):
    __tablename__ = 'user_input'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    input1 = db.Column(db.Integer)
    input2 = db.Column(db.Integer)
    input3 = db.Column(db.Integer)
    input4 = db.Column(db.Integer)
    input5 = db.Column(db.Integer)
    input6 = db.Column(db.Integer)
    input7 = db.Column(db.Integer)
    input8 = db.Column(db.Integer)
    input9 = db.Column(db.Integer)
    input10 = db.Column(db.Integer)
    input11 = db.Column(db.Integer)
    input12 = db.Column(db.Integer)
    input13 = db.Column(db.Integer)
    input14 = db.Column(db.Integer)
    input15 = db.Column(db.Integer)
    input16 = db.Column(db.Integer)

# Create an SQLite database in memory
engine = db.create_engine('sqlite:///:memory:', echo=False)
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Function to get integer input from user
def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter an integer.")

# Get user's name and 16 inputs
user_name = input("Enter your name: ")
inputs = [get_integer_input(f"Enter input {i+1}: ") for i in range(16)]

# Save the data to the database
user_data = UserInput(
    user_name=user_name,
    input1=inputs[0], input2=inputs[1], input3=inputs[2], input4=inputs[3],
    input5=inputs[4], input6=inputs[5], input7=inputs[6], input8=inputs[7],
    input9=inputs[8], input10=inputs[9], input11=inputs[10], input12=inputs[11],
    input13=inputs[12], input14=inputs[13], input15=inputs[14], input16=inputs[15]
)
session.add(user_data)
session.commit()

# Generate a bubble graph
x = [random.uniform(-10, 10) for _ in range(16)]
y = [random.uniform(-10, 10) for _ in range(16)]
sizes = [20 * abs(input) for input in inputs]

plt.scatter(x, y, s=sizes, alpha=0.5)

# Label quadrants
plt.text(5, 5, '1', fontsize=12)
plt.text(-5, 5, '2', fontsize=12)
plt.text(-5, -5, '3', fontsize=12)
plt.text(5, -5, '4', fontsize=12)

# Print user's name at the bottom
plt.text(0, -12, user_name, fontsize=12, ha='center')

plt.show()
