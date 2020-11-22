from typing import Dict, Union
from xml.etree import ElementTree as ET

from requests.models import Response
from requests.exceptions import HTTPError

from cep_address.ufs import UFS
from cep_address.utils import get_service_error_message, requests_retry_session


def get_parsed_address(address_data: ET.Element) -> Dict:
    return {
        "content": {
            "neighborhood": address_data.find("bairro").text,
            "cep": address_data.find("cep").text,
            "city": address_data.find("cidade").text,
            "street": address_data.find("end").text,
            "state_short": address_data.find("uf").text,
            "state": UFS.get(address_data.find("uf").text),
        },
        "status": "OK",
        "service": "correios",
    }


def parse_address(address_data: Union[Dict, str]) -> Dict:
    if isinstance(address_data, dict):
        return address_data

    for data in ET.fromstring(address_data).iter("return"):
        if data.find("bairro").text:
            return get_parsed_address(address_data=data)
        else:
            return get_service_error_message(
                service="correios", message="The input CEP is invalid"
            )
    else:
        return get_service_error_message(
            service="correios", message="The input CEP is invalid"
        )


def validate_response(response: Response) -> Union[Dict, str]:
    try:
        response.raise_for_status()
    except HTTPError as e:
        cep_message = next(ET.fromstring(response.text).iter("faultstring")).text
        if cep_message == "CEP NAO ENCONTRADO":
            return get_service_error_message(
                service="correios", message="The input CEP was not found"
            )
        elif cep_message == "CEP INVÁLIDO":
            return get_service_error_message(
                service="correios", message="The input CEP is invalid"
            )
        else:
            raise e
    return response.text


def request(cep: str) -> Union[Dict, str]:
    url = (
        "https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente"
    )
    data = (
        '<?xml version="1.0"?>\n<soapenv:Envelope xmlns:soapenv="http://schemas'
        '.xmlsoap.org/soap/envelope/" xmlns:cli="http://cliente.bean.master.'
        'sigep.bsb.correios.com.br/">\n  <soapenv:Header />\n  <soapenv:Body>\n'
        f'    <cli:consultaCEP>\n      <cep>{cep}</cep>\n    '
        '</cli:consultaCEP>\n  </soapenv:Body>\n</soapenv:Envelope>'
    )
    headers = {"Content-Type": "text/xml;charset=UTF-8", "cache-control": "no-cache"}
    response = requests_retry_session().post(url, data=data, headers=headers)

    return validate_response(response)


def get_address(cep: str) -> Dict:
    try:
        response = request(cep)
        return parse_address(address_data=response)
    except HTTPError:
        return get_service_error_message(
            service="correios",
            message=(
                "Sorry, there was an error during the request to the "
                "service, please try again later"
            ),
        )
    except Exception as e:
        return get_service_error_message(service="correios", message=f"{e.__class__.__name__}: {str(e)}")
