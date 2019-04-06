import psycopg2
import requests
import json

try:
    conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='localhost' password='pippo'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

r = requests.get("https://binance.com/api/v1/exchangeInfo")
datastore = json.loads(r.content)
pairs = datastore.get('symbols')
list_of_records = []

for index in range(len(pairs)):
    baseAsset = pairs[index].get('baseAsset')
    quoteAsset = pairs[index].get('quoteAsset')
    assets = [baseAsset, quoteAsset]
    assets.sort()
    record = [pairs[index].get("symbol"), baseAsset.upper(), quoteAsset.upper(), assets[0].lower()+assets[1].lower()]
    list_of_records.append(record)

sql = """INSERT INTO binance(symbol, base_asset, quote_asset, symbol_std) VALUES(%s, %s, %s, %s) ON CONFLICT (symbol) DO NOTHING;"""
cur.executemany(sql, list_of_records)
conn.commit()
count = cur.rowcount
print (count, "Record inserted successfully into BINANCE table")
if(count != len(pairs)):
    print("#n of items inserted differs from those received: "+count+" - "+len(pairs))
cur.close()
conn.close()
