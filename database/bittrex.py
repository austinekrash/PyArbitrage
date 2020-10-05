import psycopg2
import requests
import json
from sup import find_asset_bittrex

try:
    conn = psycopg2.connect("dbname='' user='' host='' password=''")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

r = requests.get("https://api.bittrex.com/api/v1.1/public/getmarkets")
datastore = json.loads(r.content)
pairs = datastore.get('result')
list_of_records = []


for index in range(len(pairs)):
    baseAsset = pairs[index].get('MarketCurrency')
    quoteAsset = pairs[index].get('BaseCurrency')
    assets = [baseAsset, quoteAsset]
    assets.sort()
    record = [pairs[index].get('MarketName'), baseAsset.upper(), quoteAsset.upper(), assets[0].lower()+assets[1].lower(), 'Bittrex']
    list_of_records.append(record)

sql = """INSERT INTO Bittrex(symbol, base_asset, quote_asset, symbol_std, exchange_name) VALUES(%s, %s, %s, %s, %s) ON CONFLICT (symbol) DO NOTHING;"""
cur.executemany(sql, list_of_records)
conn.commit()
count = cur.rowcount
print (count, "Record inserted successfully into BITTREX table")
if(count != len(pairs)):
    print("#n of items inserted differs from those received: "+count+" - "+len(pairs))
cur.close()
conn.close()

