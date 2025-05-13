import json

from agents_for_all.agent import Agent
from agents_for_all.llms.base_model import Model
from agents_for_all.tools.python import Python


class DummyLLM(Model):
    def __init__(self):
        self.call_count = 0

    def get_response(self, query: str) -> str:
        if self.call_count == 0:
            self.call_count += 1
            return json.dumps(
                [
                    {
                        "type": "tool",
                        "name": "Python",
                        "input_json": {"code": "print(1 + 1)"},
                    }
                ]
            )
        else:
            return "2"  # Final summary


def test_agent_runs_tool():
    llm = DummyLLM()
    python_tool = Python()
    agent = Agent(llm=llm, tools=[python_tool])
    result = agent.do("Add 1 and 1")
    assert "2" == result.output
