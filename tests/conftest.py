import pytest


@pytest.fixture
def valid_cep():
    return "55645-737"


@pytest.fixture
def formatted_valid_cep():
    return "55645737"


@pytest.fixture
def invalid_cep():
    return "00000-000"


@pytest.fixture
def formatted_invalid_cep():
    return "00000000"


@pytest.fixture
def invalid_viacep_response():
    return {"erro": True}


@pytest.fixture
def valid_viacep_response(valid_cep):
    return {
        "cep": valid_cep,
        "logradouro": "Rua Alfredo Roberto Barbosa",
        "complemento": "",
        "bairro": "Santana",
        "localidade": "Gravatá",
        "uf": "PE",
        "ibge": "2606408",
        "gia": "",
        "ddd": "81"
    }


@pytest.fixture
def valid_viacep_service_return(formatted_valid_cep):
    return {
        "content": {
            "state_short": "PE",
            "cep": formatted_valid_cep,
            "city": "Gravatá",
            "ibge": "2606408",
            "neighborhood": "Santana",
            "street": "Rua Alfredo Roberto Barbosa",
            "state": "Pernambuco",
        },
        "status": "OK",
        "service": "viacep",
        "message": "",
    }
