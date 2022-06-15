import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import os
import requests

def transmit():
    today = date.today()
    d = today - timedelta(days=30)

    url = ('https://api.bmreports.com/BMRS/DEVINDOD/v1?APIKey=3pyyl4iymgrn812&FromDate=%s&ToDate=%s&ServiceType=xml') %(d,today)
    r = requests.get(url, allow_redirects=True)
    open('transmit_elexon.xml', 'wb').write(r.content)

    file = open(os.getcwd() + r'/transmit_elexon.xml', 'r')
    
    # Read the contents of that file
    contents = file.read()
    
    soup = BeautifulSoup(contents, 'xml')
    
    # Extracting the data
    settlementDay = soup.find_all('settlementDay')
    volume = soup.find_all('volume')


    data = []
    
    # Loop to store the data in a list named 'data'
    for i in range(0, len(volume)):
        rows = [ settlementDay[i].get_text(), volume[i].get_text() ]
        data.append(rows)
    
    # Converting the list into dataframe
    df = pd.DataFrame(data, columns=['settlementDay', 'volume'], dtype = float)
    df.rename(columns={ "settlementDay" : "date", "volume" : "volume" }, inplace = True)


    # os.remove(os.getcwd() + r'/transmit_elexon.xml')


    result = df.to_dict('records')
    return result