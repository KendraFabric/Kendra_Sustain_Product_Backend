import pandas as pd
from bs4 import BeautifulSoup

import os
import requests

def fuel():
    url = ('https://api.bmreports.com/BMRS/FUELINST/v1?APIKey=3pyyl4iymgrn812&ServiceType=xml') 


    r = requests.get(url, allow_redirects=True)
    open('fuel_elexon.xml', 'wb').write(r.content)


    file = open(os.getcwd() + r'/fuel_elexon.xml', 'r')
    
    # Read the contents of that file
    contents = file.read()
    
    soup = BeautifulSoup(contents, 'xml')
    
    # Extracting the data
    publishingPeriodCommencingTime = soup.find_all('publishingPeriodCommencingTime')
    ccgt = soup.find_all('ccgt')
    coal = soup.find_all('coal')
    nuclear = soup.find_all('nuclear')
    npshyd = soup.find_all('npshyd') #hydro
    other = soup.find_all('other')

    data = []
    
    # Loop to store the data in a list named 'data'
    for i in range(0, len(other)):
        rows = [ publishingPeriodCommencingTime[i].get_text(), ccgt[i].get_text(), coal[i].get_text(), nuclear[i].get_text(), npshyd[i].get_text(), other[i].get_text() ]
        data.append(rows)
    
    # Converting the list into dataframe
    df = pd.DataFrame(data, columns=['publishingPeriodCommencingTime', 'ccgt', 'coal', 'nuclear', 'npshyd', 'other'], dtype = float)
    df.rename(columns={ "publishingPeriodCommencingTime" : "date", "ccgt" : "gas turbine", "npshyd" : "hydro" }, inplace = True)

    # os.remove(os.getcwd() + r'/fuel_elexon.xml')

    result = df.to_dict('records')
    return result