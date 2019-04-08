import requests
import json


class Poloniex:

    __instance = None
    _table = 'poloniex'


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

    def get_price_pairs(self, pair_symbol):
        try:
            r = requests.get('https://poloniex.com/public?command=returnTicker')
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        res = json.loads(r.content)
        for key, value in res.items():
            if(pair_symbol == key):
                symbol = key
                price = value['last']
                break
        print("[POLONIEX] "+price+" "+symbol)
        return float(price)
