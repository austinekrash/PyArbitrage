import requests
import json
import time
import hmac
import hashlib
import sys

class Bittrex:

    __instance = None
    _table = 'bittrex'
    _json = None
    _url = 'https://api.bittrex.com/api/v1.1'
    _url_account = 'https://api.bittrex.com/api/v1.1/account/'
    _url_market = 'https://api.bittrex.com/api/v1.1/market/'
    
    _apiKey = 'd94bf4036b9841729f2d5100ee9132a4'
    _secretKey = bytearray('672e4f9fea3b4628b1bf5617fbdb22be', "utf-8")#non so se serve la secret key

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

    @staticmethod
    def get_nonce():
        return str(int(time.time()))
    
    def costum_print(self, text):
        print('['+self.__class__.__name__.upper()+'] '+str(text))


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
                #self.costum_print("[BITTREX] "+self._json[index]['MarketName']+" "+str(self._json[index]['Last']))
                return float(self._json[index]['Last'])
        self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
        sys.exit(1)

    def get_deposit_address(self, symbol):
        auth = self._url_account+'getdepositaddress?apikey='+self._apiKey+'&currency='+symbol+'&nonce='+self.get_nonce()
        signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
        try:
            r = requests.get(auth, headers=headers)
            res = json.loads(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        if( True is json.loads(r.content).get('success')):
            self.costum_print(res.get('result').get('Address'))
            return res.get('result').get('Address')
        else:
            self.costum_print('[BITTREX] some problems')
            sys.exit(1)


    def get_balance(self, symbol):
        #con getbalances ottienei i balance ed anche i deposit addreesssssssssssss di tutte
        #dice anceh quando vailable e pending!!!!!!!!!!!!!!!!!
        auth = self._url_account+'getbalance?apikey='+self._apiKey+'&currency='+symbol+'&nonce='+self.get_nonce()
        signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
        try:
            r = requests.get(auth, headers=headers)
            res = json.loads(r.content)
            self.costum_print(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        if( True is json.loads(r.content).get('success')):
            self.costum_print(res.get('result').get('Balance'))
            return res.get('result').get('Balance')
        else:
            self.costum_print('[BITTREX] some problems')
            sys.exit(1)

    def get_balances(self, symbol):
        auth = self._url_account+'getbalances?apikey='+self._apiKey+'&currency='+symbol+'&nonce='+self.get_nonce()
        signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
        try:
            r = requests.get(auth, headers=headers)
            res = json.loads(r.content)
            self.costum_print(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        if( True is res.get('success')):
            self.costum_print(res.get('result'))
            return res.get('result')
        else:
            self.costum_print('[BITTREX] some problems')
            sys.exit(1)


    #paymentid CryptoNotes/BitShareX/Nxt/XRP
    def withdraw(self, symbol, quantity, to_address, paymentid = None):
        if(paymentid is None):
            auth = self._url_account+'withdraw?apikey='+self._apiKey+'&currency='+symbol+'&quantity='+quantity+'&address='+to_address+'&nonce='+self.get_nonce()
        else:
            auth = self._url_account+'withdraw?apikey='+self._apiKey+'&currency='+symbol+'&quantity='+quantity+'&address='+to_address+'&paymentid='+paymentid+'&nonce='+self.get_nonce()
        signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
        try:
            r = requests.get(auth, headers=headers)
            res = json.loads(r.content)
            self.costum_print(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        if( True is res.get('success')):
            self.costum_print(res.get('result'))
            return res.get('result')
        else:
            self.costum_print('[BITTREX] some problems')
            sys.exit(1)

    def buy_limit(self, market, quantitiy, rate):
        auth = self._url_account+'buylimit?apikey='+self._apiKey+'&market='+market+'&quantity='+quantitiy+'&rate='+rate+'&nonce='+self.get_nonce()
        signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
        try:
            r = requests.get(auth, headers=headers)
            res = json.loads(r.content)
            self.costum_print(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        if( True is res.get('success')): #occhio a questo controllo perchè bittrex restituisce 'true' minuscolo
            self.costum_print(res.get('result'))
            return res.get('result')
        else:
            self.costum_print('[BITTREX] some problems')
            sys.exit(1)

    def sell_limit(self, market, quantitiy, rate):
        auth = self._url_account+'selllimit?apikey='+self._apiKey+'&market='+market+'&quantity='+quantitiy+'&rate='+rate+'&nonce='+self.get_nonce()
        signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
        try:
            r = requests.get(auth, headers=headers)
            res = json.loads(r.content)
            self.costum_print(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        if( True is res.get('success')): #occhio a questo controllo perchè bittrex restituisce 'true' minuscolo
            self.costum_print(res.get('result'))
            return res.get('result')
        else:
            self.costum_print('[BITTREX] some problems')
            sys.exit(1)

    #LA CANCEL ORDER?