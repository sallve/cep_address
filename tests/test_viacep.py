import vcr

from cep_address.services import viacep


def test_parse_address_valid_cep(
    valid_viacep_response, formatted_valid_cep, valid_viacep_service_return
):
    assert (
        viacep.parse_address(
            cep=formatted_valid_cep, address_data=valid_viacep_response
        )
        == valid_viacep_service_return
    )


def test_parse_address_invalid_cep(invalid_cep, formatted_invalid_cep):
    viacep_address = {
        "cep": invalid_cep,
        "logradouro": "",
        "complemento": "",
        "bairro": "",
        "localidade": "",
        "uf": "",
        "unidade": "",
        "ibge": "",
        "gia": "",
    }
    response = {
        "message": "The input CEP is invalid",
        "service": "viacep",
        "status": "ERROR",
    }
    assert (
        viacep.parse_address(cep=formatted_invalid_cep, address_data=viacep_address)
        == response
    )


@vcr.use_cassette('tests/fixtures/vcr_cassettes/viacep_valid_cep.yml')
def test_request_valid_cep(formatted_valid_cep, valid_viacep_response):
    response = viacep.request(formatted_valid_cep)
    assert response.status_code == 200
    assert response.json() == valid_viacep_response


@vcr.use_cassette('tests/fixtures/vcr_cassettes/viacep_invalid_cep.yml')
def test_request_invalid_cep(invalid_cep, invalid_viacep_response):
    response = viacep.request(invalid_cep)
    assert response.status_code == 200
    assert response.json() == invalid_viacep_response
