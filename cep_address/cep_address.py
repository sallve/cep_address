from contextlib import contextmanager
from functools import reduce
from importlib import import_module
from multiprocessing import Process, Queue
from multiprocessing.queues import Empty
from re import sub
from typing import Dict, List

from cep_address.utils import get_service_error_message
from cep_address.exceptions import InvalidCepLength, ServiceError, ValidationError

CEP_SIZE = 8


def _fill_left_with_zeros(cep: str) -> str:
    return cep.zfill(CEP_SIZE)


def _validate_input_length(cep: str) -> str:
    if len(cep) <= CEP_SIZE:
        return cep
    raise InvalidCepLength(f"The cep length must be less then or equal to {CEP_SIZE}")


def _remove_special_characters(cep: str) -> str:
    return sub(r"\D+", "", cep)


def _validate_input_type(cep):
    if not isinstance(cep, str) and not isinstance(cep, int):
        raise TypeError("Cep must be a str or an int")
    return str(cep)


def validate_cep(cep: str) -> str:
    try:
        return reduce(
            lambda value, function: function(value),
            (
                _validate_input_type,
                _remove_special_characters,
                _validate_input_length,
                _fill_left_with_zeros,
            ),
            cep,
        )
    except TypeError as e:
        raise e
    except InvalidCepLength as e:
        raise e
    except Exception as e:
        raise ValidationError(
            f"An error occurred during the CEP validation\n{e.message}"
        )


@contextmanager
def _run_jobs(jobs):
    for j in jobs:
        j.start()
    yield
    for p in jobs:
        p.terminate()


def _import_services(services: List) -> List:
    for service in services:
        yield import_module(f"cep_address.services.{service}")


def get_address(cep: str, services: List = ["viacep"]) -> Dict:
    """Returns the address based on the CEP, focusing on the fastest service return.

    Args:
        cep: Código de Endereçamento Postal(zip code)
        services: list of services to be consulted(today we just have viacep and correios)

    TODO: create an abstract base class so that anyone can create a service
    """
    cep = validate_cep(cep)
    jobs = []
    q = Queue()
    for service in _import_services(services):
        jobs.append(Process(target=service.get_address, args=(q, cep)))

    with _run_jobs(jobs):
        try:
            service_response = q.get(timeout=10)
        except Empty:
            service_response = get_service_error_message(
                service="ALL",
                message=(
                    "Sorry, none of the services were able to get the "
                    "address you wanted, try again later"
                ),
            )

    if service_response["status"] == "OK":
        return service_response
    else:
        raise ServiceError(
            service=service_response["service"], message=service_response["message"]
        )
