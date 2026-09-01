# Chapter 6: Classes and OOP

# --- Defining Classes ---
# Theory: a class is a blueprint for creating objects. __init__ runs when a
# new object is created, setting up its initial attributes. "self" refers
# to the specific object the method is being called on.
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"{self.name} says woof!")

my_dog = Dog("Rex", "Labrador")
my_dog.bark()
print(my_dog.name, my_dog.breed)

# --- Class Methods ---
# Theory: a class method works with the class itself rather than a single
# object. It uses @classmethod and takes "cls" instead of "self". Often
# used as an alternative constructor.
class Dog2:
    species = "Canis familiaris"

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_puppy(cls, name):
        return cls(name)

puppy = Dog2.create_puppy("Buddy")
print(puppy.name, Dog2.species)

# --- Static Methods ---
# Theory: a static method doesn't use "self" or "cls" at all. It's just a
# regular function that logically belongs inside the class, using
# @staticmethod.
class MathHelper:
    @staticmethod
    def add(a, b):
        return a + b

print(MathHelper.add(3, 4))

# --- Inheritance ---
# Theory: a subclass can inherit attributes and methods from a parent
# class, and override or extend them. super() calls the parent's version.
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound")

class Cat(Animal):
    def speak(self):
        super().speak()
        print(f"{self.name} says meow")

my_cat = Cat("Whiskers")
my_cat.speak()
