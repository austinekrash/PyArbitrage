import psycopg2
import requests
import json
import re

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
    pass
    #print(symbols[index]['MarketName'])

def find_base_asset(symbol):
    #da finire
    reUsdt = re.compile(r"\busdt\b")
    reBtc = re.compile(r"\bbtc\b")
    reEth = re.compile(r"\beth\b")
    reUsd = re.compile(r"\busd\b")
    if(reUsdt.search(symbol[:4]) is not None):
        return [symbol[5:], 'usdt']
    elif(reBtc.findall(symbol[:4]) is not None):
        return [symbol[3:], 'btc']
    elif(reEth.findall(symbol[:4]) is not None):
        return [symbol[3:], 'eth']
    elif(reUsd.findall(symbol[:4]) is not None):
        return [symbol[3:], 'usd']


print(find_base_asset('USD_DFER'))

#usdt, usd, btc, eth
    #record = [symbols[index]['MarketName'], symbols[index]['quoteAsset'], symbols[index]['baseAsset'], (symbols[index]['symbol']).lower()]
    #list_of_records.append(record)

#record_to_insert = ['ETHBTC', 'BTC', 'ETH', 'ethbtc']
#cur.execute(sql, record_to_insert)


#cur.executemany(sql, list_of_records)
#conn.commit()
#count = cur.rowcount
#print (count, "Record inserted successfully into binance table")
