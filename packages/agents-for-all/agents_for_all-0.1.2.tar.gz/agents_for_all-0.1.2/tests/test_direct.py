from agents_for_all.llms.direct import Direct


def test_direct_initialization():
    model = Direct(api_endpoint="http://localhost:1234", model="test-model")
    assert model.api_endpoint == "http://localhost:1234"
    assert model.model == "test-model"
