import psycopg2
import requests
import json

intersectionView = []
perc = []

try:
    conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='localhost' password='pippo'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'VIEW'")
records = cur.fetchall()

for x in records:
    intersectionView.append(x[0]) #faccio una lista con tutte le view contenenti le intersezioni tra exchange

print(intersectionView)

#per ogni exchange prendo la lista delle crypto
for view in intersectionView:
    cur.execute("SELECT * FROM "+view)
    cryptoIntersection = []
    symbol = []
    for x in cur.fetchall():#prendo tutte le tuple per ogni view
        cryptoIntersection.append(x)
        for i in cryptoIntersection:
            pass
            #chiamo api prezzo su symbol
            #inserisco in perc la coppia o tripla symbol std_symbol percentuale
            #non ha senso prendere anche il prezzo, perchè il prezzo va preso subito prima della vednita/Acquisto

"""
def percentage(crypto1, crypto2):
    price1# = price della tupla che gli viene passata
    price2# = price della tupla che gli viene passata
    if(price1 >= price 2):
        perc = (price1 - price2) / price2 * 100
    else:
        perc = (price2 - price1) / price1 * 100
    #return tupla con percentuale, exchange di partenza, exchange di destinazione
"""