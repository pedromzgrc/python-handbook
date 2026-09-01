# Chapter 8: Fetching Data

# --- Fetching Data with urllib ---
# Theory: urllib is part of the Python standard library, so it works with
# no extra installs. It's more verbose than third-party alternatives but
# useful when you can't (or don't want to) add dependencies.
import urllib.request

response = urllib.request.urlopen("https://jsonplaceholder.typicode.com/todos/1")
print(response.status)
print(response.read().decode())

# --- Fetching Data Using the Requests Package ---
# Theory: requests is a third-party package (install with "pip install
# requests") that offers a much simpler, more readable API than urllib.
import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
print(response.status_code)
print(response.json())

# --- Adding Query Parameters ---
# Theory: query parameters filter or customize a GET request. Pass them as
# a dict via the "params" argument instead of building the URL by hand.
params = {"userId": 1}
response = requests.get("https://jsonplaceholder.typicode.com/todos", params=params)
print(response.url)
print(response.json()[:2])  # show first 2 results

# --- POST Requests ---
# Theory: POST sends data to the server, usually to create something new.
# Pass a dict via the "json" argument to send it as a JSON request body.
new_todo = {"title": "Learn Python", "completed": False}
response = requests.post("https://jsonplaceholder.typicode.com/todos", json=new_todo)
print(response.status_code)
print(response.json())

# --- Handling Errors ---
# Theory: network requests can fail (bad URL, no internet, server error).
# Wrap requests in try/except, and use raise_for_status() to turn a bad
# HTTP status code (like 404 or 500) into an exception you can catch.
try:
    response = requests.get("https://jsonplaceholder.typicode.com/invalid-endpoint")
    response.raise_for_status()
except requests.exceptions.HTTPError as error:
    print("HTTP error occurred:", error)
except requests.exceptions.RequestException as error:
    print("Request failed:", error)
