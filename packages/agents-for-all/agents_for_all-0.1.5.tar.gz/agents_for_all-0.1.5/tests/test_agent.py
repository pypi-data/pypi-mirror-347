import pytest

from agents_for_all.agent import Agent, AgentResult
from agents_for_all.llms.base_model import Model
from agents_for_all.tools.python import Python


class MockLLM(Model):
    def __init__(self, responses):
        self.responses = responses
        self.index = 0

    def get_response(self, prompt: str) -> str:
        response = self.responses[self.index]
        self.index += 1
        return response


def test_simple_python_tool():
    responses = [
        '[{"type": "tool", "name": "Python", "input_json": {"code": "print(2 + 3)"}}]',
        "5",
    ]
    llm = MockLLM(responses)
    python_tool = Python()
    agent = Agent(llm=llm, tools=[python_tool])
    result = agent.do("Calculate 2 + 3")
    assert isinstance(result, AgentResult)
    assert "5" in result.output
    assert any("Tool `Python` Output: 5" in line for line in result.history)


def test_llm_in_middle_to_format_input():
    # flake8: noqa
    responses = [
        '[{"type": "tool", "name": "Python", "input_json": {"code": "print(2 + 2)"}}, {"type": "llm", "query": "format the above output as valid input"}, {"type": "tool", "name": "Python", "input_json": null}]',
        '{"code": "print(4)"}',
        "4",
    ]
    llm = MockLLM(responses)
    python_tool = Python()
    agent = Agent(llm=llm, tools=[python_tool])
    result = agent.do("Chain two steps to print and reprint 4")
    assert result.output.strip() == "4"
    assert "Tool `Python` Output: 4" in result.history[-1]
