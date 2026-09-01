# Chapter 4: Working with Files

# --- Opening and Reading Files ---
# Theory: open(path, mode) returns a file object. mode "r" means read.
# Always close a file when you're done with it (or use a context manager,
# see below) to free up system resources.
file = open("sample.txt", "w")
file.write("Hello, file!\nSecond line.")
file.close()

file = open("sample.txt", "r")
content = file.read()
print(content)
file.close()

# --- Writing to Files ---
# Theory: mode "w" creates the file if it doesn't exist, and overwrites it
# completely if it does.
file = open("sample.txt", "w")
file.write("This replaces the old content.")
file.close()

# --- Appending to Files ---
# Theory: mode "a" adds new content to the end of the file instead of
# overwriting it.
file = open("sample.txt", "a")
file.write("\nThis line was appended.")
file.close()

# --- Working with Paths ---
# Theory: the os.path module helps build and inspect file paths in a way
# that works across different operating systems.
import os

path = os.path.join("data", "sample.txt")
print(path)
print(os.path.exists("sample.txt"))

# --- Pathlib to Read and Write Files ---
# Theory: pathlib.Path is the modern, object-oriented way to work with
# paths and files, replacing a lot of what os.path does.
from pathlib import Path

p = Path("sample.txt")
p.write_text("Written using pathlib.")
print(p.read_text())

# --- Handling File Errors ---
# Theory: trying to open a file that doesn't exist raises FileNotFoundError.
# Wrap file operations in try/except to handle this gracefully.
try:
    missing_file = open("does_not_exist.txt", "r")
except FileNotFoundError:
    print("That file does not exist.")

# --- Context Managers ---
# Theory: "with open(...) as file:" automatically closes the file for you,
# even if an error happens inside the block. This is the recommended way
# to work with files.
with open("sample.txt", "r") as file:
    content = file.read()
    print(content)
# file is automatically closed here

# --- Working with JSON Files ---
# Theory: the json module converts between Python objects (dicts, lists)
# and JSON text, so you can save and load structured data easily.
import json

data = {"name": "Pedro", "age": 30, "skills": ["Python", "SQL"]}

with open("data.json", "w") as file:
    json.dump(data, file)

with open("data.json", "r") as file:
    loaded_data = json.load(file)
    print(loaded_data)
