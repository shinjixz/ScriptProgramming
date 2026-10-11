# my_utils.py - Custom module

def greet(name):
    """Print a greeting message for the given name."""
    print(f"Hello, {name}!")


def is_prime(number):
    """Return True if number is prime, otherwise False."""
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True
