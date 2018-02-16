import pandas as pd
import time
import requests
import json
import matplotlib.pyplot as plt


#bit_req = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()
#eth_req = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/').json()
#ltc_req = requests.get('https://api.coinmarketcap.com/v1/ticker/litecoin/').json()


run = True
count = 0

prices = pd.DataFrame(columns=['Bitcoin', 'Ethereum', 'Litecoin'])

while run:
    bit_req = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()
    eth_req = requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum/').json()
    ltc_req = requests.get('https://api.coinmarketcap.com/v1/ticker/litecoin/').json()
    print(float(bit_req[0]['price_usd']), float(eth_req[0]['price_usd']), float(ltc_req[0]['price_usd']))
    print(prices)
    print('------')
    
    prices = prices.append({'Bitcoin' : float(bit_req[0]['price_usd']),
                            'Ethereum' : float(eth_req[0]['price_usd']), 
                            'Litecoin' :float(ltc_req[0]['price_usd'])}, ignore_index = True)
#    prices = prices.reset_index(drop=True)
    
    time.sleep(10)
    
    if count > 15:
        print(prices)
        plt.plot(prices.index.values, prices['Bitcoin'])
        plt.show()
        plt.plot(prices.index.values, prices['Ethereum'])
        plt.show()
        plt.plot(prices.index.values, prices['Litecoin'])
        plt.show()
        
        run = False
    
    count += 1
 
