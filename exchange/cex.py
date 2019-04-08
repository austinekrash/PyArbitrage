import requests
import json


class Cex:

    __instance = None
    _table = 'cex'
    _json = []
    _url = 'https://cex.io/api/tickers/USD'
    _url_prices = 'https://cex.io/api/last_prices/'

    @staticmethod
    def Factory():
        if Cex.__instance == None:
            Cex()
        return Cex.__instance

    def __init__(self):
        if Cex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Cex.__instance = self            
    
    def sync(self):
            crypto_list = []
            try:
                r = requests.get(self._url)
                crypto_data = json.loads(r.content).get('data')
                for index in range(len(crypto_data)):
                    crypto = crypto_data[index]['pair'].split(':')[0]
                    crypto_list.append(crypto)
                for index in range(len(crypto_list)):
                    r = requests.get(self._url_prices+crypto_list[index])
                    last_prices_market = json.loads(r.content).get('data')
                    for ind in range(len(last_prices_market)):
                        symb1 = last_prices_market[ind]['symbol1']
                        symb2 = last_prices_market[ind]['symbol2']
                        price = last_prices_market[ind]['lprice']
                        info = {'pair' : symb1+'/'+symb2, 'lprice': float(price)}
                        self._json.append(info)
            except (r.status_code != 200):
                raise Exception('Some problems retrieving price: '+r.status_code)
            #print(self._json)

    def get_price_pairs(self, pair_symbol):
        for index in range(len(self._json)):
            if pair_symbol.lower() in self._json[index]['pair'].lower() :
                print("[CEX.IO] "+pair_symbol+" "+str(self._json[index]['lprice']))
                return self._json[index]['lprice']
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1