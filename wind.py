import requests
from datetime import datetime, timedelta, date
import pandas as pd
from bs4 import BeautifulSoup
import os

def wind():
    today = date.today()
    d2 = today - timedelta(days=1)
    url = 'https://api.bmreports.com/BMRS/B1440/v1?APIKey=3pyyl4iymgrn812&SettlementDate=%s&Period=*&ServiceType=xml' %(d2)
    r = requests.get(url, allow_redirects=True)
    open('wind.xml', 'wb').write(r.content)


    # Open XML file
    file = open(os.getcwd() + r'/wind.xml', 'r')
    
    # Read the contents of that file
    contents = file.read()
    
    soup = BeautifulSoup(contents, 'xml')
    
    # Extracting the data
    businessType = soup.find_all('businessType')
    powerSystemResourceType = soup.find_all('powerSystemResourceType')
    settlementDate = soup.find_all('settlementDate')
    settlementPeriod = soup.find_all('settlementPeriod')
    quantity = soup.find_all('quantity')

    data = []

    # Loop to store the data in a list named 'data'
    for i in range(0, len(quantity)):
        rows = [ businessType[i].get_text(), powerSystemResourceType[i].get_text(), settlementDate[i].get_text(), settlementPeriod[i].get_text(), quantity[i].get_text()]
        data.append(rows)
    
    # Converting the list into dataframe
    df = pd.DataFrame(data, columns=['businessType', 'powerSystemResourceType', 'settlementDate' , 'settlementPeriod', 'quantity'
                                    'settlementDate' ], dtype = float)
    df.rename(columns={ "powerSystemResourceType" : "wind_type", "businessType" : "type", "settlementDate": "date", "settlementPeriod": "period", "quantity" : "quantity" }, inplace = True)

    df = df.replace(['\"','\"'], ['',''], regex=True)

    for i in range(df.shape[0]): 
        if i%3 == 0:
                    df = df.drop([i], axis = 0)
    df.rename(columns={ "quantitysettlementDate" : "Energy Value" }, inplace = True)
    df.drop(['type'] , inplace=True, axis=1)
    #@df.to_csv('wind1.csv', encoding='utf-8', index=False)

    # os.remove(os.getcwd() + r'/wind.xml')

    result = df.to_dict('records')
    return result