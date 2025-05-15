import io
import logging
import sys
from typing import Dict

from agents_for_all.tools.base_tool import Tool


class Python(Tool):
    """
    A tool that can execute python codes.

    Accepts code via input JSON and executes it on the host system using python..
    """

    @property
    def name(self) -> str:
        """
        Python
        """
        return "Python"

    @property
    def description(self) -> str:
        """
        Explains that this tool executes raw Python code.
        """
        return """
            "A tool which can execute python commands commands on the host."
            'Input format: {"code": "<your python command>"}'
            'Use print() to output the result and do not output extraneous details'
            'Do not use input() or anything that will make the execution stop'
        """

    def execute(self, input_json: Dict) -> str:
        """
        Execute the given code string using python.

        Args:
            input_json (Dict): Must contain a "code" key with the python command as value.

        Returns:
            str: The output or error string from the execution.
        """
        command = input_json.get("code").replace("```python\n", "").replace("```\n", "")
        if not command:
            return "Error: 'code' key missing from input_json."

        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        try:
            exec(command)
        except Exception as e:
            logging.info(f"Execution failed with exception: {str(e)}")
            raise e
        finally:
            sys.stdout = old_stdout
        output = buffer.getvalue()
        return output
