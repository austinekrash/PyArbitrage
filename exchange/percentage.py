import sys
import json
import requests
import psycopg2
from binan import Binance
from bitfinex import Bitfinex
from bittrex import Bittrex
from cex import Cex
from poloni import Poloniex

E_BINANCEapiKey = 'key'
E_BINANCEsecretKey = 'key'

E_BITTREXapiKey = 'key'
E_BITTREXsecretKey = 'key'

E_POLONIEXapiKey = 'key'
E_POLONIEXsecretKey = 'key'

#Api ale

A_BITTREXapiKey = 'key '
A_BITTREXsecretKey = 'key'

A_POLONIEXapiKey = 'key'
A_POLONIEXsecretKey = 'key'

A_BITFINEXapiKey = 'key'
A_BITFINEXsecretKey = 'key'

def costum_print(text):
        print('[PERCENTAGE] '+str(text))   

def open_db():
    try:
        conn = psycopg2.connect("dbname='' user='' host='' password=''")
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
        for x in cur.fetchall():#prendo tutte le tuple per ogni view
            y = __percentage(x)
            if y != 0:
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
    else:
        return 0
    #return tupla con percentuale, exchange di partenza, exchange di destinazione

def remove_sort_duplicates(percentages):
    seen = set()
    no_dup_list = []
    for d in percentages:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            no_dup_list.append(d)
    return sorted(no_dup_list, key=lambda k: k['percentage'], reverse=True) 

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
    am = 0
    amWithdrawalFee = 0
    takerAm = 0
    if symbolStart != symbolEnd:
        print(symbolStart)
        print(symbolEnd)
        print("NOT EQUALS")
        return -2
    
    #query per dati su start end e fee
    #Nel caso le fee non si rtrovano nell excahnge di partenza si prendpno da quello finale
    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolStart +  "' AND exchange ='" + startExchange + "'")
    start = cur.fetchall()
    if not start:
        cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolStart +  "' AND exchange ='" + endExchange + "'")
        start = cur.fetchall()
    if not start:
        cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolStart +  "' AND exchange ='" + amountExchange + "'")
        start = cur.fetchall()
        if not start:
            return -1
            
    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolEnd +  "' AND exchange ='" + endExchange + "'")
    end = cur.fetchall()
    if not end:
        cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolEnd +  "' AND exchange ='" + startExchange + "'")
        end = cur.fetchall()
    if not end:
        cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + symbolEnd +  "' AND exchange ='" + amountExchange + "'")
        end = cur.fetchall()
        if not end:
            return -1


    cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + cryptoTaxi +  "' AND exchange ='" + amountExchange + "'")
    am = cur.fetchall()
    if not am:
        cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + cryptoTaxi +  "' AND exchange ='" + endExchange + "'")
        am = cur.fetchall()
    if not am:
        cur.execute("SELECT min_widthdrawal, withdrawal, deposit, maker, taker FROM fee WHERE symbol = '" + cryptoTaxi +  "' AND exchange ='" + startExchange + "'")
        am = cur.fetchall()
        if not am:
            return -1
    
    #convertire amount in cryptotaxi
    #generare coppia
    #se amount è quote_asset generiamo coppia
    #sennò generi la coppia amountBTC poi btccryptotaxi
    doubleTaker = False
    cur.execute("SELECT * FROM "+ eval(amountExchange)._table +" WHERE base_asset = '"+symbolAmount+"' AND quote_asset = '"+cryptoTaxi+"'")#improbabile
    quote_taxi = cur.fetchall()
    if not quote_taxi:
        cur.execute("SELECT * FROM "+ eval(amountExchange)._table +" WHERE base_asset = '"+cryptoTaxi+"' AND quote_asset = '"+symbolAmount+"'")
        quote_taxi = cur.fetchall()
        if not quote_taxi:
            cur.execute("SELECT s1.quote_asset from (select distinct * from "+ eval(amountExchange)._table +" WHERE base_asset = '"+cryptoTaxi+"')s1 inner JOIN (SELECT distinct * from "+ eval(amountExchange)._table +" WHERE base_asset = '"+symbolAmount+"')s2 on s1.quote_asset = s2.quote_asset")
            quote_taxi = cur.fetchall()
            doubleTaker = True

    quote_asset = quote_taxi[0][0]
    symbol_std = ''
    for x in sorted([quote_asset.lower(), symbolAmount.lower()]):
        symbol_std = symbol_std + x

    cur.execute("SELECT symbol FROM "+eval(amountExchange)._table+" WHERE symbol_std = '"+symbol_std+"'")
    pair = cur.fetchall()[0][0]

    rate = eval(amountExchange).get_price_pairs(pair)#prezzo della coppia pair 
    #con i prezzi va sempre fatta la MOLTIPLICAZIONE
    amountExchange = amountExchange * rate

    symbol_std = ''
    for x in sorted([quote_asset.lower(), cryptoTaxi.lower()]):
        symbol_std = symbol_std + x
    if doubleTaker:
        cur.execute("SELECT symbol FROM "+eval(amountExchange)._table+" WHERE symbol_std = '"+symbol_std+"'")
        pair = cur.fetchall()[0][0]
        rate = eval(amountExchange).get_price_pairs(pair)#prezzo della coppia pair 
        #con i prezzi va sempre fatta la MOLTIPLICAZIONE
        amountExchange = amountExchange * rate
    #A questo punto siamo sull'exchange gisuto
    #TODO se doubleTaker = 1 aumenta le fee nella formula

    #TODO 

    amWithdrawalFee = float(am[0][1])
    takerAm = float(am[0][4])
    
    #print(startExchange + " " + endExchange + " " + pairStart)
    #Fee amount of withdrawal and buy/sell on start
    startWithdrawalFee = float(start[0][1])
    takerStart = float(start[0][4])
    startDepositFee = float(start[0][2]) 
    #Fee amount of withdrawal and buy/sell on end
    endDepositFee = float(end[0][2]) 
    takerEnd = float(end[0][4]) 
    #Fee amount of withdrawal and buy/sell on end

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
        feeStart = takerStart/100 #DA LEVARE COGLIONE
        firstWithdrawalFee = amWithdrawalFee + startDepositFee
        feeEnd = takerEnd/100
        #controllo se la moneta coincide con quella utilizzata per spostarsi
        if symbolAmount != cryptoTaxi:
            firstFee = takerAm / 100
            #se coincide non pago taker su exchangeamount
        #NON HO ANCORA CONSIDERATO LE FEE TAKER SU EXCHANGE END. 
        #QUELLE LE CALCOLO FUORI DAGLI IF


    #computing fee on balance
    #startWithdrawal = float(balanceAmount - (balanceAmount * takerStart/100) - withdrawalFee - firstWithdrawalFee)
    goToStart = float(balanceAmount - (balanceAmount * firstFee + firstWithdrawalFee))
    start = float(goToStart - (feeStart * goToStart + sw))
    #endWithdrawal = float(startWithdrawal - depositFee)
    end = float(start- (start * takerEnd))
    #sellCurr = float(endWithdrawal - endWithdrawal * takerEnd /100)

    #Price at start and at the end of arbitrage
    startAmount = float(priceStart) * float(goToStart)
    endAmount = float(priceEnd) * float(end)

    #calcolo solo se non freezato e vantaggioso
    #print({"startAmount": startAmount, "endAmount": endAmount, "percentage": percentage, "startExchange": startExchange, "startSymbol": pairStart, "startPrice": priceStart, "endExchange": endExchange, "endSymbol": pairEnd, "endPrice": priceEnd})

    if is_advantages(startAmount, endAmount) and not eval(startExchange).is_frozen(pairStart)['withdrawal'] and not eval(endExchange).is_frozen(pairEnd)['deposit']:
        percentage_fee = (endAmount - startAmount) / startAmount*100
        return {"startAmount": startAmount, "endAmount": endAmount, "percentage": percentage, "percentage_fee": percentage_fee ,"startExchange": startExchange, "startSymbol": pairStart, "startPrice": priceStart, "endExchange": endExchange, "endSymbol": pairEnd, "endPrice": priceEnd}
    else:
        percentage_fee = (endAmount - startAmount) / startAmount*100
        print('************************************************'+str({"startAmount": startAmount, "endAmount": endAmount, "percentage": percentage, "percentage_fee": percentage_fee ,"startExchange": startExchange, "startSymbol": pairStart, "startPrice": priceStart, "endExchange": endExchange, "endSymbol": pairEnd, "endPrice": priceEnd}))

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
orderded_nop_percentages = remove_sort_duplicates(percentages)


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
