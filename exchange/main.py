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
binance.get_records() #Works
binance.get_price_pairs(0)
binance.close()

bitfinex = Bitfinex.Factory()
bitfinex.get_records() #Works
bitfinex.get_price_pairs(2)
bitfinex.close()

bittrex = Bittrex.Factory()
bittrex.get_records() #Works
bittrex.get_price_pairs(0)
bittrex.close()

poloniex = Poloniex.Factory()
poloniex.get_records() #Works
poloniex.get_price_pairs(0)
poloniex.close()

