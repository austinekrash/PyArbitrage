import requests
import json


class Bitfinex:

    __instance = None
    _table = 'bitfinex'


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
        
    def get_price_pairs(self, pair_symbol):
        try:
            r = requests.get('https://api-pub.bitfinex.com/v2/ticker/'+pair_symbol)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        res = json.loads(r.content)
        print("[BITFINEX] "+pair_symbol+" "+str(res[6]))
        return float(res[6])
        