#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 00:55:02 2018

@author: laisy
"""

import requests
import base64, hashlib, hmac, time
from requests.auth import AuthBase
# sandbox api base
sandbox_api_base = 'https://api-public.sandbox.gdax.com'
my_api_key = 
passphrase = 
secret_key = 
#insert values here before running code

def products():
    response_products = requests.get(sandbox_api_base + '/products')
    
    if response_products.status_code is not 200:
        raise Exception('Invalid request {0}'.format(response_products.status_code))
    
    return response_products.json()
    
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, my_api_key, secret_key, passphrase):
        self.my_api_key = my_api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.my_api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return(request)

api_url = 'https://api.gdax.com/'
ltc_historic_endpoint = '/products/LTC-USD/candles'
ltc_historic_json = { 'start' : '2018-02-23T00:00:00-05:00', 'end' : '2018-02-24T00:00:00-05:00', 'granularity' : '900'}

auth = CoinbaseExchangeAuth(my_api_key, secret_key, passphrase)

response_historic_data = requests.get(api_url + ltc_historic_endpoint,
                                     json = ltc_historic_json,
                                     auth=auth)
print(response_historic_data.json())
