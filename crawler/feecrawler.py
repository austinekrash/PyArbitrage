import requests
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def get_record_coin(url_info, driver):
    driver.get(url_info)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, ".//tbody")))

    if( '()' in driver.title):
        print("Scraping ended")
        return -1

    crypto = driver.title.split('withdrawal fees - FeeXplorer')[0]
    name = crypto.split(' ')[0]
    symbol = crypto.split('(')[1].split(')')[0]

    tbody = driver.find_elements_by_xpath('.//tbody')
    exchanges_list = []
    if(len(tbody) != 1):
        raise Exception("Too many tbody found!!")
    print(symbol)
    rows = tbody[0].find_elements_by_xpath('.//tr')
    for row in rows:
        cols = row.find_elements_by_xpath('.//td')
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
        exchanges_list.append([exchange_name, min_withdrawal, withdrawal, deposit, maker, taker])
    return [name, symbol, exchanges_list]

id_crypto = 1
driver = webdriver.Firefox()
record_list = []
while True:
    url_info = 'https://www.feexplorer.io/coin/'+str(id_crypto)+'/'
    record = get_record_coin(url_info, driver)
    record_list.append(record)
    if(record is -1):
        break
    id_crypto = id_crypto + 1
driver.quit()
print(record_list)
#Exchange, Min-with, with, (espresso in coin corrente) deposit, maker, taker (ultimi due in percentuale)