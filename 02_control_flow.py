# Chapter 2: Control Flow

# --- Conditional Statements ---
# Theory: if / elif / else let your program choose a path based on a condition.
# Only the first True branch runs.
age = 18
if age < 13:
    print("child")
elif age < 18:
    print("teenager")
else:
    print("adult")

# --- Conditional Assignments ---
# Theory: also called a ternary operator, it assigns a value based on a
# condition in a single line: value_if_true if condition else value_if_false
age = 16
status = "adult" if age >= 18 else "minor"
print(status)

# --- While Loops ---
# Theory: a while loop repeats as long as its condition stays True.
# Make sure something inside the loop eventually makes the condition False.
count = 0
while count < 3:
    print("count is", count)
    count += 1

# --- Break and Continue ---
# Theory: break exits the loop immediately. continue skips to the next
# iteration without running the rest of the loop body.
number = 0
while number < 10:
    number += 1
    if number == 5:
        continue  # skip printing 5
    if number == 8:
        break  # stop the loop entirely
    print("number is", number)

# --- For Loops ---
# Theory: a for loop iterates over items in a sequence (list, string, etc.)
for fruit in ["apple", "banana", "cherry"]:
    print(fruit)

# --- Ranges with Loops ---
# Theory: range(start, stop, step) generates a sequence of numbers,
# commonly used to control how many times a for loop runs.
for i in range(2, 10, 2):
    print("even number:", i)

# --- Match Statements ---
# Theory: match/case compares a value against several patterns, similar to
# switch statements in other languages.
day = "Sat"
match day:
    case "Sat" | "Sun":
        print("weekend")
    case "Mon":
        print("start of the week")
    case _:
        print("weekday")

# --- Error Handling ---
# Theory: try/except catches errors so the program doesn't crash. else runs
# if no error happened, and finally always runs at the end.
try:
    result = 10 / 0
except ZeroDivisionError:
    print("cannot divide by zero")
else:
    print("division succeeded:", result)
finally:
    print("done trying to divide")
