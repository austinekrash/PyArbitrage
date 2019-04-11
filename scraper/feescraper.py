import requests
import json
import psycopg2
import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options

def get_record_coin(url_info, driver):
    driver.get(url_info)
    WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, ".//tbody")))

    if('()' in driver.title):
        print("Scraping ended")
        return -1

    crypto = driver.title.split('withdrawal fees - FeeXplorer')[0]
    name = crypto.split(' ')[0]
    symbol = crypto.split('(')[1].split(')')[0]

    tbody = driver.find_elements_by_xpath('.//tbody')
    records_coin = []
    if(len(tbody) != 1):
        raise Exception("Too many tbody found!!")
    rows = tbody[0].find_elements_by_xpath('.//tr')
    for row in rows:
        cols = row.find_elements_by_xpath('.//td')
        if(len(cols) == 1):
            return -2
        exchange_name = cols[0].text
        div = cols[1].find_elements_by_xpath('.//div')
        if not div[0].get_attribute("data-tooltip"):
            min_withdrawal = 0
        else:
            min_withdrawal = div[0].get_attribute("data-tooltip").split('Minimum Withdrawal: ')[1]
        if('FREE' in div[0].text):
            withdrawal = 0
        else:
            withdrawal = div[0].text
        if('-' in cols[2].text):
            deposit = 0
        else:
            deposit = cols[2].text
        if('/' in cols[3].text):
            maker = cols[3].text.split('/')[0]
            taker = cols[3].text.split('/')[1]
        else:
            maker = taker = cols[3].text
        records_coin.append([symbol, exchange_name.lower(), name.lower(), float(min_withdrawal), float(withdrawal), float(deposit), float(maker), float(taker)])
    return records_coin

def insert_in_db(records, conn, cur):
    sql = """INSERT INTO fee(symbol, exchange, name_extend, min_widthdrawal, withdrawal, deposit, maker, taker) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT(symbol,exchange) DO NOTHING;"""
    cur.executemany(sql, records)
    conn.commit()

def connect_db():
    try:
        conn = psycopg2.connect("dbname='arbitraggio' user='ale' host='localhost' password='pippo'")
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()


def main():
    id_crypto = 905
    options = Options()  #Needed since no display
    options.headless = True
    conn, cur = connect_db()
    while True:
        driver = webdriver.Firefox(options=options)
        print(id_crypto)
        url_info = 'https://www.feexplorer.io/coin/'+str(id_crypto)+'/'
        records_coin = get_record_coin(url_info, driver)
        if(records_coin is -1):
            break
        if(records_coin is -2):
            id_crypto = id_crypto + 1
            continue
        insert_in_db(records_coin, conn, cur)
        id_crypto = id_crypto + 1
        driver.quit()
        os.system('pkill firefox')
    close_db(conn, cur)
    #Exchange, Min-with, with, (espresso in coin corrente) deposit, maker, taker (ultimi due in percentuale)

main()
