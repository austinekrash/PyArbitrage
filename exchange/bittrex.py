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
    
    @staticmethod
    def Factory(apiKey, secretKey):
        if Bittrex.__instance == None:
            Bittrex(apiKey, secretKey)
        return Bittrex.__instance

    def __init__(self, apiKey, secretKey):
        if Bittrex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Bittrex.__instance = self
            _apiKey = apiKey
            _secretKey = bytearray(secretKey, "utf-8")
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
            self.costum_print(res)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        if( True is json.loads(r.content).get('success')):
            self.costum_print(res.get('result').get('Address'))
            return res.get('result').get('Address')
        else:
            if(res.get('messagge') == 'CURRENCY_OFFLINE'):
                return -1
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
            self.costum_print(' some problems')
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
            self.costum_print('some problems')
            sys.exit(1)

    def get_balances(self):
        auth = self._url_account+'getbalances?apikey='+self._apiKey+'&nonce='+self.get_nonce()
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
            self.costum_print(' some problems')
            sys.exit(1)



    def buy_limitR(self, market, quantitiy, rate, price = None):
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
            self.costum_print(' some problems')
            sys.exit(1)

    def sell_limitR(self, market, quantitiy, rate, price = None):
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
            self.costum_print(' some problems')
            sys.exit(1)

    def get_open_orders(self, market):
        auth = self._url_market+'getopenorders?apikey='+self._apiKey+'&market='+market+'&nonce='+self.get_nonce()
        signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
        try:
            r = requests.get(auth, headers=headers)
            res = json.loads(r.content)
            self.costum_print(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        if( True is res.get('success')): #occhio a questo controllo perchè bittrex restituisce 'true' minuscolo
            self.costum_print('N° open orders '+str(len(res.get('result'))))  #STAMPA SOLO LUNGHRZZA PERCHÈ DURANTE IL TEST NON AVEVAMO OPEN ORDER E NON ERO SICURO DI COME PRENDERE I VALORI DEL JSON
            return len(res.get('result'))
        else:
            self.costum_print(' some problems')
            sys.exit(1)

    def cancel_order(self, uuid):
            auth = self._url_market+'cancel?apikey='+self._apiKey+'&uuid='+uuid+'&nonce='+self.get_nonce()
            signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
            headers = {'apisign': signature}
            try:
                r = requests.get(auth, headers=headers)
                res = json.loads(r.content)
                self.costum_print(r.content)
            except (r.status_code != 200):
                raise Exception('Some problems retrieving price: '+r.status_code)
            if( True is res.get('success')): #occhio a questo controllo perchè bittrex restituisce 'true' minuscolo
                self.costum_print('canceled order: '+str(res.get('result')['uuid']))  #STAMPA SOLO LUNGHRZZA PERCHÈ DURANTE IL TEST NON AVEVAMO OPEN ORDER E NON ERO SICURO DI COME PRENDERE I VALORI DEL JSON
                return True
            else:
                self.costum_print(' some problems')
                sys.exit(1)