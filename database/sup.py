def find_asset(symbol):
    #return base and quote asset
    if(symbol[:4].lower()  == 'usdt'):
        return [symbol[5:], 'usdt']
    elif(symbol[:3].lower()  == 'btc'):
        return [symbol[4:], 'btc']
    elif(symbol[:3].lower()  == 'eth'):
        return [symbol[4:], 'eth']
    elif(symbol[:3].lower()  == 'usd'):
        return [symbol[4:], 'usd']