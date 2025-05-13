import subprocess
from typing import Dict

from agents_for_all.tools.base_tool import Tool


class Shell(Tool):
    """
    A tool that can execute shell commands.

    Accepts input via input JSON and runs the command on the host shell.

    Example:
        {"command": "ls -l"}

    Note:
        Use with caution. No output redirection or piping is allowed.
    """

    @property
    def name(self) -> str:
        """
        Shell
        """
        return "Shell"

    @property
    def description(self) -> str:
        """
        Executes shell commands on the host system. Input format:
        {"command": "<your shell command>"}
        """
        return (
            'Executes shell commands. Input: {"command": "<your shell command>"}. '
            "Only stdout is returned. Errors are suppressed or printed as text."
        )

    def execute(self, input_json: Dict) -> str:
        command = input_json.get("command")
        if not command:
            return "Error: 'command' key missing from input_json."
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=False
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Shell error: {str(e)}"
