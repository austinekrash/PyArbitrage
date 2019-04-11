import requests
import json
import hashlib
import hmac
import time #for nonce
import base64
import bitfinexpy
import sys

class Bitfinex:

    __instance = None
    _table = 'bitfinex'
    _json = None
    _url = 'https://api-pub.bitfinex.com/v2/tickers?symbols=ALL'
    _bitfinex = None

    @staticmethod
    def Factory(apiKey, secretKey):
        if Bitfinex.__instance == None:
            Bitfinex(apiKey, secretKey)
        return Bitfinex.__instance

    def __init__(self, apiKey, secretKey):
        if Bitfinex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Bitfinex.__instance = self
            self._bitfinex = bitfinexpy.API(environment="live", key=apiKey , secret_key=secretKey)

    @staticmethod
    def get_nonce():
        return str(int(time.time()))
    
    def costum_print(self, text):
        print('['+self.__class__.__name__.upper()+'] '+str(text))


    def sync(self):
        try:
            r = requests.get(self._url)
            self._json = json.loads(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)

    def find_asset(self, symbol):
    #return base and quote asset
        if(symbol[-4:].lower()  == 'usdt'):
            return [symbol[1:-4], 'usdt']
        elif(symbol[-3:].lower()  == 'btc'):
            return [symbol[1:-3], 'btc']
        elif(symbol[-3:].lower()  == 'eth'):
            return [symbol[1:-3], 'eth']
        elif(symbol[-3:].lower()  == 'usd'):
            return [symbol[1:-3], 'usd']
        elif(symbol[-3:].lower()  == 'dai'):
            return [symbol[1:-3], 'dai']
        elif(symbol[-3:].lower()  == 'xlm'):
            return [symbol[1:-3], 'xlm']
        elif(symbol[-3:].lower()  == 'eos'):
            return [symbol[1:-3], 'eos']
        elif(symbol[-3:].lower()  == 'jpy'):
            return [symbol[1:-3], 'jpy']
        elif(symbol[-3:].lower()  == 'gbp'):
            return [symbol[1:-3], 'gbp']
        elif(symbol[-3:].lower()  == 'eur'):
            return [symbol[1:-3], 'eur']
        elif(symbol[1:4].lower()  == 'btc'):
            return [symbol[4:], 'btc']
        elif(symbol[1:4].lower()  == 'eth'):
            return [symbol[4:], 'eth']
        else:
            return ['', '']

    def get_price_pairs(self, pair_symbol):
        for item in self._json:
            if pair_symbol.lower() in item[0].lower():
                self.costum_print(pair_symbol+" "+str(item[7]))
                return float(item[7])
        self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1
    
    def get_deposit_address(self, symbol): #symbol NON è BTC ma bitcoin mentre altre no
        res = self._bitfinex.deposit(method=symbol.lower(), wallet_name='exchange', renew=1)
        self.costum_print(res)
        if(res['result'] == 'success'): #
            if('address_pool' in res):
                return res['address'], res['address_pool']
            else:
                return res['address']
        else:
            self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
            return -1

    def withdraw(self, symbol, to_address, amount, addressTag = None): #To be tested
        if addressTag is None:
            res = self._bitfinex.withdrawal('exchange', to_address, amount)
        else:
            res = self._bitfinex.withdrawal('exchange', to_address, amount, payment_id=addressTag)
        self.costum_print(res)
        return res


    def get_balance(self, symbol): #“trading”, “deposit” or “exchange” da capire quale ci serve a noi
        res = self._bitfinex.wallet_balances()
        for item in res:
            if item['currency'] == symbol.lower():
                print(item['type'], item['amount'],item['available'])
                return(item['type'], item['amount'],item['available'])
        self.costum_print(res)
        self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1


    def get_balances(self):
        res = self._bitfinex.wallet_balances()
        self.costum_print(str(res))
        return res


    #SONO DIVERSI GLI ARGOMENTI DELLE LIMIT RISPETTO A BIIREX
    def buy_currencyP(self, market, quantitiy, price, rate = None):
        res = self._bitfinex.new_offer(market, quantitiy, price, 'buy', 'fill-or-kill')
        self.costum_print(str(res))
        return res

    def sell_currencyP(self, market, quantitiy,  price, rate = None):
        res = self._bitfinex.new_offer(market, quantitiy, price, 'sell', 'fill-or-kill')
        self.costum_print(str(res))
        return res 

    def get_open_orders(self): #diversa dalle altre
        res = self._bitfinex.active_orders()
        self.costum_print(str(res))
        if len(res) > 1:
            return -1
        for item in res:
            return item['id']
        self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1

    def cancel_order(self, uuid): # qui non serve market
        res = self._bitfinex.cancel_order(uuid)
        self.costum_print(str(res))
        return res
    
######################################################################

    def get_withdraw_fee(self, symbol): #MAKER e TAKER NON SONO WITHDRAW FEE
        res = self._bitfinex.account_infos()
        #self.costum_print(res[0]['fees'])
        for item in res[0]['fees']:
            #self.costum_print(item['pairs'])
            if item['pairs'] == symbol.upper():
                self.costum_print(item)
                return item['maker_fees'], item['taker_fees']
        self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
        sys.exit(1)
    