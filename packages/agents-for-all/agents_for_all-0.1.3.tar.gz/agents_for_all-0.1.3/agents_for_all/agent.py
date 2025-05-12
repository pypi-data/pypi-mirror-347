import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List

from agents_for_all.llms.base_model import Model
from agents_for_all.tools.base_tool import Tool

logging.basicConfig(level=logging.WARNING)

DEFAULT_SUBDIVISION_PROMPT = """
You are a task-planning AI. Give a JSON array preferring tools over llm given the following user request:

{action}

And a list of available tools described below:

{tool_descriptions}

Break the task into steps. For each step, specify:
- "type": "tool" or "llm"
- "name": name of the tool (if type is tool)
- "input_json": dictionary input for the tool (if type is tool)
- "query": string to send to LLM (if type is llm)

Respond only with a JSON array like:
[
  {{"type": "tool", "name": "Computer", "input_json": {{"code": "echo hello"}}}},
  {{"type": "llm", "query": "Summarize what was just done."}}
]

Do not respond with anything other than the JSON array. No need for explanation or anything.
Do not explain the steps or say anything in the beginning. No need to tag the json with ```json.
Just give the JSON array as told.
"""

ERROR_CORRECTION_PROMPT = """
Last time, with these steps we got an error.

Steps:
{steps}

{error}
"""


@dataclass
class AgentResult:
    """
    Represents the result of running an Agent's `.do()` method.

    Attributes:
        output (str): The final summary response after executing all steps.
        history (List[str]): Step-by-step log of what happened during execution.
    """

    output: str
    history: List[str]


class Agent:
    """
    Agent class which can 'do' actions using llm and tools.

    Example code:

    .. code-block:: python

        from agents_for_all import Agent
        from agents_for_all.llms.direct import DirectModel
        from agents_for_all.tools.python import Python

        llm = DirectModel(
            api_endpoint="http://127.0.0.1:1234/v1/chat/completions",
            model="deepseek-r1-distill-llama-8b"
        )
        python = Python()

        agent = Agent(llm=llm, tools=[python])
        result = agent.do("Create a file with system date as the filename and txt as extension.")
        print(result.output) # Final output
        print(result.history) # History of steps taken

    """

    def __init__(self, llm: Model, tools: List[Tool], max_retries: int = 10):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_retries = max_retries

    def _force_json_response(self, llm_response: str):
        try:
            return json.loads(llm_response)
        except json.JSONDecodeError:
            # Try to extract JSON if it was wrapped in text
            match = re.search(r"\[.*\]", llm_response, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise

    def _subdivide_task(
        self, action: str, error: str = "", steps: Dict | None = None
    ) -> List[Dict[str, Any]]:
        tool_descriptions = "\n".join(
            [f"- {tool.name}: {tool.description}" for tool in self.tools.values()]
        )
        prompt = DEFAULT_SUBDIVISION_PROMPT.format(
            action=action, tool_descriptions=tool_descriptions, error=error
        )
        prompt += (
            ERROR_CORRECTION_PROMPT.format(steps=steps, error=error) if error else ""
        )
        response = self.llm.get_response(prompt)
        return self._force_json_response(response)

    def do(self, action: str) -> str:
        """
        Do the given action using tools available and the llm specified.

        Args:
            action (str): The action to perform.

        Returns:
            str: The output from doing the action or a brief summary of what happened by performing the action.
        """

        attempt = 0
        steps = []
        error = ""
        while attempt < self.max_retries:
            try:
                steps = self._subdivide_task(action=action, steps=steps, error=error)
                results = []
                history = []

                for idx, step in enumerate(steps):
                    step_type = step.get("type")

                    if step_type == "tool":
                        name = step.get("name")
                        input_json = step.get("input_json")
                        tool = self.tools.get(name)
                        if not tool:
                            message = f"Tool '{name}' not found."
                            logging.error(message)
                            results.append(message)
                            history.append(message)
                            continue

                        logging.info(
                            f"[Step {idx+1}] Tool: {name} | Input: {input_json}"
                        )
                        result = tool.execute(input_json)
                        logging.info(f"[Tool:{name}] Result: {result}")
                        results.append(result)
                        history.append(
                            f"Tool `{name}` executed with input {input_json} produced: {result}"
                        )

                    elif step_type == "llm":
                        llm_query = step.get("query")
                        history_str = "\n".join(history)
                        full_prompt = f"""
Give the answer for the {llm_query} based on the following.

The user asked for the action

{action}

We subdivided the action based to these steps:

{steps}

Here is what has happened so far in the execution:

{history_str}

Use values from history when possible.
"""
                        logging.info(f"[Step {idx+1}] LLM Query: {llm_query}")
                        response = self.llm.get_response(full_prompt.strip())
                        logging.info(f"[LLM] Response: {response}")
                        results.append(response)
                        history.append(f"LLM responded with: {response}")

                    else:
                        msg = f"Unknown step type: {step_type}"
                        logging.error(msg)
                        results.append(msg)
                        history.append(msg)
                history_str = "\n".join(history)
                summary_prompt = f"""
Give the answer without giving the full history. Just answer based on the action in brief.
Give the desired answer only or tell whether the desired outcome happened or not.

The user asked for the action

{action}

We subdivided the action based to these steps:

{steps}

Here is what has happened so far in the execution:

{history_str}

Now, Give the final answer in brief based on the action desired without going into detail of the history.
"""
                final_result = self.llm.get_response(summary_prompt.strip())
                logging.info(f"[Final Summary] {final_result}")
                return AgentResult(output=final_result, history=history)
            except Exception as e:
                attempt += 1
                error = e
                logging.warning(f"Retry {attempt} due to error: {e}")
