import requests
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
#https://www.feexplorer.io/search.php?q=Ripple

id_crypto = 1
url_info = 'https://www.feexplorer.io/coin/'+str(id_crypto)+'/'

driver = webdriver.Firefox()
driver.get(url_info)
WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, ".//tbody")))
crypto = driver.title.split('withdrawal fees - FeeXplorer')[0]
name = crypto.split(' ')[0]
symbol = crypto.split('(')[1].split(')')[0]
print(crypto)
print(name)
print(symbol)
tbody = driver.find_elements_by_xpath('.//tbody')
if(len(tbody) != 1):
    raise Exception("Too many tbody found!!")
rows = tbody[0].find_elements_by_xpath('.//tr')
for row in rows:
    cols = row.find_elements_by_xpath('.//td')
    exchange_name = cols[0].text
    print("Exchange "+exchange_name)
    div = cols[1].find_elements_by_xpath('.//div')
    if not div[0].get_attribute("data-tooltip"):
        min_withdrawal = 0
    else:
        min_withdrawal = div[0].get_attribute("data-tooltip").split('Minimum Withdrawal: ')[1]
    print("Min_Withdrawal: "+str(min_withdrawal))
    if('FREE' in div[0].text):
        withdrawal = 0
    else:
        withdrawal = div[0].text
    print("Withdrawal "+str(withdrawal))
    if('-' in cols[2].text):
        deposit = 0
    else:
        deposit = cols[2].text
    print("Deposit "+str(deposit))
    if('/' in cols[3].text):
        maker = cols[3].text.split('/')[0]
        taker = cols[3].text.split('/')[1]
    else:
        maker = taker = cols[3].text
    print("Maker: "+maker)
    print("Taker: "+taker)
    print("--------------------")
driver.quit()