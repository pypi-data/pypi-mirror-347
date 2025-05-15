import platform
import subprocess
from typing import Dict

from agents_for_all.tools.base_tool import Tool


class Shell(Tool):
    """
    A tool that can execute shell commands.

    Accepts input via input JSON and runs the command on the host shell.
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
        """
        return (
            """
            Executes shell commands. Input: {"command": "<your shell command>"}}.
            Only stdout is returned. Errors are suppressed or printed as text.
            Base the command on the Platform i.e. use cmd or powershell for windows, bash for linux.
            The platform is: """
            + platform.system()
        )

    def execute(self, input_json: Dict) -> str:
        command = input_json.get("command")
        if not command:
            raise ValueError("Error: 'command' key missing from input_json.")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )
            return result.stdout.strip()
        except Exception as e:
            raise ValueError(f"Shell error: {str(e)}")
