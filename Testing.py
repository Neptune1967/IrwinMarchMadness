import tkinter as tk
from tkinter import ttk

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age} years old"

# Callback function for creating Person objects
def create_person():
    selected_name = name_var.get()
    selected_age = age_var.get()
    if selected_name and selected_age:
        person = Person(selected_name, int(selected_age))
        people.append(person)
        result_label.config(text=f"Created: {person}")
    else:
        result_label.config(text="Please select a name and an age.")

# Initialize the GUI window
root = tk.Tk()
root.title("Create Person Objects")

# List of names and ages for dropdowns
names = ["Alice", "Bob", "Charlie", "Diana"]
ages = ["20", "25", "30", "35"]

# Variable to hold the selected options
name_var = tk.StringVar()
age_var = tk.StringVar()

# Dropdown menu for names
name_label = tk.Label(root, text="Select a Name:")
name_label.pack()
name_dropdown = ttk.Combobox(root, textvariable=name_var, values=names)
name_dropdown.pack()

# Dropdown menu for ages
age_label = tk.Label(root, text="Select an Age:")
age_label.pack()
age_dropdown = ttk.Combobox(root, textvariable=age_var, values=ages)
age_dropdown.pack()

# Button to create Person objects
create_button = tk.Button(root, text="Create Person", command=create_person)
create_button.pack()

# Label to display results
result_label = tk.Label(root, text="")
result_label.pack()

# List to store created Person objects
people = []

# Start the Tkinter main loop
root.mainloop()
