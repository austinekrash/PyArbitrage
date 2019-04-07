import requests
import json

#https://www.feexplorer.io/search.php?q=Ripple

id_crypto = 2
info_exchange = requests.get('https://www.feexplorer.io/list.php?&id_crypto='+str(id_crypto)+'&id_exchange=undefined')
p = json.loads(info_exchange.content)
a = p['data']
info_page = requests.get('https://www.feexplorer.io/coin/'+str(id_crypto)+'/')
crypto = info_page.text.split('<title>')[1].split('withdrawal fees - FeeXplorer')[0]
name = crypto.split(' ')[0]
symbol = crypto.split('(')[1].split(')')[0]
print(crypto)
print(name)
print(symbol)
print(len(a))
for index in range(len(a)):
    print(str(a[index][0])+'\n') #Minimum Withdraw
    name_exchange = a[index][0].split("alt='")[1].split("'")[0]
    print(name_exchange)
    print(str(a[index][1])+'\n')
    if("Minimum Withdrawal:" in a[index][1]):
        min_widthdrawl = a[index][1].split('Minimum Withdrawal:')[1].split("'>")[0]
        print("min_with: "+min_widthdrawl)
    else:
        min_widthdrawl = '-'
    withdrawal = a[index][1].split('>')[1].split("<")[0]
    print("withdrawal: "+withdrawal)
    print(str(a[index][2])+'\n')  #Deposit
    deposit = a[index][2]
    print("deposit: "+deposit)
    print(str(a[index][3])+'\n')  #Trade maker/Trader
    if("/" in a[index][3]):
        print("Maker&Trader differs")
        maker = a[index][3].split('/')[0]
        trader =a[index][3].split('/')[1]
        
    else:
        maker = trader = a[index][3]
    print("maker: "+maker)
    print("trader: "+trader)
    print('----------------------------------------------------------------')