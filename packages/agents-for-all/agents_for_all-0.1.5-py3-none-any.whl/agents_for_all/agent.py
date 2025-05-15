import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List

from agents_for_all.llms.base_model import Model
from agents_for_all.tools.base_tool import Tool

logging.basicConfig(level=logging.WARNING)

# flake8: noqa
SUBDIVISION_PROMPT = """
<SUBDIVISION_PROMPT>
You are a task-planning AI. Your job is to break down the user's request into a list of structured steps that use tools and LLMs.

User request:
<action>
{action}
</action>

Below is a list of available tools:

<tool_descriptions>
{tool_descriptions}
</tool_descriptions>

Each step must be a dictionary with:
- "type": either "tool" or "llm"
- "name": name of the tool (if type is "tool")
- "input_json": (if type is "tool")
    - A dictionary of inputs, if the input is already available based on the tool's description. Be careful to use the keys in the tool's description.
    - Or null, if the input must be dynamically generated from a previous step. Be sure to say null and not None.
- "query": a string to send to the LLM (if type is "llm")

---

When one tool's output is needed as input for another tool:
- Insert an **LLM step in between** to format the output properly.
- For the dependent tool, set `"input_json": null`. This is the dependent tool which comes after not the one in front.
- In the LLM step, set the `"query"` to explain that it must convert the previous tool's output into a valid JSON input for the next tool, based on that tool's description.

Example LLM query in this case:
"Format the previous tool's output as valid input for Tool B. Tool B expects: {{...input format from Tool B's description...}}. Fill the content verbatim as needed."
Be very careful about the json format that is needed by the tool. Do not include any extra keys than the ones in Tool B's description.
[
  {{"type": "tool", "name": "WebFetcher", "input_json": {{"url": "https://google.com"}}}},
  {{"type": "llm", "query": "Replace the <content> from previous execution and return a json string by filling the content verbatim without code tags and proper escaping: {{"code": "print(len(<content>))"}}."}}
  {{"type": "tool", "name": "Python": null}}
]

Important:
- The LLM must return the exact JSON dictionary needed.
- Use inputs from previous tool verbatim with no changes.
- Do not use variables, placeholders, or explanation.
- Just return the structured JSON to be used as `input_json` for the next tool. Be very careful about the format of the input_json in the tool's description.

---

Respond only with a JSON array like:
[
  {{"type": "tool", "name": "Python", "input_json": {{"code": "print("hello")"}}}},
  {{"type": "llm", "query": "Summarize what was just done."}}
]

Do not return anything else — no markdown, no code tags, no explanations. Only the JSON array.
</SUBDIVISION_PROMPT>
"""

ERROR_CORRECTION_PROMPT = """
<ERROR_CORRECTION_PROMPT>
Last time, with these steps we got an error.

Steps:
<steps>
{steps}
</steps>

Error:
<error>
{error}
</error>
<ERROR_CORRECTION_PROMPT>
"""

# flake8: noqa
LLM_STEP_PROMPT = """
<LLM_STEP_PROMPT>
User asked for this action:
<action>
{action}
</action>

Steps to solve the task:
<steps>
{steps}
</steps>

So far this has happened:
<history>
{history}
</history>

Now answer this query:
<query>
{query}
</query>

If the content from last step is:
<content>
{content}
</content>

If the content is present, use it verbatim in the format required in the query to perform the action required using the next tool's input_json format.
</LLM_STEP_PROMPT>
"""

SUMMARY_PROMPT = """
Give the answer in brief, based on the action and what happened. Avoid repeating full history.

Action:
<action>
{action}
</action>

History:
<history>
{history}
</history>
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
            model="deepseek-r1-distill-qwen-14b"
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

    def _force_json_array(self, llm_response: str):
        llm_response = llm_response.replace("```json\n", "").replace("```", "").strip()
        try:
            return json.loads(llm_response)
        except Exception:
            match = re.search(r"\[.*\]", llm_response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except Exception:
                    raise ValueError(f"Invalid json: {llm_response}")

    def _force_json(self, llm_response: str):
        llm_response = llm_response.replace("```json\n", "").replace("```", "").strip()
        try:
            return json.loads(llm_response)
        except Exception:
            match = re.search(r"\{.*\}", llm_response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except Exception:
                    raise ValueError(f"Invalid json: {llm_response}")

    def _subdivide_task(
        self, action: str, error: str = "", steps: Dict | None = None
    ) -> List[Dict[str, Any]]:
        tool_descriptions = "\n\n\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools.values()]
        )
        subdivision_prompt = SUBDIVISION_PROMPT.format(
            action=action,
            tool_descriptions=tool_descriptions,
        )
        subdivision_prompt += (
            ERROR_CORRECTION_PROMPT.format(steps=steps, error=error) if error else ""
        )
        response = self.llm.get_response(subdivision_prompt)
        return self._force_json_array(response)

    def do(self, action: str) -> AgentResult:
        """
        Do the given action using tools available and the llm specified.

        Args:
            action (str): The action to perform.

        Returns:
            AgentResult: Final answer and execution trace.
        """

        attempt = 0
        steps = []
        error = ""

        while attempt < self.max_retries:
            try:
                steps = self._subdivide_task(action=action, steps=steps, error=error)
                logging.info(f"Steps: {steps}")
                history = []
                content = ""  # output of previous step

                for idx, step in enumerate(steps):
                    step_type = step.get("type")

                    if step_type == "tool":
                        name = step.get("name")
                        input_json = step.get("input_json") or self._force_json(content)
                        tool = self.tools.get(name)

                        if not tool:
                            msg = f"[{idx+1}] Tool '{name}' not found."
                            logging.error(msg)
                            history.append(msg)
                            raise ValueError(msg)

                        logging.info(
                            f"[Step {idx+1}] Tool `{name}` Input: {input_json}"
                        )
                        result = tool.execute(input_json)
                        logging.info(f"[Tool:{name}] Output: {result}")
                        history.append(f"[{idx+1}] Tool `{name}` Output: {result}")
                        content = result

                    elif step_type == "llm":
                        query = step.get("query")
                        prompt = LLM_STEP_PROMPT.format(
                            action=action,
                            steps=json.dumps(steps, indent=2),
                            history="\n".join(history),
                            query=query,
                            content=content,
                        )
                        logging.info(f"[Step {idx+1}] LLM Prompt: {prompt}")
                        response = self.llm.get_response(prompt.strip())
                        logging.info(f"[LLM] Response: {response}")
                        history.append(f"[{idx+1}] LLM Output: {response}")
                        content = response

                    else:
                        msg = f"[{idx+1}] Unknown step type: '{step_type}'"
                        logging.error(msg)
                        history.append(msg)
                        raise ValueError(msg)

                final_prompt = SUMMARY_PROMPT.format(
                    action=action, history="\n".join(history)
                )
                final_result = self.llm.get_response(final_prompt.strip())
                logging.info(f"[Final Summary] {final_result}")

                return AgentResult(output=final_result, history=history)

            except Exception as e:
                attempt += 1
                error = str(e)
                logging.warning(f"Retry {attempt} due to error: {e}")
