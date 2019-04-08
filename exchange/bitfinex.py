import requests
import json


class Bitfinex:

    __instance = None
    _table = 'bitfinex'
    _json = None
    _url = 'https://api-pub.bitfinex.com/v2/tickers?symbols=ALL'

    @staticmethod
    def Factory():
        if Bitfinex.__instance == None:
            Bitfinex()
        return Bitfinex.__instance

    def __init__(self):
        if Bitfinex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Bitfinex.__instance = self
    
    def sync(self):
        try:
            r = requests.get(self._url)
            self._json = r.content
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)

    def get_price_pairs(self, pair_symbol):
        for index in range(len(self._json)):
            if pair_symbol.lower() in self._json[index][0].lower() :
                print("[BITFINEX] "+pair_symbol+" "+str(self._json[index][7]))
                return float(self._json[index][7])
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1
        