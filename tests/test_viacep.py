from multiprocessing import Process, Queue

import pytest

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


# def test_get_address(
#     valid_viacep_response, formatted_valid_cep, valid_viacep_service_return, mocker
# ):
#     q = Queue()
#     p = Process()
#     p.start()
#     mock_request = mocker.patch("cep_address.services.viacep.request")
#     mock_request.json.return_value = valid_viacep_service_return
#     viacep.get_address(queue=q, cep=formatted_valid_cep)
#     response = q.get(timeout=1)
#     breakpoint()
#     p.join()
