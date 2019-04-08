import requests
import json


class Binance:

    __instance = None
    _table = 'binance'


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

    def get_price_pairs(self, pair_symbol):
        try:
            r = requests.get('https://binance.com/api/v3/ticker/price?symbol='+pair_symbol)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        res = json.loads(r.content)
        print("[BINANCE] "+res.get("price")+" "+res.get("symbol"))
        return float(res.get("price"))
