
import psycopg2
import requests
import json


class Bittrex:

    __instance = None
    _db = "dbname='arbitraggio' user='ale' host='localhost' password='pippo'"
    _conn = None
    _cur = None
    _pairs_record = None
    _table = 'bittrex'


    @staticmethod
    def Factory():
        if Bittrex.__instance == None:
            Bittrex()
        return Bittrex.__instance

    def __init__(self):
        if Bittrex.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            Bittrex.__instance = self
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
            r = requests.get('https://api.bittrex.com/api/v1.1/public/getticker?market='+self._pairs_record[pair_index][0])
        except (r.status_code != 200):
            raise Exception('Some problems retrieving price: '+r.status_code)
        res = json.loads(r.content).get("result")
        print("[BITTREX] "+self._pairs_record[pair_index][0]+" "+str(res.get("Last")))
        
    def close(self):
        if(self._conn):
            self._cur.close()
            self._conn.close()
            print("[BITTREX] PostgreSQL connection is closed")