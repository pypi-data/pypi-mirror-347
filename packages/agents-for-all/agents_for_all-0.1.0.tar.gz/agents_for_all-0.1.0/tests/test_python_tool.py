from agents_for_all.tools.python import Python


def test_python_execution():
    tool = Python()
    result = tool.execute({"code": "print(5 * 2)"})
    assert result.strip() == "10"
