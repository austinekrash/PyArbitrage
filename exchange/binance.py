import requests
import json


class Binance:

    __instance = None
    _table = 'binance'
    _json = None
    _url = 'https://binance.com/api/v3/ticker/price'
    _apiKey = 'WXYox2eh9V8fUiLvjdW9f8xkh3q30EpzxGaeLQvxMZ0TTUyDSaIJliEmAXr2NtYN'
    _secretKey = 'qbXdJU82w1QKpjHe6OFRMdJMxbZgQuHigLRzssDqf3TCpEaxyAaHyrGolDQzbrbD'#non so se serve la secret key

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
            self._json = json.loads(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
    

    def get_price_pairs(self, pair_symbol):
        for index in range(len(self._json)):
            if self._json[index]['symbol'].lower() == pair_symbol.lower():
                #print("[BINANCE] "+self._json[index]['price']+" "+self._json[index]['symbol'])
                return float(self._json[index]['price'])
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        return float(-1)

        
