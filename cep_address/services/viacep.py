from json import JSONDecodeError
from typing import Dict

from requests.exceptions import HTTPError
from requests.models import Response

from cep_address.ufs import UFS
from cep_address.utils import get_service_error_message, requests_retry_session


def parse_address(cep: str, address_data: Dict) -> Dict:
    if address_data.get("ibge"):
        return {
            "content": {
                "state_short": address_data["uf"],
                "cep": cep,
                "city": address_data["localidade"],
                "ibge": address_data["ibge"],
                "neighborhood": address_data["bairro"],
                "street": address_data["logradouro"],
                "state": UFS.get(address_data["uf"]),
            },
            "status": "OK",
            "service": "viacep",
            "message": "",
        }
    else:
        return get_service_error_message(
            service="viacep", message="The input CEP is invalid"
        )


def request(cep: str) -> Response:
    url_api = f"http://viacep.com.br/ws/{cep}/json"
    response = requests_retry_session().get(url_api)
    response.raise_for_status()
    return response


def get_address(cep: str) -> Dict:
    try:
        response = request(cep)
        return parse_address(cep=cep, address_data=response.json())
    except JSONDecodeError:
        return get_service_error_message(
            service="viacep", message="The input CEP is invalid"
        )
    except HTTPError:
        return get_service_error_message(
            service="viacep",
            message=(
                "Sorry, there was an error during the request to the "
                "service, please try again later"
            ),
        )
    except Exception as e:
        return get_service_error_message(service="viacep", message=e.message)
