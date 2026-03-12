import csv

# Define the Person class
class Person:
    def __init__(self, name, email, options):
        self.name = name
        self.email = email
        self.options = options

    def __repr__(self):
        return f"Person(name={self.name}, email={self.email}, options={self.options})"

# List to hold all Person objects
people = []

# Read the records.txt file
with open("records.txt", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        if not row:  # skip empty lines
            continue
        name = row[0]
        email = row[1]
        options = row[2:]
        people.append(Person(name, email, options))

# Print all Person objects
print("Printing all Person objects as stored:")
for person in people:
    print(person)

# Optional: nicer, readable print
print("\nReadable format:")
for person in people:
    print(f"Name: {person.name}")
    print(f"Email: {person.email}")
    print(f"Options: {', '.join(person.options)}")
    print("-" * 40)