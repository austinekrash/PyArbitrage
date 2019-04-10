import requests
import json
import hashlib
import hmac
import time #for nonce
import base64



class Bitfinex:

    __instance = None
    _table = 'bitfinex'
    _json = None
    _url = 'https://api-pub.bitfinex.com/v2/tickers?symbols=ALL'
    BASE_URL = "https://api.bitfinex.com/"
    KEY="RKv5MNSRaHCzaxF6OmYh7eIC3qc0v657izJ8EjzEHVd"
    SECRET= bytearray("xaXTd9er3aEelDpoBm9aS4YVeFNckmj2YgV6jVdiDod", "utf-8")

    @staticmethod
    def Factory():
        if Bitfinex.__instance == None:
            Bitfinex()
        return Bitfinex.__instance

    def __init__(self):
        if Bitfinex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Bitfinex.__instance = self

    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(int(round(time.time() * 1000)))

    def _headers(self, path, nonce, body):
        
        signature =  path + nonce + body
        print("Signing: " + signature)
        h = hmac.new(self.SECRET, signature.encode('utf8'), hashlib.sha384)
        signature = h.hexdigest()

        return {
            #"bfx-nonce": nonce,
            #"bfx-apikey": self.KEY,
            #"bfx-signature": signature,
            #"content-type": "application/json"
            'X-BFX-APIKEY': self.KEY,
            'X-BFX-PAYLOAD': body,
            'X-BFX-SIGNATURE': signature
        }

    def active_orders(self):
        """
        Fetch active orders
        """
        nonce = self._nonce()
        body = {}
        rawBody = json.dumps(body)
        path = "v2/auth/r/orders"


        print(self.BASE_URL + path)
        print(nonce)


        headers = self._headers(path, nonce, rawBody)

        print(headers)
        print(rawBody)


        print("requests.post("+self.BASE_URL + path + ", headers=" + str(headers) + ", data=" + rawBody + ", verify=True)")
        r = requests.post(self.BASE_URL + path, headers=headers, data=rawBody, verify=True)

        if r.status_code == 200:
            print(r.content)
            return r.json()
        else:
            print(r.status_code)
            #print(r)
            return ''

    def sync(self):
        try:
            r = requests.get(self._url)
            self._json = json.loads(r.content)
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)

    def get_price_pairs(self, pair_symbol):
        for index in range(len(self._json)):
            if pair_symbol.lower() in self._json[index][0].lower():
                #print("[BITFINEX] "+pair_symbol+" "+str(self._json[index][7]))
                return float(self._json[index][7])
        print("---------------------------------VALUE NOT FOUND---------------------------------")
        return -1
    
    def get_address(self, symbol):
        """
        Fetch active orders
        """
        nonce = self._nonce()
        body = {
            "request": "/v1/account_infos",
            "nonce": self._nonce(),
            #"method": "bitcoin",
            #"wallet_name": "exchange",
            #"renew": 1
            
        }
        tua_mamma = bytes(json.dumps(body),  "utf-8")
        print(type(tua_mamma))
        rawBody = base64.b64encode(tua_mamma).decode("utf-8")
        print(rawBody)
        stringbody = (tua_mamma.decode("utf-8"))
        print(stringbody)

        #= json.dumps(body)
        path = "/v1/account_infos"


        print(self.BASE_URL + path)
        print(nonce)


        headers = self._headers(path, nonce, rawBody)

        print(headers)
        print(rawBody)


        print("requests.post("+self.BASE_URL + path + ", headers=" + str(headers) + ", data=" + rawBody + ", verify=True)")
        r = requests.post(self.BASE_URL + path, headers=headers, data=rawBody)

        if r.status_code == 200:
            print(r.content)
            return r.json()
        else:
            print(r.status_code)
            #print(r)
            return ''