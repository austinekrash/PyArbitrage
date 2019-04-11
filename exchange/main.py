import psycopg2
from cex import Cex
from binan import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
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

def is_advantages(startAmount, endAmount):
    if startAmount >= endAmount:
        return False
    else:
        return True


def arbitrage_fee(startExchange, endExchange, symbolStart, symbolEnd, priceStart, priceEnd, startAmount):
    #SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee  WHERE symbol = 'BTC' AND exchange = 'binance'
    try:
        conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='51.15.122.155' password='pippo'")
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee")
    start = cur.fetchall()
    #cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee  WHERE symbol = " + symbolEnd +  "AND exchange =" + endExchange)
    #end = cur.fetchall()
    print(start)
    withdrawalFee = 0 #query
    depositFee = 0 #query
    taker = 0 #query
    startWithdrawal = startAmount - withdrawalFee
    endWithdrawal = startWithdrawal - depositFee
    sellCurr = endWithdrawal - endWithdrawal * taker


#arbitrage_fee('bitfinex', 'binance', 'BTC', 'BTC', '1', '1', '10')

binance = Binance.Factory(E_BINANCEapiKey, E_BINANCEsecretKey)
bitfinex = Bitfinex.Factory(A_BITFINEXapiKey, A_BITFINEXsecretKey)
bittrex = Bittrex.Factory(E_BITTREXapiKey,E_BITTREXsecretKey)
poloniex = Poloniex.Factory(A_POLONIEXapiKey, A_POLONIEXsecretKey)
binance.sync()
bittrex.sync()
poloniex.sync()
bitfinex.sync()

bittrex.get_price_pairs('BTC-POWR')
binance.get_price_pairs('POWRBTC')
poloniex.get_price_pairs('BTC_BCN')
bitfinex.get_price_pairs('tABSETH')