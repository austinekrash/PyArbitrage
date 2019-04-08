import psycopg2
import requests
import json

try:
    conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='localhost' password='pippo'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

r = requests.get("https://poloniex.com/public?command=returnTicker")
datastore = json.loads(r.content)
list_of_records = []

#In Poloniex il primo è il QUOTE ed il secondo il BASE
for key, value in datastore.items():
    assets = key.split('_')
    baseAsset = assets[1]
    quoteAsset = assets[0]
    assets.sort()
    record = [key, baseAsset.upper(), quoteAsset.upper(), assets[0].lower()+assets[1].lower(), 'Poloniex']
    list_of_records.append(record)

sql = """INSERT INTO Poloniex(symbol, base_asset, quote_asset, symbol_std, exchange_name) VALUES(%s, %s, %s, %s, %s) ON CONFLICT (symbol) DO NOTHING;"""
cur.executemany(sql, list_of_records)
conn.commit()
count = len(list_of_records)
print (count, "Record inserted successfully into POLONIEX table")
if(count != len(datastore.items())):
    print("#n of items inserted differs from those received: "+str(count)+" - "+str(len(datastore.items())))
cur.close()
conn.close()


