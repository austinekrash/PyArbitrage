import psycopg2
from cex import Cex
from binan import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from poloni import Poloniex


E_BINANCEapiKey = 'WXYox2eh9V8fUiLvjdW9f8xkh3q30EpzxGaeLQvxMZ0TTUyDSaIJliEmAXr2NtYN'
E_BINANCEsecretKey = 'qbXdJU82w1QKpjHe6OFRMdJMxbZgQuHigLRzssDqf3TCpEaxyAaHyrGolDQzbrbD'


E_POLONIEXapiKey = '8QF9DS6A-YJWQQLWW-ZKUM8YV8-YJ5HG70E'
E_POLONIEXsecretKey = '6dd1afa15f71fe6c77bb0fd9348058f9d45deb99d0e9c5aed2752f974919f5b381db5f5e458c558e720805a1d840f56064253cce64a4c84fc0b05ad8f51d8ecc'


#Api ale
A_POLONIEXapiKey = '74DRDEIV-2G9W6KXO-QK6FY8Z9-LP1CAT98'
A_POLONIEXsecretKey = '16962e88b0e3349e2f774d6eb5dd5bde54a59bcd120c637e0e2cca5dbb0f77d93379416ab4e6dbc4fe9116007a548913b1f7815fb306484e14fc4df6c3c23486'

A_BITFINEXapiKey = 'SxBHFSegUgIjDXCKCJSbGRPAxmGdgNCVFRStoVkLaaD'
A_BITFINEXsecretKey = '7Ud65qmtjg1lFA4j1u8e5tu3CeU4bL2V4Ni79an6B0P'

A_BITTREXapiKey = '04ad577f17d24106939e1dca8c4fe20f'
A_BITTREXsecretKey = '347996b130214a71bfe8c000c48e9fda'

def is_advantages(startAmount, endAmount):
    if startAmount >= endAmount:
        return False
    else:
        return True


#arbitrage_fee('bitfinex', 'binance', 'BTC', 'BTC', '1', '1', '10')


'''
bitfinex = Bitfinex.Factory(BITFINEXapiKey,BITFINEXsecretKey)
bitfinex.sync()
#bitfinex.get_price_pairs('tAGIUSD')
#print(bitfinex.get_deposit_address('santiment')) #Oocio
#bitfinex.withdraw()# test
#bitfinex.get_balance('btc')  #“trading”, “deposit” or “exchange”
bitfinex.get_withdraw_fee('btc')
'''
'''
binance = Binance.Factory(E_BINANCEapiKey, E_BINANCEsecretKey)
binance.sync()
bitfinex = Bitfinex.Factory(A_BITFINEXapiKey, A_BITFINEXsecretKey)
bitfinex.sync()
cex = Cex().Factory()
cex.sync()
poloniex = Poloniex.Factory(A_POLONIEXapiKey,A_POLONIEXsecretKey)
poloniex.sync()
'''
'''
poloniex = Poloniex.Factory(A_POLONIEXapiKey,A_POLONIEXsecretKey)
poloniex.sync()
print(poloniex.get_deposit_address('XRP'))
'''
bittrex = Bittrex.Factory(A_BITTREXapiKey, A_BITTREXsecretKey)
bittrex.sync()
#bittrex.get_deposit_address('XRP')
#print(bittrex.get_deposit_address('ETH'))
print(bittrex.is_frozen('BTC-TX'))
print(bittrex.is_frozen('BTC-ETH'))

#print(arbitrage_fee('poloniex', 'bitfinex', 'BTC_REP', 'tREPBTC', 0.00350197, 0.0035394, 100, 13))
#print(poloniex.get_deposit_address('XRP'))
#poloniex.get_open_orders()

#print(p.return_deposit_address())
#polo = Poloniex()


"""
cex = Cex.Factory()
cex.sync()
cex.get_price_pairs('ETH/BTC')

binance = Binance.Factory(BINANCEapiKey, BINANCEsecretKey)
binance.sync()
bittrex.sync()
poloniex.sync()
bitfinex.sync()

bittrex.get_price_pairs('BTC-POWR')
binance.get_price_pairs('POWRBTC')
poloniex.get_price_pairs('BTC_BCN')
bitfinex.get_price_pairs('tABSETH')
"""