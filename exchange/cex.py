import requests
import json


class Cex:

    __instance = None
    _table = 'cex'


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

    def get_price_pairs(self, pair_symbol):
        try:
            r = requests.get('https://cex.io/api/last_price/'+pair_symbol)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        res = json.loads(r.content)
        print("[CEX] "+res.get("lprice")+" "+res.get("curr1")+" "+res.get("curr2"))
        res.get("lprice")