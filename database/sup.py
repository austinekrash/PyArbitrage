def find_asset_bittrex(symbol):
    #return base and quote asset
    if(symbol[:4].lower()  == 'usdt'):
        return [symbol[5:], 'usdt']
    elif(symbol[:3].lower()  == 'btc'):
        return [symbol[4:], 'btc']
    elif(symbol[:3].lower()  == 'eth'):
        return [symbol[4:], 'eth']
    elif(symbol[:3].lower()  == 'usd'):
        return [symbol[4:], 'usd']

def find_asset_bitfinex(symbol):
    #return base and quote asset
    if(symbol[-4:].lower()  == 'usdt'):
        return [symbol[1:-4], 'usdt']
    elif(symbol[-3:].lower()  == 'btc'):
        return [symbol[1:-3], 'btc']
    elif(symbol[-3:].lower()  == 'eth'):
        return [symbol[1:-3], 'eth']
    elif(symbol[-3:].lower()  == 'usd'):
        return [symbol[1:-3], 'usd']
    elif(symbol[-3:].lower()  == 'dai'):
        return [symbol[1:-3], 'dai']
    elif(symbol[-3:].lower()  == 'xlm'):
        return [symbol[1:-3], 'xlm']
    elif(symbol[-3:].lower()  == 'eos'):
        return [symbol[1:-3], 'eos']
    elif(symbol[-3:].lower()  == 'jpy'):
        return [symbol[1:-3], 'jpy']
    elif(symbol[-3:].lower()  == 'gbp'):
        return [symbol[1:-3], 'gbp']
    elif(symbol[-3:].lower()  == 'eur'):
        return [symbol[1:-3], 'eur']
    elif(symbol[1:4].lower()  == 'btc'):
        return [symbol[4:], 'btc']
    elif(symbol[1:4].lower()  == 'eth'):
        return [symbol[4:], 'eth']
    else:
        return ['', '']

def find_asset_poloniex(symbol):
    #return base and quote asset
    if(symbol[:4].lower()  == 'usdt'):
        return [symbol[5:], 'usdt']
    elif(symbol[:3].lower()  == 'btc'):
        return [symbol[4:], 'btc']
    elif(symbol[:3].lower()  == 'eth'):
        return [symbol[4:], 'eth']
    elif(symbol[:3].lower()  == 'xmr'):
        return [symbol[4:], 'xmr']
    elif(symbol[:4].lower()  == 'usdc'):
        return [symbol[5:], 'usdc']