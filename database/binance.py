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
symbols = datastore.get('symbols')
list_of_records = []

for index in range(len(symbols)):
    record = [symbols[index]['symbol'], symbols[index]['quoteAsset'], symbols[index]['baseAsset'], (symbols[index]['symbol']).lower()]
    list_of_records.append(record)

sql = """INSERT INTO binance(symbol, quote_asset, base_asset, symbol_std) VALUES(%s, %s, %s, %s) ON CONFLICT (symbol) DO NOTHING;"""
#record_to_insert = ['ETHBTC', 'BTC', 'ETH', 'ethbtc']
#cur.execute(sql, record_to_insert)
cur.executemany(sql, list_of_records)
conn.commit()
count = cur.rowcount
print (count, "Record inserted successfully into binance table")

