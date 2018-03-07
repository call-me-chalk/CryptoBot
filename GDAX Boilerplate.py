#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 00:55:02 2018

@author: laisy
"""

import requests
import base64, hashlib, hmac, time
from requests.auth import AuthBase
import pandas as pd
# sandbox api base
sandbox_api_base = 'https://api-public.sandbox.gdax.com'
my_api_key = ''
passphrase = ''
secret_key = ''
historicCsvPath = ''
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

def coin_csv_create(coin, granularity):
#coin value must be 'LTC' or 'BTC'
#The granularity must be one of the following values: {60, 300, 900, 3600, 21600, 86400}. 
    if coin not in ('LTC', 'BTC'):
        return(print('Please use LTC or BTC for your coin.'))
    elif granularity not in ('60', '300', '900', '3600', '21600', '86400'):
        return(print('Please use 60, 300, 900, 3600, 21600, or 86400 for your granularity.'))
    historic_endpoint = '/products/{0}-USD/candles'.format('LTC')
    historic_json = { 'start' : '2018-02-23T00:00:00-05:00', 'end' : '2018-02-24T00:00:00-05:00', 'granularity' : granularity}

    auth = CoinbaseExchangeAuth(my_api_key, secret_key, passphrase)

    response_historic_data = requests.get(api_url + historic_endpoint,
                                          json = historic_json,
                                          auth=auth)
#    print(response_historic_data.json())
    historicData = pd.DataFrame(response_historic_data.json())
    historicData.columns = ['Time', 'Low', 'High', 'Open', 'Close', 'Volume']
    historicData.to_csv(historicCsvPath)
    pass
    
if __name__ == '__main__':
    coin_csv_create('LTC', '3600')
#put code that you want to run after this if statement.
