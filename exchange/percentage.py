import sys
import json
import requests
import psycopg2
from binan import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from cex import Cex
from poloni import Poloniex

E_BINANCEapiKey = 'WXYox2eh9V8fUiLvjdW9f8xkh3q30EpzxGaeLQvxMZ0TTUyDSaIJliEmAXr2NtYN'
E_BINANCEsecretKey = 'qbXdJU82w1QKpjHe6OFRMdJMxbZgQuHigLRzssDqf3TCpEaxyAaHyrGolDQzbrbD'

E_BITTREXapiKey = 'd94bf4036b9841729f2d5100ee9132a4'
E_BITTREXsecretKey = '672e4f9fea3b4628b1bf5617fbdb22be'

E_POLONIEXapiKey = '8QF9DS6A-YJWQQLWW-ZKUM8YV8-YJ5HG70E'
E_POLONIEXsecretKey = '6dd1afa15f71fe6c77bb0fd9348058f9d45deb99d0e9c5aed2752f974919f5b381db5f5e458c558e720805a1d840f56064253cce64a4c84fc0b05ad8f51d8ecc'

#Api ale
A_POLONIEXapiKey = '74DRDEIV-2G9W6KXO-QK6FY8Z9-LP1CAT98'
A_POLONIEXsecretKey = '16962e88b0e3349e2f774d6eb5dd5bde54a59bcd120c637e0e2cca5dbb0f77d93379416ab4e6dbc4fe9116007a548913b1f7815fb306484e14fc4df6c3c23486'

A_BITFINEXapiKey = 'SxBHFSegUgIjDXCKCJSbGRPAxmGdgNCVFRStoVkLaaD'
A_BITFINEXsecretKey = '7Ud65qmtjg1lFA4j1u8e5tu3CeU4bL2V4Ni79an6B0P'

def costum_print(text):
        print('[PERCENTAGE] '+str(text))   

def open_db():
    try:
        conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='localhost' password='pippo'")
    except:
        costum_print("I am unable to connect to the database")
        sys.exit(1)
    cur = conn.cursor()
    return conn, cur

def fetch_views_db(cur):
    intersectionView = []
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'VIEW'")
    records = cur.fetchall()
    for x in records:
        intersectionView.append(x[0]) # faccio una lista con tutte le view contenenti le intersezioni tra exchange
    return intersectionView

def close_db(conn, cur):
    conn.close()
    cur.close()
    costum_print("DB successfully closed")


def initialize_exchanges():
    binance = Binance.Factory(E_BINANCEapiKey, E_BINANCEsecretKey)
    bitfinex = Bitfinex.Factory(A_BITFINEXapiKey, A_BITFINEXsecretKey)
    bittrex = Bittrex.Factory(E_BITTREXapiKey,E_BITTREXsecretKey)
    poloniex = Poloniex.Factory(A_POLONIEXapiKey, A_POLONIEXsecretKey)
    cex = Cex.Factory() # Sarà da togliere
    binance.sync()
    bitfinex.sync()
    bittrex.sync()
    poloniex.sync()
    cex.sync()
    return binance, bitfinex, bittrex, poloniex, cex

def compute_percentages(intersectionView, cur):
    percentages = []
    #per ogni exchange prendo la lista delle crypto
    for view in intersectionView:
        cur.execute("SELECT * FROM "+view)
        cryptoIntersection = []
        for x in cur.fetchall():#prendo tutte le tuple per ogni view
            cryptoIntersection.append(x)
            percentages.append(__percentage(x))            
            #chiamo api prezzo su symbol
            #inserisco in percentages la coppia o tripla symbol std_symbol percentuale
            #non ha senso prendere anche il prezzo, perchè il prezzo va preso subito prima della vednita/Acquisto
    return percentages

def __percentage(cryptoIntersection):
    exchange1 = (cryptoIntersection[3]).lower()
    exchange2 = (cryptoIntersection[4]).lower()  #lower() in modo che coincidano con i nomi delle variabili degli exchange definite in initialize_exchange()
    symbol1 = cryptoIntersection[0]
    symbol2 = cryptoIntersection[1]
    baseAsset = cryptoIntersection[2]
    price1 = eval(exchange1).get_price_pairs(symbol1)
    price2 = eval(exchange2).get_price_pairs(symbol2)
    if(price1 >= price2):
        percentages = (price1 - price2) / price2 * 100
        return {"percentage": percentages ,"startExchange": exchange2, "startSymbol": symbol2, "startPrice": price2, "endExchange": exchange1, "endSymbol": symbol1, "endPrice": price1}
    else:
        percentages = (price2 - price1) / price1 * 100
        return {"percentage": percentages ,"startExchange": exchange1, "startSymbol": symbol1, "startPrice": price1, "endExchange": exchange2, "endSymbol": symbol2, "endPrice": price2}
    #return tupla con percentuale, exchange di partenza, exchange di destinazione

def remove_sort_duplicates(percentages):
    seen = set()
    no_dup_list = []
    for d in percentages:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            no_dup_list.append(d)
    return sorted(no_dup_list, key=lambda k: k['percentage']) 

############################## FEE ########################################

def is_advantages(startAmount, endAmount):
    if startAmount >= endAmount:
        return False
    else:
        return True

def arbitrage_fee(startExchange, endExchange, pairStart, pairEnd, priceStart, priceEnd, setAmount, percentage, conn, cur):
    symbolStart = eval(startExchange).find_asset(pairStart)
    symbolEnd = eval(endExchange).find_asset(pairEnd)[0]
    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolStart +  "' AND exchange ='" + startExchange + "'")
    start = cur.fetchall()
    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolEnd +  "' AND exchange ='" + endExchange + "'")
    end = cur.fetchall()
    withdrawalFee = float(start[0][1]) #query
    depositFee = float(end[0][2])  #query
    takerStart = float(start[0][4])
    takerEnd = float(end[0][4])  #query
    startWithdrawal = float(setAmount - (setAmount * takerStart/100) - withdrawalFee)
    endWithdrawal = float(startWithdrawal - depositFee)
    sellCurr = float(endWithdrawal - endWithdrawal * takerEnd /100)
    startAmount = float(priceStart)*float(setAmount)
    endAmount = float(priceEnd)*sellCurr
    if is_advantages(startAmount, endAmount):
        percentage_fee = (endAmount - startAmount) / startAmount*100
        return {"startAmount": startAmount, "endAmount": endAmount, "percentage": percentage, "percentage_fee": percentage_fee ,"startExchange": startExchange, "startSymbol": pairStart, "startPrice": priceStart, "endExchange": endExchange, "endSymbol": pairEnd, "endPrice": priceEnd}
    else:
        -1

###########################################################################
    
binance, bitfinex, bittrex, poloniex, cex = initialize_exchanges()
conn, cur = open_db()
intersectionView = fetch_views_db(cur)
percentages = compute_percentages(intersectionView, cur)
orderded_nop_percentages = remove_sort_duplicates(percentages)

print('-----------------------------------------------------------------------------------------')
print(arbitrage_fee('binance', 'bittrex', 'LTCBTC', 'BTC-LTC', 0.015533, 0.01754890, 100, 13))


print('-----------------------------------------------------------------------------------------')

close_db(conn, cur)


