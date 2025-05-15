import io
from typing import Dict

import pandas as pd

from agents_for_all.tools.base_tool import Tool


class DataAnalysis(Tool):
    """
    A tool that runs arbitrary pandas code on a DataFrame created from CSV input.

    Example:
        {
            "csv": "a,b\\n1,2\\n3,4",
            "code": "df['a'].mean()"
        }

    Note:
        Only use safe pandas expressions. This tool does not sandbox or restrict eval().
    """

    @property
    def name(self) -> str:
        """
        DataAnalysis
        """
        return "DataAnalysis"

    @property
    def description(self) -> str:
        """
        Executes pandas code on a DataFrame loaded from CSV.
        The variable `df` is automatically defined as the parsed DataFrame.
        """
        return (
            "Evaluates pandas code on a CSV-derived DataFrame. "
            'Input: {"csv": "a,b\\n1,2\\n3,4", "code": "df[\'a\'].sum()"}. '
            "The code must reference the variable `df`."
        )

    def execute(self, input_json: Dict) -> str:
        csv_data = input_json.get("csv")
        code = input_json.get("code")
        if not csv_data or not code:
            return "Error: 'csv' and 'code' are required."

        try:
            df = pd.read_csv(io.StringIO(csv_data))
            result = eval(code, {"df": df})
            return str(result)
        except Exception as e:
            return f"DataAnalysis error: {str(e)}"
