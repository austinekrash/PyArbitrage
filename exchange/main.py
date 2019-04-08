from cex import Cex
from binance import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from poloniex import Poloniex

cex = Cex.Factory()
cex.get_records() #Works
cex.get_price_pairs(0)
cex.close()

binance = Binance.Factory()
binance.get_price_pairs(0)

bitfinex = Bitfinex.Factory()
bitfinex.get_price_pairs(2)

bittrex = Bittrex.Factory()
bittrex.get_price_pairs(0)

poloniex = Poloniex.Factory()
poloniex.get_price_pairs(0)

