# lab6_1.py - Simple Calculator Functions

def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the result of a minus b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return a divided by b, or an error message if b is zero."""
    if b == 0:
        return "Error: Division by zero"
    return a / b


def power(base, exponent=2):
    """Return base raised to exponent (default exponent is 2)."""
    return base ** exponent


def get_number(prompt):
    """Ask the user for a number until a valid one is entered."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    while True:
        print("\n===== Simple Calculator =====")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Power (leave exponent blank for square)")
        print("0. Exit")
        choice = input("Choose an operation (0-5): ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        if choice not in ("1", "2", "3", "4", "5"):
            print("Invalid choice. Please try again.")
            continue

        x = get_number("Enter first number: ")

        if choice == "5":
            exp_text = input("Enter exponent (press Enter for 2): ").strip()
            if exp_text == "":
                result = power(x)
            else:
                try:
                    result = power(x, float(exp_text))
                except ValueError:
                    print("Invalid exponent.")
                    continue
        else:
            y = get_number("Enter second number: ")
            if choice == "1":
                result = add(x, y)
            elif choice == "2":
                result = subtract(x, y)
            elif choice == "3":
                result = multiply(x, y)
            else:
                result = divide(x, y)

        print("Result:", result)


main()
