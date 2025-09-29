"""
This script demonstrates a method to solve a system of three quadratic equations with three variables (x, y, z).
It uses the SymPy library for symbolic mathematics in Python.

The system of equations is defined as:
1. x^2 + y + z = 5
2. x + y^2 + z = 7
3. x + y + z^2 = 8

The script defines these equations symbolically and solves the system.
"""

# Import the necessary functions from the SymPy library
from sympy import symbols, Eq, solve

# Define the variables we want to solve for
x, y, z = symbols('x y z')

# Define the three quadratic equations
# Equation 1: x^2 + y + z = 5
eq1 = Eq(x**2 + y + z, 5)

# Equation 2: x + y^2 + z = 7
eq2 = Eq(x + y**2 + z, 7)

# Equation 3: x + y + z^2 = 8
eq3 = Eq(x + y + z**2, 8)

# Solve the system of equations for x, y, z
# The result is a list of dictionaries, where each dictionary is a solution set
solutions = solve((eq1, eq2, eq3), (x, y, z))

# Print the resulting solutions
print("Solutions for the system of equations:")
print(solutions)