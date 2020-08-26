# cep_address
Library for consulting addresses with CEP, today in viacep and correios

---
When you enter the CEP you want to search for, by default it will search on viacep, if there is no answer it will try on correios

## Usage

```python
from cep_address import get_address

get_address("55645737")
# {'content': {'state_short': 'PE',
#   'cep': '55645737',
#   'city': 'Gravatá',
#   'ibge': '2606408',
#   'neighborhood': 'Santana',
#   'street': 'Rua Alfredo Roberto Barbosa',
#   'state': 'Pernambuco'},
#  'status': 'OK',
#  'service': 'viacep',
#  'message': ''}}

# if you pass an invalid CEP it will raise an error
get_address("123456789")
# InvalidCepLength: InvalidCepLength has been raised, The cep length must be less then or equal to 8

# it also completes the CEP with leading zeros
get_address("5868-010")
# {'content': {'state_short': 'SP',
#   'cep': '05868010',
#   'city': 'São Paulo',
#   'ibge': '3550308',
#   'neighborhood': 'Conjunto Habitacional Instituto Adventista',
#   'street': 'Rua Cachoeira do Airi',
#   'state': 'São Paulo'},
#  'status': 'OK',
#  'service': 'viacep',
#  'message': ''}


# if you pass an unexisting CEP it will raise an error
get_address("1")
# ServiceError: ServiceError has been raised in correios
# The input CEP is invalid
```
