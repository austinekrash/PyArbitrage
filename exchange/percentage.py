import psycopg2
import requests
import json
from binance import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from cex import Cex
from poloniex import Poloniex

def percentage(cryptoIntersection):
    exchange1 = (cryptoIntersection[3])[0].upper() + (cryptoIntersection[3])[1:]
    exchange2 = (cryptoIntersection[4])[0].upper() + (cryptoIntersection[4])[1:]
    symbol1 = cryptoIntersection[0]
    symbol2 = cryptoIntersection[1]
    baseAsset = cryptoIntersection[2]
    price1 = eval(exchange1).get_price_pairs(symbol1)
    price2 = eval(exchange2).get_price_pairs(symbol2)
    if(price1 >= price2):
        perc = (price1 - price2) / price2 * 100
        return {"percentage": perc ,"startExchange": exchange2, "startSymbol": symbol2, "startPrice": price2, "endExchange": exchange1, "endSymbol": symbol1, "endPrice": price1}
    else:
        perc = (price2 - price1) / price1 * 100
        return {"percentage": perc ,"startExchange": exchange1, "startSymbol": symbol1, "startPrice": price1, "endExchange": exchange2, "endSymbol": symbol2, "endPrice": price2}
    #return tupla con percentuale, exchange di partenza, exchange di destinazione


intersectionView = []
perc = []
Binance = Binance().Factory()
Binance.sync()
Bittrex = Bittrex().Factory()
Bittrex.sync()
Bitfinex = Bitfinex().Factory()
Bitfinex.sync()
Cex = Cex().Factory()
Cex.sync()
Poloniex = Poloniex().Factory()
Poloniex.sync()

try:
    conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='localhost' password='pippo'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'VIEW' AND table_name = 'intersection_binance_poloniex'")
records = cur.fetchall()

for x in records:
    intersectionView.append(x[0]) #faccio una lista con tutte le view contenenti le intersezioni tra exchange

#per ogni exchange prendo la lista delle crypto
for view in intersectionView:
    cur.execute("SELECT * FROM "+view)
    cryptoIntersection = []
    symbol = []
    for x in cur.fetchall():#prendo tutte le tuple per ogni view
        cryptoIntersection.append(x)
        for i in cryptoIntersection:
            
            perc.append(percentage(i))
            print(percentage(i))
            #chiamo api prezzo su symbol
            #inserisco in perc la coppia o tripla symbol std_symbol percentuale
            #non ha senso prendere anche il prezzo, perchè il prezzo va preso subito prima della vednita/Acquisto

print(percentage)