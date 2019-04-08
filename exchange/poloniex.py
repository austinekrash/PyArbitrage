import requests
import json


class Poloniex:

    __instance = None
    _table = 'poloniex'
    _json = None
    _url = 'https://poloniex.com/public?command=returnTicker'

    @staticmethod
    def Factory():
        if Poloniex.__instance == None:
            Poloniex()
        return Poloniex.__instance

    def __init__(self):
        if Poloniex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Poloniex.__instance = self       

    def sync(self):
        try:
            r = requests.get(self._url)
            self._json = json.loads(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)  

    def get_price_pairs(self, pair_symbol):
        for key, value in self._json.items():
            if(pair_symbol.lower() == key.lower()):
                symbol = key
                price = value['last']
                print("[POLONIEX] "+price+" "+symbol)
                return float(price)
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1
        