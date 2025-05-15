from typing import Dict

import sympy

from agents_for_all.tools.base_tool import Tool


class Math(Tool):
    """
    A tool to evaluate mathematical expressions safely using sympy.

    Accepts an expression string and optional variables to substitute.

    """

    @property
    def name(self) -> str:
        """
        Math
        """
        return "Math"

    @property
    def description(self) -> str:
        """
        Evaluates symbolic math expressions using sympy.
        Variables are substituted automatically.
        """
        return (
            'Evaluates math expressions using sympy. Input: {"expr": "2*x + 1", "x": 5}. '
            "Returns numeric result using variable substitution."
        )

    def execute(self, input_json: Dict) -> str:
        expr_str = input_json.get("expr")
        if not expr_str:
            return "Error: 'expr' key missing"
        try:
            expr = sympy.sympify(expr_str)
            subs = {k: v for k, v in input_json.items() if k != "expr"}
            return str(expr.evalf(subs=subs))
        except Exception as e:
            return f"Math error: {str(e)}"
