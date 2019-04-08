import requests
import json


class Binance:

    __instance = None
    _table = 'binance'
    _json = None
    _url = 'https://binance.com/api/v3/ticker/price'


    @staticmethod
    def Factory():
        if Binance.__instance == None:
            Binance()
        return Binance.__instance

    def __init__(self):
        if Binance.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Binance.__instance = self
    
    def sync(self):
        try:
            r = requests.get(self._url)
            self._json = r.content
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)


    def get_price_pairs(self, pair_symbol):
        print("prima del for")
        for i in self._json:
            print(i)
            if i['symbol'].lower() == pair_symbol.lower():
                print("[BINANCE] "+i['price']+" "+i['symbol'])
                return float(i['price'])
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        return float(-1)

        
