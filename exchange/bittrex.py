import requests
import json


class Bittrex:

    __instance = None
    _table = 'bittrex'
    _json = None
    _url = 'https://api.bittrex.com/api/v1.1'
    _apiKey = 'd94bf4036b9841729f2d5100ee9132a4'
    _secretKey = '672e4f9fea3b4628b1bf5617fbdb22be'#non so se serve la secret key

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
        self._url = self._url + '/public/getmarketsummaries'
        try:
            r = requests.get(self._url)
            self._json = json.loads(r.content).get('result')
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)

    def get_price_pairs(self, pair_symbol):
        for index in range(len(self._json)):
            if pair_symbol.lower() in self._json[index]['MarketName'].lower():
                #print("[BITTREX] "+self._json[index]['MarketName']+" "+str(self._json[index]['Last']))
                return float(self._json[index]['Last'])
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1

    def getDepositAddress(self, symbol):
        self._url = self._url + '/account/getdepositaddress?apikey=' + self._apiKey + '&currency=' + symbol
        try:
            r = requests.get(self._url).json()
            self._json = json.loads(r.content).get('result')
            for index in range(len(self._json)):
                print(self._json[index])
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)