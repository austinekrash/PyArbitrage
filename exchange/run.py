from cex import Cex
from binan import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from poloni import Poloniex


E_BINANCEapiKey = 'key'
E_BINANCEsecretKey = 'key'

E_BITTREXapiKey = 'key'
E_BITTREXsecretKey = 'key'

E_POLONIEXapiKey = 'key'
E_POLONIEXsecretKey = 'key'


#Api ale
A_POLONIEXapiKey = 'key'
A_POLONIEXsecretKey = 'key'

A_BITFINEXapiKey = 'key'
A_BITFINEXsecretKey = 'key'

binance = Binance.Factory(E_BINANCEapiKey, E_BINANCEsecretKey)
bitfinex = Bitfinex.Factory(A_BITFINEXapiKey, A_BITFINEXsecretKey)
bittrex = Bittrex.Factory(E_BITTREXapiKey,E_BITTREXsecretKey)
poloniex = Poloniex.Factory(A_POLONIEXapiKey, A_POLONIEXsecretKey)
max = [None, 0]

cex = Cex.Factory() # Sarà da togliere
binance.sync()
bitfinex.sync()
bittrex.sync()
poloniex.sync()
cex.sync()

print(binance.is_frozen('ADABTC'))








