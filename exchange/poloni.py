import requests
import json
import time
import hmac
import hashlib
import sys
from poloniex import Poloniex as polo

class Poloniex():

    __instance = None
    _table = 'poloniex'
    _json = None
    _url = 'https://poloniex.com/public?command=returnTicker'
    _baseUrl = 'https://poloniex.com/tradingApi'
    pol = None

    @staticmethod
    def Factory(apiKey, secreKey):
        if Poloniex.__instance == None:
            Poloniex(apiKey, secreKey)
        return Poloniex.__instance

    def __init__(self, apiKey, secretKey):
        if Poloniex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Poloniex.__instance = self
            self.pol = polo(apiKey, secretKey)

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
        if(symbol[:4].lower()  == 'usdt'):
            return [symbol[5:], 'usdt']
        elif(symbol[:3].lower()  == 'btc'):
            return [symbol[4:], 'btc']
        elif(symbol[:3].lower()  == 'eth'):
            return [symbol[4:], 'eth']
        elif(symbol[:3].lower()  == 'xmr'):
            return [symbol[4:], 'xmr']
        elif(symbol[:4].lower()  == 'usdc'):
            return [symbol[5:], 'usdc']

    def get_price_pairs(self, pair_symbol):
        for key, value in self._json.items():
            if(pair_symbol.lower() == key.lower()):
                symbol = key
                price = value['last']
                self.costum_print(symbol+" "+str(price))
                return float(price)
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1
    
    def get_deposit_address(self, symbol):
        res = self.pol.generateNewAddress(symbol)
        self.costum_print(res)
        if res['success'] == 1:
            return {'address':res['response'], 'addressTag': '123456'}
        elif res['success'] == 0:
            listAddress = self.__return_deposit_address()
            return {'address': listAddress[symbol], 'addressTag': '123456'}
            #todo nel caso di errore return -1
    
    def __return_deposit_address(self):
        return self.pol.returnDepositAddresses()
    
    def get_balances(self):
        res  = self.pol.returnCompleteBalances()
        self.costum_print(res)
        return res

    def get_balance(self, symbol):
        res  = self.pol.returnCompleteBalances()[symbol]
        self.costum_print(res)
        return res['available'], res['onOrders']

        
    def get_available_account_balances(self):
        res = self.pol.returnAvailableAccountBalances()
        self.costum_print(res)
        return res
        #return -1 se errore

    def get_open_orders(self):
        res = self.pol.returnOpenOrders()
        for key, value in res.items():
            if value:
                self.costum_print(value)
                return value['orderNumber']
        self.costum_print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1
        #assumiamo che ci sia solo 1 ordine
    
    def buy_currency(self, currencyPair, amount, rate, orderType=False):
        res = self.pol.buy(currencyPair, rate, amount, orderType=False)
        self.costum_print(res)
        return res
        """You may optionally set "orderType"
        to "fillOrKill", "immediateOrCancel" or "postOnly". A fill-or-kill order
        will either fill in its entirety or be completely aborted. An
        immediate-or-cancel order can be partially or completely filled, but
        any portion of the order that cannot be filled immediately will be
        canceled rather than left on the order book. A post-only order will
        only be placed if no portion of it fills immediately; this guarantees
        you will never pay the taker fee on any part of the order that fills.
        If successful, the method will return the order number."""

    def sell_currency(self, currencyPair, rate, amount, orderType=False):
        res = self.pol.sell(currencyPair, rate, amount, orderType=False)
        self.costum_print(res)
        return res
        """You may optionally set "orderType"
        to "fillOrKill", "immediateOrCancel" or "postOnly". A fill-or-kill order
        will either fill in its entirety or be completely aborted. An
        immediate-or-cancel order can be partially or completely filled, but
        any portion of the order that cannot be filled immediately will be
        canceled rather than left on the order book. A post-only order will
        only be placed if no portion of it fills immediately; this guarantees
        you will never pay the taker fee on any part of the order that fills.
        If successful, the method will return the order number."""

    def cancel_order(self, orderNumber):
        res = self.pol.cancelOrder(orderNumber)
        self.costum_print(res)
        return res

    def move_order(self, orderNumber, rate, amount=False, orderType=False):
        res = self.pol.moveOrder(orderNumber, rate, amount=False, orderType=False)
        self.costum_print(res)
        return res

    def withdraw(self, currency, address, amount, paymentId=False):
        res = self.pol.withdraw(currency, amount, address, paymentId=False)
        self.costum_print(res)
        return res
        #vedere come funziona
        #vedere errori tipo min withdraw

    def return_fee_info(self):
        res = self.pol.returnFeeInfo()
        self.costum_print(res)
        return res
        #da vedere poi cosa far restituire
        #per ora non serve
    
    def __is_frozen(self, symbol):
        res = self.pol.returnCurrencies().get(symbol)
        self.costum_print(res)
        if res['disabled'] == 0 and res['delisted'] == 0 and res['frozen'] == 0:
            return 0
        else:
            return 1
