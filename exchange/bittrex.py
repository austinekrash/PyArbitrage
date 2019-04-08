import requests
import json


class Bittrex:

    __instance = None
    _table = 'bittrex'


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

    def get_price_pairs(self, pair_symbol):
        try:
            r = requests.get('https://api.bittrex.com/api/v1.1/public/getticker?market='+pair_symbol)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        res = json.loads(r.content).get("result")
        print("[BITTREX] "+pair_symbol+" "+str(res.get("Last")))
        return float(res.get("Last"))