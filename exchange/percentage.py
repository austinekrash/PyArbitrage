import sys
import json
import requests
import psycopg2
from binan import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from cex import Cex
from poloni import Poloniex

E_BINANCEapiKey = 'WXYox2eh9V8fUiLvjdW9f8xkh3q30EpzxGaeLQvxMZ0TTUyDSaIJliEmAXr2NtYN'
E_BINANCEsecretKey = 'qbXdJU82w1QKpjHe6OFRMdJMxbZgQuHigLRzssDqf3TCpEaxyAaHyrGolDQzbrbD'

E_BITTREXapiKey = 'd94bf4036b9841729f2d5100ee9132a4'
E_BITTREXsecretKey = '672e4f9fea3b4628b1bf5617fbdb22be'

E_POLONIEXapiKey = '8QF9DS6A-YJWQQLWW-ZKUM8YV8-YJ5HG70E'
E_POLONIEXsecretKey = '6dd1afa15f71fe6c77bb0fd9348058f9d45deb99d0e9c5aed2752f974919f5b381db5f5e458c558e720805a1d840f56064253cce64a4c84fc0b05ad8f51d8ecc'

#Api ale

A_BITTREXapiKey = 'fe357e0ca4bd4cdebd37d06e3773c33f '
A_BITTREXsecretKey = '9d9c8ebb584d40ffb5dfca4ada0bbf63'

A_POLONIEXapiKey = '74DRDEIV-2G9W6KXO-QK6FY8Z9-LP1CAT98'
A_POLONIEXsecretKey = '16962e88b0e3349e2f774d6eb5dd5bde54a59bcd120c637e0e2cca5dbb0f77d93379416ab4e6dbc4fe9116007a548913b1f7815fb306484e14fc4df6c3c23486'

A_BITFINEXapiKey = 'SxBHFSegUgIjDXCKCJSbGRPAxmGdgNCVFRStoVkLaaD'
A_BITFINEXsecretKey = '7Ud65qmtjg1lFA4j1u8e5tu3CeU4bL2V4Ni79an6B0P'

def costum_print(text):
        print('[PERCENTAGE] '+str(text))   

def open_db():
    try:
        conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='localhost' password='pippo'")
    except:
        costum_print("I am unable to connect to the database")
        sys.exit(1)
    cur = conn.cursor()
    return conn, cur

def fetch_views_db(cur):
    intersectionView = []
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'VIEW'")
    records = cur.fetchall()
    for x in records:
        if 'cex' not in str(x[0]):
            print(x)
            intersectionView.append(x[0]) # faccio una lista con tutte le view contenenti le intersezioni tra exchange
    return intersectionView

def close_db(conn, cur):
    conn.close()
    cur.close()
    costum_print("DB successfully closed")


def initialize_exchanges():
    binance = Binance.Factory(E_BINANCEapiKey, E_BINANCEsecretKey)
    bitfinex = Bitfinex.Factory(A_BITFINEXapiKey, A_BITFINEXsecretKey)
    bittrex = Bittrex.Factory(A_BITTREXapiKey,A_BITTREXsecretKey)
    poloniex = Poloniex.Factory(A_POLONIEXapiKey, A_POLONIEXsecretKey)
    cex = Cex.Factory() # Sarà da togliere
    binance.sync()
    bitfinex.sync()
    bittrex.sync()
    poloniex.sync()
    cex.sync()
    return binance, bitfinex, bittrex, poloniex, cex

def compute_percentages(intersectionView, cur):
    percentages = []
    #per ogni exchange prendo la lista delle crypto
    for view in intersectionView:
        cur.execute("SELECT * FROM "+view)
        cryptoIntersection = []
        for x in cur.fetchall():#prendo tutte le tuple per ogni view
            cryptoIntersection.append(x)
            percentages.append(__percentage(x))            
            #chiamo api prezzo su symbol
            #inserisco in percentages la coppia o tripla symbol std_symbol percentuale
            #non ha senso prendere anche il prezzo, perchè il prezzo va preso subito prima della vednita/Acquisto
    return percentages

