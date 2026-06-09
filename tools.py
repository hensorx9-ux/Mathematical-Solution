from smolagents import Tool
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class MathVerificationTool(Tool):
    name = "math_verifier"
    description = "Verifies if two mathematical expressions are algebraically equivalent using symbolic logic."
    inputs = {
        "expression_a": {"type": "string", "description": "The target expression (e.g., 'x**2 - 1' or '5*x')"},
        "expression_b": {"type": "string", "description": "The solution to verify (e.g., '(x-1)*(x+1)')"}
    }
    output_type = "string" 

    def forward(self, expression_a: str, expression_b: str) -> str:
        try:
            transformations = standard_transformations + (implicit_multiplication_application,)
            
            expr_a = parse_expr(expression_a, transformations=transformations)
            expr_b = parse_expr(expression_b, transformations=transformations)

            if sp.simplify(expr_a - expr_b) == 0:
                return "VERIFICATION SUCCESSFUL: The expressions are algebraically equivalent."
            else:
                return f"VERIFICATION FAILED: {expression_a} is NOT equivalent to {expression_b}."
        except Exception as e:
            return f"Error in symbolic verification: {str(e)}"