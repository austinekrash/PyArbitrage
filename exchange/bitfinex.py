import requests
import json


class Bitfinex:

    __instance = None
    _table = 'bitfinex'
    _json = None
    _url = 'https://api-pub.bitfinex.com/v2/tickers?symbols=ALL'
    BASE_URL = "https://api.bitfinex.com/"
    KEY="RKv5MNSRaHCzaxF6OmYh7eIC3qc0v657izJ8EjzEHVd"
    SECRET="xaXTd9er3aEelDpoBm9aS4YVeFNckmj2YgV6jVdiDod"

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

        signature = "/api/" + path + nonce + body
        print(")Signing: " + signature)
        h = hmac.new(self.SECRET.encode('utf8'), signature.encode('utf8'), hashlib.sha384)
        signature = h.hexdigest()

        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.KEY,
            "bfx-signature": signature,
            "content-type": "application/json"
        }

    def get_address(self, symbol):
        nonce = self._nonce()
        body = {}
        rawBody = json.dumps(body)
        path = "/v1/deposit/new"


        print(self.BASE_URL + path)
        print(nonce)


        headers = self._headers(path, nonce, rawBody)

        print(headers)
        print(rawBody)
        print("requests.post("+self.BASE_URL + path + ", headers=" + str(headers) + ", data=" + rawBody + ", verify=True)")
        r = requests.post(self.BASE_URL + path, headers=headers, data=rawBody, verify=True)

        if r.status_code == 200:
            return r.json()
        else:
            print(r.status_code)
            print(r)
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
        