def __percentage(cryptoIntersection):
    exchange1 = (cryptoIntersection[3]).lower()
    exchange2 = (cryptoIntersection[4]).lower()  #lower() in modo che coincidano con i nomi delle variabili degli exchange definite in initialize_exchange()
    symbol1 = cryptoIntersection[0]
    symbol2 = cryptoIntersection[1]
    baseAsset = cryptoIntersection[2]
    price1 = eval(exchange1).get_price_pairs(symbol1)
    price2 = eval(exchange2).get_price_pairs(symbol2)
    if price1 >= price2 and price2 > 0:
        percentages = (price1 - price2) / price2 * 100
        return {"percentage": percentages ,"startExchange": exchange2, "startSymbol": symbol2, "startPrice": price2, "endExchange": exchange1, "endSymbol": symbol1, "endPrice": price1}
    elif price2 >= price1 and price1 > 0:
        percentages = (price2 - price1) / price1 * 100
        return {"percentage": percentages ,"startExchange": exchange1, "startSymbol": symbol1, "startPrice": price1, "endExchange": exchange2, "endSymbol": symbol2, "endPrice": price2}
    #return tupla con percentuale, exchange di partenza, exchange di destinazione

def remove_sort_duplicates(percentages):
    """seen = set()
    no_dup_list = []
    for d in percentages:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            no_dup_list.append(d)"""
    return sorted(percentages, key=lambda k: k['percentage'], reverse=True) 

############################## FEE ########################################

def is_advantages(startAmount, endAmount):
    if startAmount >= endAmount:
        return False
    else:
        return True

def arbitrage_fee(startExchange, endExchange, pairStart, pairEnd, priceStart, priceEnd, balanceAmount, percentage, cur, amountExchange, symbolAmount):
    cryptoTaxi = 'XLM' #crypto scelta per muoversi tra exchange
    #TODO bisogna scegliere e settare la lista delle monete da usare per lo spostamento, poi generalizzare questa quyery
    symbolStart = eval(startExchange).find_asset(pairStart)[0]
    symbolEnd = eval(endExchange).find_asset(pairEnd)[0]
    if symbolStart != symbolEnd:
        print(symbolStart)
        print(symbolEnd)
        print("NOT EQUALS")
        return -2
    
    #query per dati su start end e fee
    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolStart +  "' AND exchange ='" + startExchange + "'")
    start = cur.fetchall()
    if not start:
        cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolStart +  "' AND exchange ='" + endExchange + "'")
        start = cur.fetchall()
    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolEnd +  "' AND exchange ='" + endExchange + "'")
    end = cur.fetchall()
    if not end:
        cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolEnd +  "' AND exchange ='" + startExchange + "'")
        end = cur.fetchall()
    if not symbolAmount:
        cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolAmount +  "' AND exchange ='" + amountExchange + "'")
        am = cur.fetchall()
    if not start and not end and not symbolAmount:
        print('both start and end and amount are None!!')
        return -3
    
    #Fee amount of withdrawal and buy/sell on start
    startWithdrawalFee = float(start[0][1])
    takerStart = float(start[0][4])
    startDepositFee = float(start[0][2]) 
    #Fee amount of withdrawal and buy/sell on end
    endDepositFee = float(end[0][2]) 
    takerEnd = float(end[0][4]) 
    #Fee amount of withdrawal and buy/sell on end
    amWithdrawalFee = float(am[0][1])
    takerAm = float(am[0][4])

    firstWithdrawalFee = 0#fee del withdrawal dall'exchangeamount all'exchangeamount
    firstFee = 0#fee sul buy/sell sull'exchange amount

    feeStart = 0 #fee dovute al buy/sell della crypto su start
    sw = 0 #fee del withdrawal da startexchange a endexchange
    feeEnd = 0##fee dovute al buy/sell della crypto su start

    #controllo se exchange di partenza = a quello in cui si trova il balance.
    if startExchange == amountExchange:
        sw = startWithdrawalFee + endDepositFee
        feeEnd =takerEnd/100
        #se coincidono controllo se il symbol coincide con quello dell'arbitraggio (symbolstart)
        if symbolStart != symbolAmount:
            #se coincidono allora non pago il taker sullo start
            #se non coincidono pago il taker
            feeStart = balanceAmount * takerStart/100
    #se non coincidono
    else:
        #in questo caso comunque pago il taker su exchangestart
        #in questo caso considero che quando arrivo sul nuovo exchange la moneta non coincida con quella dell'arbitraggio
        #quindi pago sia il withdrawal dal primo al seconod exchange che il taker sul primo
        sw = startWithdrawalFee + endDepositFee
        feeStart = balanceAmount * takerStart/100
        firstWithdrawalFee = amWithdrawalFee + startDepositFee
        feeEnd = takerEnd/100
        #controllo se la moneta coincide con quella utilizzata per spostarsi
        if symbolAmount != cryptoTaxi:
            firstFee = balanceAmount * takerAm/100
            #se coincide non pago taker su exchangeamount
        #NON HO ANCORA CONSIDERATO LE FEE TAKER SU EXCHANGE END. 
        #QUELLE LE CALCOLO FUORI DAGLI IF


    #computing fee on balance
    #startWithdrawal = float(balanceAmount - (balanceAmount * takerStart/100) - withdrawalFee - firstWithdrawalFee)
    goToStart = float(balanceAmount - (balanceAmount * firstFee + firstWithdrawalFee))
    start = float(goToStart - (feeStart * goToStart + sw))
    #endWithdrawal = float(startWithdrawal - depositFee)
    end = float(start- (start * takerEnd / 100))
    #sellCurr = float(endWithdrawal - endWithdrawal * takerEnd /100)

    #Price at start and at the end of arbitrage
    startAmount = float(priceStart) * float(goToStart)
    endAmount = float(priceEnd) * float(end)

    #calcolo solo se non freezato e vantaggioso
    if is_advantages(startAmount, endAmount) and eval(startExchange).is_frozen(symbolStart)['withdrawal'] and eval(endExchange).is_frozen(symbolEnd)['deposit']:
        percentage_fee = (endAmount - startAmount) / startAmount*100
        return {"startAmount": startAmount, "endAmount": endAmount, "percentage": percentage, "percentage_fee": percentage_fee ,"startExchange": startExchange, "startSymbol": pairStart, "startPrice": priceStart, "endExchange": endExchange, "endSymbol": pairEnd, "endPrice": priceEnd}
    else:
        return -1
    
    #def __return_fee(startExchange, endExchange, amountExchange, ):

    def where_i_am():
        binance.get_balances()
        poloniex.get_balances()
        bittrex.get_balances()
        binance.get_balances()
        binance.sync()
        bitfinex.sync()
        bittrex.sync()
        poloniex.sync()
        cex.sync()
        max = [None, 0, None]
        #binance
        balBin = binance.get_balances().get('balances')
        for index in range(len(balBin)):
            if float(balBin[index].get('free')) >= max[1]:
                max[1] = float(balBin[index].get('free'))
                max[0] = balBin[index].get('asset')
                max[2] = 'binance'
        #poloniex
        balPolo = poloniex.get_available_account_balances()
        for key, value in balPolo['exchange'].items():
            if value >= max[1]:
                max[1] = value
                max[0] = key
                max[2] = 'poloniex'
        #bittrex
        balBit = bittrex.get_balances()
        if balBit['success'] == 'true':
            for i in range(len(balBit['result'])):
                if balBit['result'][i]['Balance'] >= max[1]:
                    max[1] = balBit['result'][i]['Balance']
                    max[0] = balBit['result'][i]['Currency']
                    max[2] = 'bittrex'
        #bitfinex
        balBitfi = bitfinex.get_balances()
        for i in range(len(balBitfi)):
            if float(balBitfi[i]['amount']) >= max[1]:
                max[0] = balBitfi[i]['currency']
                max[1] = float(balBitfi[i]['amount'])
                max[2] = 'bitfinex'
        
        return max
        


