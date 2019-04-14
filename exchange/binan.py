import requests
import json
import time
import hmac
import hashlib
import sys
from binance.client import Client
'''
BITFINEX 
Maker  0.100%
Taker 0.200%
https://api.bitfinex.com/v1/account_infos maker taker
https://api.bitfinex.com/v1/account_fees withdraw
https://www.bitfinex.com/fees

#Poloniex
Maker 0.08% 
Taker 0.20%
https://docs.poloniex.com/#returnchartdata


#BINANCE
Maker 0.1000%
Taker 0.1000%
Deposit FREE
address = client.get_withdraw_fee(asset='BTC')

BIITREX

'''
class Binance():

    __instance = None
    _table = 'binance'
    _json = None
    _fee = None
    _client = None
    _url = 'https://binance.com/api/v3/ticker/price'
    _url_fee = 'https://binance.com/api/v1/exchangeInfo'

    @staticmethod
    def Factory(apiKey, secretKey):
        if Binance.__instance == None:
            Binance(apiKey, secretKey)
        return Binance.__instance

    def __init__(self, apiKey, secretKey):
        if Binance.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Binance.__instance = self
            self._client = Client(apiKey, secretKey)

    @staticmethod
    def get_nonce():
        return str(int(time.time()))
    
    def costum_print(self, text):
        print('['+self.__class__.__name__.upper()+'] '+str(text))
    
    def sync(self):
        try:
            r = requests.get(self._url)
            self._json = json.loads(r.content)

            r2 = requests.get(self._url_fee)
            self._fee = json.loads(r2.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
    
    def get_price_pairs(self, pair_symbol):
        print(pair_symbol)
        for item in self._json:
            if pair_symbol.lower() in item['symbol'].lower():
                self.costum_print(item['symbol']+" "+str(item['price']))
                return float(item['price'])
        self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1

    def find_asset(self, pair_symbol):
        pairs = self._fee.get('symbols')
        for index in range(len(pairs)):
            if pairs[index].get('symbol') == pair_symbol:
                print("-------------------------------------------------------- "+pairs[index].get('baseAsset'), pairs[index].get('quoteAsset'))
                return [pairs[index].get('baseAsset'), pairs[index].get('quoteAsset')]
        return -1

    def get_deposit_address(self, symbol):
        if (self.is_frozen(symbol) == -1):
            self.costum_print('Frozen '+symbol)
            return -1
        res = self._client.get_deposit_address(asset=symbol)
        if res['success'] is True:
            self.costum_print(res)
            return {'address':res['address'], 'addressTag': res['addressTag']}
        else:
            self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
            return -1

    def withdraw(self, symbol, to_address, amount, addressTag = None): #To be tested
        if addressTag is None:
            return self._client.withdraw(asset=symbol, address=to_address, amount=amount)
        else:
            return self._client.withdraw(asset=symbol, address=to_address, addressTag='<xrp_address_tag>', amount=amount)


    def get_balance(self, symbol): # return couple: free, locked
        res = self._client.get_asset_balance(asset=symbol)
        #self.costum_print(res)
        return res['free'], res['locked']

    def get_balances(self):
        res = self._client.get_account()
        self.costum_print(res)
        return res


    #SONO DIVERSI GLI ARGOMENTI DELLE LIMIT RISPETTO A BIIREX
    def buy_currencytP(self, market, quantitiy, price, rate = None):
        res = self._client.order_limit_buy(symbol=market, quantity=quantitiy, price=price)
        self.costum_print(res)
        return res

    def sell_currencyP(self, market, quantitiy,  price, rate = None):
        res = self._client.order_limit_sell(symbol=market, quantity=quantitiy, price=price)
        self.costum_print(res)
        return res

    def get_open_orders(self):
        res = self._client.get_open_orders()
        self.costum_print(res)
        return res

    def cancel_order(self, market, uuid):
        res = self._client.cancel_order(symbol=market, orderId=uuid)
        self.costum_print(res)
        return res
    
    def get_withdraw_fee(self, symbol):
        res = self._client.get_withdraw_fee(asset=symbol)
        self.costum_print(res)
        return res
    
    def is_frozen(self, pair): #return depositStatus, withdrawStatus
        symbol = self.find_asset(pair)[0]
        res = self._client.get_asset_details()
        if self.is_tradable(pair) == False:
            return {'withdrawal': True, 'deposit': True}
        if( res['success'] is True):
            for key,value in res['assetDetail'].items():
                if(key == symbol):
                    return {'withdrawal': not value['withdrawStatus'], 'deposit': not value['depositStatus']}
                    #return not value['depositStatus'], not value['withdrawStatus']
            self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
            return {'withdrawal': True, 'deposit': True}
        else:
            self.costum_print('Frozen')
            return {'withdrawal': True, 'deposit': True}

    def is_tradable(self, pair):
        for item in self._fee['symbols']:
            if pair.lower() == item['symbol'].lower():
                if item['status'].lower() == 'trading':
                    return True
                else:
                    return False
    
    def is_tradable(self, symbol):
        pass

'''    
    def get_price_pairs(self, pair_symbol):
        for index in range(len(self._json)):
            if self._json[index]['symbol'].lower() == pair_symbol.lower():
                #self.costum_print("self._json[index]['price']+" "+self._json[index]['symbol'])
                return float(self._json[index]['price'])
        print("---------------------------------VALUE NOT FOUND---------------------------------")
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
            self.costum_print(' some problems')
            sys.exit(1)
'''
