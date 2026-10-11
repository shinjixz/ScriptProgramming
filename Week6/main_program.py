# main_program.py - Uses the custom module and standard library modules
import my_utils
import math
import random

# Custom module
my_utils.greet("Alice")

for n in (7, 10, 1, 97):
    print(f"is_prime({n}) = {my_utils.is_prime(n)}")

# math module
number = 144
print(f"Square root of {number} = {math.sqrt(number)}")
print(f"Value of pi = {math.pi}")

# random module
print(f"Random number (1-100): {random.randint(1, 100)}")
print(f"Random choice: {random.choice(['apple', 'banana', 'cherry'])}")
