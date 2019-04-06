from cex import Cex
from binance import Binance
from bitfinex import Bitfinex
from poloniex import Poloniex

'''
cex = Cex.Factory()
#cex.get_records() #Works
cex.get_price_pairs(0)
cex.close()
'''
'''
binance = Binance.Factory()
# binance.get_records() #Works
binance.get_price_pairs(0)
binance.close()
'''
poloniex = Poloniex.Factory()
#bitfinex.get_records() #Works
poloniex.get_price_pairs(2)
poloniex.close()