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
    _tradables = None
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
            self._apiKey = apiKey
            self._secretKey = bytearray(secretKey, "utf-8")

    @staticmethod
    def get_nonce():
        return str(int(time.time()))
    
    def costum_print(self, text):
        print('['+self.__class__.__name__.upper()+'] '+str(text))


    def sync(self):  #era self.-urk
        _url = self._url + '/public/getmarketsummaries'
        try:
            r = requests.get(_url)
            self._json = json.loads(r.content).get('result')
            _url = self._url + '/public/getmarkets'
            r = requests.get(_url)
            self._tradables = json.loads(r.content).get('result')
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)

    def find_asset(self, pair):
    #return base and quote asset
        if(pair[:4].lower()  == 'usdt'):
            return [pair[5:], 'usdt']
        elif(pair[:3].lower()  == 'btc'):
            return [pair[4:], 'btc']
        elif(pair[:3].lower()  == 'eth'):
            return [pair[4:], 'eth']
        elif(pair[:3].lower()  == 'usd'):
            return [pair[4:], 'usd']
        else:
            -1

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
        self.costum_print('start')
        try:
            r = requests.get(auth, headers=headers)
            res = json.loads(r.content)
            self.costum_print(res)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        
        if( True is res.get('success')):
            address = None
            self.costum_print(res.get('result').get('Address'))
            if(symbol == 'XLM'):
                address = 'GB6YPGW5JFMMP2QB2USQ33EUWTXVL4ZT5ITUNCY3YKVWOJPP57CANOF3'
                
            elif(symbol == 'NXT'):
                address = 'NXT-97H4-KRWL-A53G-7GVRG'

            elif(symbol == 'XMR'):
                address = '463tWEBn5XZJSxLU6uLQnQ2iY9xuNcDbjLSjkn3XAXHCbLrTTErJrBWYgHJQyrCwkNgYvyV3z8zctJLPCZy24jvb3NiTcTJ'
            
            elif(symbol == 'BURST'):
                address = 'BURST-HK9D-P74Q-XDEJ-D6PGM'

            elif(symbol == 'BITS'):
                address = 'ARDOR-S42Z-ERET-QLMX-4JR77'

            elif(symbol == 'XRP'):
                address = 'rPVMhWBsfF9iMXYj3aAzJVkPDTFNSyWdKy'

            elif(symbol == 'AEON'):
                address = 'WmtK9TQ6yd2ZWZDAkRsebc2ppzUq2Wuo9XRRjHMH2fvqM3ARVqk3styJ6AavJFcpJFPFtxRGAqGFoJMZGJ6YYzQ61TYGfpykX'

            elif(symbol == 'STEEM'):
                address = 'bittrex'

            elif(symbol == ' SBD'):
                address = 'bittrex'

            elif(symbol == 'ARDR'):
                address = 'ARDOR-XK2L-Z7NK-VNKM-AZYVT'

            elif(symbol == 'GOLOS'):
                address = 'bittrex'

            elif(symbol == 'GBG'):
                address = 'bittrex'

            elif(symbol == 'DCT'):
                address = 'bittrex'

            elif(symbol == 'XEL'):
                address = 'XEL-AQVJ-PPCK-QJYJ-8T65V'

            elif(symbol == 'IGNIS'):
                address = 'ARDOR-BG2F-QZ3B-H99Y-6PSGQ'
            if (address is None):
                return {'address': res.get('result').get('Address'), 'addressTag': ''} 
            else:
                return {'address': address, 'addressTag': res.get('result').get('Address')} #Su bittrex restituiscono il tag e lasciano invatiato l'address per le crypto con il payment id
        else:
            p = res.get('message')
            self.costum_print(p)
            if(p in 'ADDRESS_GENERATING'):
                self.costum_print(res.get('message'))
                time.sleep(2)
                return self.get_deposit_address(symbol)
            else:
                self.costum_print(res.get('message')+' 2')
                return -1
        self.costum_print('male')

        #aggiungere tag su monete tipo ripple

    def is_frozen(self, pair):
        if self.is_tradable(pair):
            return {'withdrawal': False, 'deposit': False}
        symbol = self.find_asset(pair)[0]
        auth = self._url_account+'getdepositaddress?apikey='+self._apiKey+'&currency='+symbol+'&nonce='+self.get_nonce()
        signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'apisign': signature}
        try:
            r = requests.get(auth, headers=headers)
            res = json.loads(r.content)
            self.costum_print(res)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        p = res.get('message')
        if( p == 'CURRENCY_OFFLINE'):
            return {'withdrawal': True, 'deposit': True}
        return {'withdrawal': False, 'deposit': False}

    def is_tradable(self, pair):
        for item in self._tradables:
            if(item['MarketName'] == pair):
                return item.get('IsActive')
        return False

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


'''
auth = self._url_account_v3_alpha+'addresses/'+symbol
print(auth)
Api_Timestamp = self.get_nonce()
print(Api_Timestamp)
content = hashlib.sha512(''.encode('utf-8')).hexdigest()
print(content)
presign = (Api_Timestamp+auth+'GET'+content+'').encode('utf-8')
print(presign)
signature = hmac.new(self._secretKey, presign, hashlib.sha512).hexdigest()
print(signature)
#signature = hmac.new(self._secretKey, auth.encode('utf-8'), hashlib.sha512).hexdigest()
headers = {'Api-Key': self._apiKey, 'Api-Timestamp': Api_Timestamp, 'Api-Content-Hash':content,'Api-Signature':signature }
'''