import requests
from random import randint
from django.conf import settings
from rest_framework import status

def get_currency_rate(base, opposite):
    params = {
        'from': opposite,
        'to': base,        
        'quantity': 1,
        'api_key': 'key'
    }
    #example: https://forex.1forge.com/1.0.3/convert?from=EUR&to=USD&quantity=1&api_key=key
    result = requests.get('https://forex.1forge.com/1.0.3/convert?', params=params)
    if result.status_code == status.HTTP_200_OK:        
        return result.json().get('value')
    return 0

def get_random_id():
    return randint(10000000, 99999999)
