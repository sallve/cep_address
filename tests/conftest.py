import pytest


@pytest.fixture
def valid_cep():
    return "06340-290"


@pytest.fixture
def formatted_valid_cep():
    return "06340290"


@pytest.fixture
def invalid_cep():
    return "00000-000"


@pytest.fixture
def formatted_invalid_cep():
    return "00000000"


@pytest.fixture
def valid_viacep_response(valid_cep):
    return {
        "cep": valid_cep,
        "logradouro": "Rua Silas Lino Ramos",
        "complemento": "",
        "bairro": "Parque Santa Teresa",
        "localidade": "Carapicuíba",
        "uf": "SP",
        "unidade": "",
        "ibge": "3510609",
        "gia": "2550",
    }


@pytest.fixture
def valid_viacep_service_return(formatted_valid_cep):
    return {
        "content": {
            "state_short": "SP",
            "cep": formatted_valid_cep,
            "city": "Carapicuíba",
            "ibge": "3510609",
            "neighborhood": "Parque Santa Teresa",
            "street": "Rua Silas Lino Ramos",
            "state": "São Paulo",
        },
        "status": "OK",
        "service": "viacep",
        "message": "",
    }
