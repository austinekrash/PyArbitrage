import psycopg2
import requests
import json

intersectionView = []

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

#Ora per ogni exchange prendo la lista delle crypto

for view in intersectionView:
    cur.execute("SELECT * FROM "+view)
    cryptoIntersection = []
    for x in cur.fetchall():
        cryptoIntersection.append(x[0])
