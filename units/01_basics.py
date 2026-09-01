# Chapter 1: Python Basics

# --- Strings ---
# Theory: text is stored using str, written with single or double quotes.
first_name = "Pedro"
last_name = 'Garcia'
print(first_name, last_name)
print(first_name + " " + last_name)

# --- Numbers and Comments ---
# Theory: int and float store whole and decimal numbers. Lines starting
# with # are comments and are ignored when the code runs.
age = 30
price = 19.99
print(age, price)

# --- Lists ---
# Theory: a list is an ordered, changeable collection of items.
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
print(fruits)

# --- Tuples ---
# Theory: a tuple is an ordered collection like a list, but it cannot be
# changed after it's created.
coordinates = (10, 20)
print(coordinates)

# --- Joining ---
# Theory: str.join() combines a list of strings into one string, using
# the string it's called on as the separator.
words = ["Python", "is", "fun"]
sentence = " ".join(words)
print(sentence)

# --- Slicing ---
# Theory: slicing with [start:stop] grabs a range of items from a
# sequence. Leaving start or stop empty means "from the beginning" or
# "to the end".
numbers = [0, 1, 2, 3, 4, 5]
print(numbers[1:4])
print(numbers[:3])
print(numbers[-2:])

# --- Dicts ---
# Theory: a dict stores key-value pairs, letting you look up a value by
# its key instead of by position. Accessing a missing key with [] raises
# a KeyError, so use the "in" operator or .get() to check safely instead.
person = {"name": "Pedro", "age": 30}
print(person["name"])
person["city"] = "Lisbon"
print(person)

if "email" not in person:
    print("email is not set")

email = person.get("email", "no email provided")
print(email)

# --- Booleans ---
# Theory: bool values are either True or False, often used to represent
# yes/no states or the result of a comparison.
is_active = True
is_admin = False
print(is_active, is_admin)

# --- Sets ---
# Theory: a set is an unordered collection that automatically removes
# duplicate values.
unique_numbers = {1, 2, 2, 3, 3, 3}
print(unique_numbers)

# --- Formatted Strings ---
# Theory: an f-string (prefixed with f) lets you embed variables and
# expressions directly inside a string using curly braces.
name = "Pedro"
score = 95
print(f"{name} scored {score} points")

# --- User Input ---
# Theory: input() pauses the program, shows a prompt, and returns
# whatever the user types as a string.
user_name = input("What is your name? ")
print(f"Hello, {user_name}!")
