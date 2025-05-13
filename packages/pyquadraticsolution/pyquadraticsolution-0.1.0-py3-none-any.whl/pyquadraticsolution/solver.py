import math

def solve_quadratic(a, b, c):
    if a == 0:
        return "This is not a quadratic equation. It's a linear equation."

    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return f"The solutions are real and distinct: x1 = {x1}, x2 = {x2}. \nReason: Discriminant is positive, which indicates two real roots."

    elif discriminant == 0:
        x = -b / (2 * a)
        return f"The solution is real and repeated: x = {x}. \nReason: Discriminant is zero, indicating a repeated real root."

    else:
        real_part = -b / (2 * a)
        imaginary_part = math.sqrt(-discriminant) / (2 * a)
        return f"The solutions are complex: x1 = {real_part} + {imaginary_part}i, x2 = {real_part} - {imaginary_part}i. \nReason: Discriminant is negative, indicating complex roots."