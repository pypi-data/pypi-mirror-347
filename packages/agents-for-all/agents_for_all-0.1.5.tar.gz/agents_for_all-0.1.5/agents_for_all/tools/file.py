from typing import Dict

from agents_for_all.tools.base_tool import Tool


class File(Tool):
    """
    A tool that can perform basic file operations: read and write.

    Accepts input via input JSON to read from or write to a file.

    """

    @property
    def name(self) -> str:
        """
        File
        """
        return "File"

    @property
    def description(self) -> str:
        """
        Reads from or writes to files.
        """
        return (
            "Performs file operations. Input: "
            '{"operation": "read"|"write", "path": "filename", "content": "..."}.'
            " For 'write', 'content' must be provided."
        )

    def execute(self, input_json: Dict) -> str:
        operation = input_json.get("operation")
        path = input_json.get("path")
        if not operation or not path:
            return "Error: 'operation' and 'path' required."

        try:
            if operation == "read":
                with open(path, "r") as f:
                    return f.read()
            elif operation == "write":
                content = input_json.get("content", "")
                with open(path, "w") as f:
                    f.write(content)
                return f"Wrote to {path}"
            else:
                return "Unsupported operation"
        except Exception as e:
            return f"File error: {str(e)}"
