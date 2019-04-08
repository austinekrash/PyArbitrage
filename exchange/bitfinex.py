
import psycopg2
import requests
import json


class Bitfinex:

    __instance = None
    _db = "dbname='arbitraggio' user='ale' host='localhost' password='pippo'"
    _conn = None
    _cur = None
    _pairs_record = None
    _table = 'bitfinex'


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
            r = requests.get('https://api-pub.bitfinex.com/v2/ticker/'+self._pairs_record[pair_index][0])
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        res = json.loads(r.content)
        print("[BITFINEX] "+self._pairs_record[pair_index][0]+" "+str(res[6]))
        
    def close(self):
        if(self._conn):
            self._cur.close()
            self._conn.close()
            print("[BITFINEX] PostgreSQL connection is closed")