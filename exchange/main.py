from cex import Cex
from binance import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from poloniex import Poloniex

'''
cex = Cex.Factory()
cex.sync()
cex.get_price_pairs('ETH/BTC')

binance = Binance.Factory()
binance.sync()
binance.get_price_pairs('ETHBTC')

bitfinex = Bitfinex.Factory()
bitfinex.sync()
bitfinex.get_price_pairs('ETHBTC')
'''

bittrex = Bittrex.Factory()
bittrex.sync()
bittrex.get_price_pairs('BTC-GRIN')
bittrex.get_deposit_address('BTC')
bittrex.get_balances('BTC')

'''
poloniex = Poloniex.Factory()
poloniex.sync()
poloniex.get_price_pairs('BTC_BCN')
'''