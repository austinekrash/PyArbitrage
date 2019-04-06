
import psycopg2
import requests
import json


class Poloniex:

    __instance = None
    _db = "dbname='arbitraggio' user='ale' host='localhost' password='pippo'"
    _conn = None
    _cur = None
    _pairs_record = None
    _table = 'poloniex'


    @staticmethod
    def Factory():
        if Poloniex.__instance == None:
            Poloniex()
        return Poloniex.__instance

    def __init__(self):
        if Poloniex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Poloniex.__instance = self
            try:
                self._conn = psycopg2.connect(self._db)
            except:
                print("I am unable to connect to the database")
                return
            self._cur = self._conn.cursor()
            self._cur.execute('SELECT * FROM '+self._table)
            self._pairs_record = self._cur.fetchall()
            

    def get_records(self):
        for row in self._pairs_record:
            print(row)

    def get_price_pairs(self, pair_index):
        if(pair_index > len(self._pairs_record)):
            raise Exception("pair_index > len(self._pairs_record)")
        try:
            r = requests.get('https://poloniex.com/public?command=returnTicker')
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        res = json.loads(r.content)
        for key, value in res.items():
            if(self._pairs_record[pair_index][0] == key):
                symbol = key
                price = value['last']
        print("[POLONIEX] "+price+" "+symbol)
        
    def close(self):
        if(self._conn):
            self._cur.close()
            self._conn.close()
            print("[POLONIEX] PostgreSQL connection is closed")
