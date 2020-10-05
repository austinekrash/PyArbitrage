import psycopg2
import requests
import json

try:
    conn = psycopg2.connect("dbname='' user='' host='' password=''")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

r = requests.get("https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange")
pairs = json.loads(r.content)[0]
list_of_records = []

for index in range(len(pairs)):
    if(len(pairs[index]) != 6):
        print("BAD ASSUMPTION")
        break 
    baseAsset = pairs[index][0:3]
    quoteAsset = pairs[index][3:6]
    assets = [baseAsset, quoteAsset]
    assets.sort()
    primary = 't'+pairs[index]
    record = [primary, baseAsset.upper(), quoteAsset.upper(), assets[0].lower()+assets[1].lower(), 'Bitfinex']
    list_of_records.append(record)

sql = """INSERT INTO Bitfinex(symbol, base_asset, quote_asset, symbol_std, exchange_name) VALUES(%s, %s, %s, %s, %s) ON CONFLICT (symbol) DO NOTHING;"""
cur.executemany(sql, list_of_records)
conn.commit()
count = cur.rowcount
print (count, "Record inserted successfully into BITFINEX table")
if(count != len(pairs)):
    print("#n of items inserted differs from those received: "+str(count)+" - "+str(len(pairs)))
cur.close()
conn.close()
