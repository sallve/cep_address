from typing import Dict, Union
from xml.etree import ElementTree as ET

from requests.exceptions import HTTPError

from cep_address.ufs import UFS
from cep_address.utils import get_service_error_message, requests_retry_session


def parse_address(address_data: Union[Dict, str]) -> Dict:
    if isinstance(address_data, dict):
        return address_data
    for data in ET.fromstring(address_data).iter("return"):
        if data.find("bairro").text:
            return {
                "content": {
                    "neighborhood": data.find("bairro").text,
                    "cep": data.find("cep").text,
                    "city": data.find("cidade").text,
                    "street": data.find("end").text,
                    "state_short": data.find("uf").text,
                    "state": UFS.get(data.find("uf").text),
                },
                "status": "OK",
                "service": "correios",
            }
        else:
            return get_service_error_message(
                service="correios", message="The input CEP is invalid"
            )


def validate_response(response):
    try:
        response.raise_for_status()
    except HTTPError as e:
        if (
            next(ET.fromstring(response.text).iter("faultstring")).text
            == "CEP NAO ENCONTRADO"
        ):
            return get_service_error_message(
                service="correios", message="The input CEP is invalid"
            )
        elif (
            next(ET.fromstring(response.text).iter("faultstring")).text
            == "CEP INVÁLIDO"
        ):
            return get_service_error_message(
                service="correios", message="The input CEP is invalid"
            )
        else:
            raise e
    return response.text


def request(cep: str):
    url = (
        "https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente"
    )
    data = (
        '<?xml version="1.0"?>\n<soapenv:Envelope xmlns:soapenv="http://schemas'
        '.xmlsoap.org/soap/envelope/" xmlns:cli="http://cliente.bean.master.'
        'sigep.bsb.correios.com.br/">\n  <soapenv:Header />\n  <soapenv:Body>\n'
        f"    <cli:consultaCEP>\n      <cep>{cep}</cep>\n    "
        "</cli:consultaCEP>\n  </soapenv:Body>\n</soapenv:Envelope>"
    )
    headers = {"Content-Type": "text/xml;charset=UTF-8", "cache-control": "no-cache"}
    response = requests_retry_session().post(url, data=data, headers=headers)

    return validate_response(response)


def get_address(cep: str) -> None:
    try:
        response = request(cep)
        return parse_address(address_data=response)
    except HTTPError:
        queue.put(
            get_service_error_message(
                service="correios",
                message=(
                    "Sorry, there was an error during the request to the "
                    "service, please try again later"
                ),
            )
        )
    except Exception as e:
        queue.put(e.message)
