import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import os
import requests

def price():
    today = date.today()
    d = today - timedelta(days=1)
    url = ('https://api.bmreports.com/BMRS/DERSYSDATA/v1?APIKey=3pyyl4iymgrn812&FromSettlementDate=%s&ToSettlementDate=%s&SettlementPeriod=*&ServiceType=xml') %(d,today)
    r = requests.get(url, allow_redirects=True)
    open('price_elexon.xml', 'wb').write(r.content)

    # Open XML file
    file = open(os.getcwd() + r'/price_elexon.xml', 'r')
    
    # Read the contents of that file
    contents = file.read()
    
    soup = BeautifulSoup(contents, 'xml')
    
    # Extracting the data
    settlementDate = soup.find_all('settlementDate')
    settlementPeriod = soup.find_all('settlementPeriod')
    systemSellPrice = soup.find_all('systemSellPrice')

    data = []
    
    # Loop to store the data in a list named 'data'
    for i in range(0, len(systemSellPrice)):
        rows = [ settlementDate[i].get_text(), settlementPeriod[i].get_text(), systemSellPrice[i].get_text()]
        data.append(rows)
    
    # Converting the list into dataframe
    df = pd.DataFrame(data, columns=['settlementDate', 'settlementPeriod', 'systemSellPrice' ], dtype = float)
    df.rename(columns={ "settlementDate" : "date", "settlementPeriod" : "period", "systemSellPrice": "price" }, inplace = True)


    # os.remove(os.getcwd() + r'/price_elexon.xml')

    result = df.to_dict('records')
    return result