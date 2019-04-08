import requests
import json


class Bittrex:

    __instance = None
    _table = 'bittrex'
    _json = None
    _url = 'https://api.bittrex.com/api/v1.1/public/getmarketsummaries'


    @staticmethod
    def Factory():
        if Bittrex.__instance == None:
            Bittrex()
        return Bittrex.__instance

    def __init__(self):
        if Bittrex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Bittrex.__instance = self

    def sync(self):
        try:
            r = requests.get(self._url)
            self._json = r.content
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)

    def get_price_pairs(self, pair_symbol):
        for index in range(len(self._json)):
            if pair_symbol.lower() in self._json[index]['MarketName'].lower():
                print("[BITTREX] "+self._json[index]['MarketName']+" "+self._json[index]['Last'])
                return float(self._json[index]['Last'])
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1