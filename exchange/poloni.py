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

    def get_price_pairs(self, pair_symbol):
        for key, value in self._json.items():
            if(pair_symbol.lower() == key.lower()):
                symbol = key
                price = value['last']
                #print("[POLONIEX] "+price+" "+symbol)
                return float(price)
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        sys.exit(1)
    
    def get_deposit_address(self, symbol):
        res = self.pol.generateNewAddress(symbol)
        if res['success'] == 1:
            return res['response']
        elif res['success'] == 0:
            listAddress = self.return_deposit_address()
            return listAddress[symbol]
    
    def return_deposit_address(self):
        return self.pol.returnDepositAddresses()
    
    def return_complete_balances(self):
        return self.pol.returnCompleteBalances()

    def return_crypto_balances(self, symbol):
        return self.pol.returnCompleteBalances()[symbol]
        
    def return_available_account_balances(self):
        return self.pol.returnAvailableAccountBalances()

    def return_open_orders(self):
        return self.pol.returnOpenOrders()
    
    def buy_currency(self, currencyPair, rate, amount, orderType=False):
        """You may optionally set "orderType"
        to "fillOrKill", "immediateOrCancel" or "postOnly". A fill-or-kill order
        will either fill in its entirety or be completely aborted. An
        immediate-or-cancel order can be partially or completely filled, but
        any portion of the order that cannot be filled immediately will be
        canceled rather than left on the order book. A post-only order will
        only be placed if no portion of it fills immediately; this guarantees
        you will never pay the taker fee on any part of the order that fills.
        If successful, the method will return the order number."""
        return self.pol.buy(currencyPair, rate, amount, orderType=False)

    def sell_currency(self, currencyPair, rate, amount, orderType=False):
        """You may optionally set "orderType"
        to "fillOrKill", "immediateOrCancel" or "postOnly". A fill-or-kill order
        will either fill in its entirety or be completely aborted. An
        immediate-or-cancel order can be partially or completely filled, but
        any portion of the order that cannot be filled immediately will be
        canceled rather than left on the order book. A post-only order will
        only be placed if no portion of it fills immediately; this guarantees
        you will never pay the taker fee on any part of the order that fills.
        If successful, the method will return the order number."""
        return self.pol.sell(currencyPair, rate, amount, orderType=False)

    def cancel_order(self, orderNumber):
        return self.pol.cancelOrder(orderNumber)

    def move_order(self, orderNumber, rate, amount=False, orderType=False):
        return self.pol.moveOrder(orderNumber, rate, amount=False, orderType=False)

    def withdraw(self, currency, amount, address, paymentId=False):
        return self.pol.withdraw(currency, amount, address, paymentId=False)

    def return_fee_info(self):
        return self.pol.returnFeeInfo()

