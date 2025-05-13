from .solver import solve_quadratic
import sys

class CallableSolver:
    def __call__(self, a, b, c):
        return solve_quadratic(a, b, c)

sys.modules[__name__] = CallableSolver()