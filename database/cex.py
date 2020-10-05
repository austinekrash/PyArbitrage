import psycopg2
import requests
import json


try:
    conn = psycopg2.connect("dbname='' user='' host='' password=''")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

r = requests.get("https://cex.io/api/currency_limits")
datastore = json.loads(r.content)
pairs = datastore.get('data').get('pairs')
list_of_records = []

for index in range(len(pairs)):
    baseAsset = pairs[index].get('symbol1')
    quoteAsset = pairs[index].get('symbol2')
    assets = [baseAsset, quoteAsset]
    assets.sort()
    primary = baseAsset+'/'+quoteAsset
    record = [primary, baseAsset.upper(), quoteAsset.upper(), assets[0].lower()+assets[1].lower(), 'Cex']
    list_of_records.append(record)

sql = """INSERT INTO Cex(symbol, base_asset, quote_asset, symbol_std, exchange_name) VALUES(%s, %s, %s, %s, %s) ON CONFLICT (symbol) DO NOTHING;"""
cur.executemany(sql, list_of_records)
conn.commit()
count = cur.rowcount
print (count, "Record inserted successfully into CEX table")
if(count != len(pairs)):
    print("#n of items inserted differs from those received: "+count+" - "+len(pairs))
cur.close()
conn.close()
