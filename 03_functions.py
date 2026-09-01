# Chapter 3: Functions

# --- Defining Functions ---
# Theory: def creates a reusable block of code. Call it by name with ().
def greet():
    print("Hello there!")

greet()

# --- Variable Scope ---
# Theory: variables created inside a function are local and don't exist
# outside it. Variables outside functions are global and can be read
# (but not reassigned without the "global" keyword) from inside.
message = "I am global"

def show_scope():
    local_message = "I am local"
    print(message)
    print(local_message)

show_scope()

# --- Arguments ---
# Theory: functions can take positional args, default args, and keyword args.
def introduce(name, greeting="Hi"):
    print(f"{greeting}, {name}!")

introduce("Pedro")
introduce("Pedro", greeting="Hey")
introduce(name="Pedro", greeting="Yo")

# --- Unpacking Operator ---
# Theory: *args collects extra positional arguments into a tuple.
# **kwargs collects extra keyword arguments into a dict.
def show_all(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

show_all(1, 2, 3, name="Pedro", age=30)

numbers = [1, 2, 3]
print(*numbers)  # unpacks list items as separate arguments

# --- Return Values ---
# Theory: return sends a value back to the caller and ends the function.
def add(a, b):
    return a + b

result = add(3, 4)
print(result)

# --- The Main Function ---
# Theory: __name__ == "__main__" checks if this file is being run directly
# (not imported by another file). It's the standard entry point pattern.
def main():
    print("Running as the main program")

if __name__ == "__main__":
    main()

# --- Using Modules and the Python Standard Library ---
# Theory: import brings in code from other files or the standard library
# so you don't have to write everything from scratch.
import math
import random

print(math.sqrt(16))
print(random.randint(1, 10))
