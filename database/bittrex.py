import psycopg2
import requests
import json
from sup import find_asset

try:
    conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='localhost' password='pippo'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

r = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummaries")
datastore = json.loads(r.content)
symbols = datastore.get('result')
list_of_records = []


sql = """INSERT INTO bittrex(symbol, quote_asset, base_asset, symbol_std) VALUES(%s, %s, %s, %s);"""

for index in range(len(symbols)):
    asset = find_asset(symbols[index]['MarketName'])
    record = [symbols[index]['MarketName'], asset[0].lower(), asset[1].lower(), asset[0].lower() + asset[1].lower()]
    list_of_records.append(record)

cur.executemany(sql, list_of_records)
conn.commit()
count = cur.rowcount
print (count, "Record inserted successfully into bittrex table")
