from cex import Cex
from binan import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from poloniex import Poloniex


BINANCEapiKey = 'WXYox2eh9V8fUiLvjdW9f8xkh3q30EpzxGaeLQvxMZ0TTUyDSaIJliEmAXr2NtYN'
BINANCEsecretKey = 'qbXdJU82w1QKpjHe6OFRMdJMxbZgQuHigLRzssDqf3TCpEaxyAaHyrGolDQzbrbD'

'''
cex = Cex.Factory()
cex.sync()
cex.get_price_pairs('ETH/BTC')
'''
binance = Binance.Factory(BINANCEapiKey, BINANCEsecretKey)
binance.sync()
binance.get_deposit_address('PAX')
binance.get_balance('XRP')
binance.get_balances()
print(binance.is_frozen('BTC'))

'''
bitfinex = Bitfinex.Factory()
bitfinex.sync()
bitfinex.get_price_pairs('ETHBTC')
'''
''''
bittrex = Bittrex.Factory()
bittrex.sync()
#bittrex.get_price_pairs('BTC-GRIN')
#bittrex.get_deposit_address('BTC')
bittrex.get_balances()
#bittrex.get_open_orders('BTC-GRIN')

poloniex = Poloniex.Factory()
poloniex.sync()
poloniex.get_price_pairs('BTC_BCN')
'''