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
    _apiKey = None
    _secretKey = None
    
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

    def find_asset(self, symbol):
    #return base and quote asset
        if(symbol[:4].lower()  == 'usdt'):
            return [symbol[5:], 'usdt']
        elif(symbol[:3].lower()  == 'btc'):
            return [symbol[4:], 'btc']
        elif(symbol[:3].lower()  == 'eth'):
            return [symbol[4:], 'eth']
        elif(symbol[:3].lower()  == 'usd'):
            return [symbol[4:], 'usd']

    def get_price_pairs(self, pair_symbol):
        for item in self._json:
            if pair_symbol.lower() in item['MarketName'].lower():
                self.costum_print(item['MarketName']+" "+str(item['Last']))
                return float(item['Last'])
        self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1

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
        #aggiungere tag su monete tipo ripple

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
            return -1

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
            return res.get('result').get('Balance'), res.get('result').get('Available'), res.get('result').get('Pending')
        else:
            self.costum_print('some problems')
            return -1
        #restituire la tupla

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
            return -1



    def buy_currencyR(self, market, quantitiy, rate, price = None):
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
            return -1

    def sell_currencyR(self, market, quantitiy, rate, price = None):
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
            return -1

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
            return res.get('result')
        else:
            self.costum_print(' some problems')
            return -1

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
                return res.get('result')
            else:
                self.costum_print(' some problems')
                return -1