# Chapter 5: Advanced Function Concepts

# --- Higher-Order Functions ---
# Theory: a higher-order function either takes another function as an
# argument, returns a function, or both. This lets you customize behavior
# by passing logic around like any other value.
def apply_twice(func, value):
    return func(func(value))

def add_five(x):
    return x + 5

print(apply_twice(add_five, 10))

# --- Lambda Functions ---
# Theory: a lambda is a small, anonymous, one-line function. Useful for
# short throwaway logic, often passed into higher-order functions like
# map(), filter(), or sorted().
square = lambda x: x * x
print(square(4))

numbers = [1, 2, 3, 4, 5]
even_numbers = list(filter(lambda n: n % 2 == 0, numbers))
print(even_numbers)

# --- Decorators ---
# Theory: a decorator is a function that wraps another function to add
# extra behavior before/after it runs, without changing its code.
# The @decorator_name syntax applies the wrapper automatically.
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_call
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Pedro")

# --- Closures ---
# Theory: a closure is a function that "remembers" variables from the
# scope it was created in, even after that outer function has finished
# running.
def make_multiplier(factor):
    def multiplier(number):
        return number * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))
print(triple(5))
