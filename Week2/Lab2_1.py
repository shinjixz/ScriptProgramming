num = int(input("Enter a number: "))
if num > 0:
    result ="The number is positive."
elif num < 0:
    result = "The number is negative."
else:
    result = "The number is zero."

if num % 2 == 0:
    even_odd = "even"
else:
    even_odd = "odd"

print(f"{result} It is an {even_odd} number.")