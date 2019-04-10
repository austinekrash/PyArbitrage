from cex import Cex
from binan import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from poloni import Poloniex


BINANCEapiKey = 'WXYox2eh9V8fUiLvjdW9f8xkh3q30EpzxGaeLQvxMZ0TTUyDSaIJliEmAXr2NtYN'
BINANCEsecretKey = 'qbXdJU82w1QKpjHe6OFRMdJMxbZgQuHigLRzssDqf3TCpEaxyAaHyrGolDQzbrbD'

def is_advantages(startAmount, endAmount):
    if startAmount >= endAmount:
        return False
    else:
        return True


def arbitrage_fee(startExchange, endExchange, symbolStart, symbolEnd, priceStart, priceEnd, startAmount):

    global conn
    #SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee  WHERE symbol = 'BTC' AND exchange = 'binance'
    cur = conn.cursor()

    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee  WHERE symbol = " + symbolStart +  "AND exchange =" + startExchange)
    start = cur.fetchall()

    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee  WHERE symbol = " + symbolEnd +  "AND exchange =" + endExchange)
    end = cur.fetchall()
    print(start)
    withdrawalFee = 0 #query
    depositFee = 0 #query
    taker = 0 #query
    startWithdrawal = startAmount - withdrawalFee
    endWithdrawal = startWithdrawal - depositFee
    sellCurr = endWithdrawal - endWithdrawal * taker

try:
    conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='localhost' password='pippo'")
except:
    print("I am unable to connect to the database")
arbitrage_fee('bitfinex', 'binance', 'BTC', 'BTC', '1', '1', '10')


POLONIEXapiKey = '8QF9DS6A-YJWQQLWW-ZKUM8YV8-YJ5HG70E'
pOLONIEXsecretKey = '6dd1afa15f71fe6c77bb0fd9348058f9d45deb99d0e9c5aed2752f974919f5b381db5f5e458c558e720805a1d840f56064253cce64a4c84fc0b05ad8f51d8ecc'


'''
p = Poloniex.Factory()
print(p.return_fee_info())
#print(p.return_deposit_address())
#polo = Poloniex()



cex = Cex.Factory()
cex.sync()
cex.get_price_pairs('ETH/BTC')

binance = Binance.Factory(BINANCEapiKey, BINANCEsecretKey)
binance.sync()
binance.get_deposit_address('PAX')
binance.get_balance('XRP')
binance.get_balances()
print(binance.is_frozen('BTC'))

bitfinex = Bitfinex.Factory()
bitfinex.sync()
bitfinex.get_price_pairs('ETHBTC')

bittrex = Bittrex.Factory()
bittrex.sync()
#bittrex.get_price_pairs('BTC-GRIN')
bittrex.get_deposit_address('BTC')
#bittrex.get_balances()
#bittrex.get_open_orders('BTC-GRIN')
bittrex = Bittrex.Factory()
bittrex.sync()
bittrex.get_price_pairs('BTC-GRIN')
bittrex.getDepositAddress('test')

bitfinex = Bitfinex().Factory()
bitfinex.get_address('BTC')

poloniex = Poloniex.Factory()
poloniex.sync()
poloniex.get_price_pairs('BTC_BCN')
'''