###########################################################################
    
binance, bitfinex, bittrex, poloniex, cex = initialize_exchanges()
conn, cur = open_db()
intersectionView = fetch_views_db(cur)
percentages = compute_percentages(intersectionView, cur)
#orderded_nop_percentages = remove_sort_duplicates(percentages)
print(type(percentages[0]['percentage']))
orderded_nop_percentages = sorted(percentages)#sorted(percentages, key=lambda k: k['percentage'], reverse=True) 
print(orderded_nop_percentages)



for perc in orderded_nop_percentages:
    print(perc)
    

print('-----------------------------------------------------------------------------------------')
fee_list = []
i = 0
for item in orderded_nop_percentages:
    print(item['startExchange']+" "+item['endExchange']+" "+item['startSymbol']+" "+item['endSymbol']+" "+str(item['startPrice'])+" "+str(item['endPrice'])+" "+str(100)+" "+str(item['percentage']))
    res = arbitrage_fee(item['startExchange'], item['endExchange'], item['startSymbol'], item['endSymbol'], float(item['startPrice']), float(item['endPrice']), 300, float(item['percentage']), cur, 'binance', 'BTC')
    if  not isinstance(res , int):
        print(res)

print('-----------------------------------------------------------------------------------------')
print('------------------------------ '+str(i)+" len"+str(len(orderded_nop_percentages)))
#fee_sorted = sorted(fee_list, key=lambda k: k['percentage_fee'], reverse=True) 
#for item in fee_sorted:
#    print(item)
    
close_db(conn, cur)
