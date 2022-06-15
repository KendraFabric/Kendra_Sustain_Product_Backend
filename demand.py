import pandas as pd
from bs4 import BeautifulSoup
import os
import requests

def demand():
    url = ('https://api.bmreports.com/BMRS/ROLSYSDEM/v1?APIKey=3pyyl4iymgrn812&ServiceType=xml') 

    r = requests.get(url, allow_redirects=True)
    open('demand_elexon.xml', 'wb').write(r.content)

    # Open XML file
    file = open(os.getcwd() + r'/demand_elexon.xml', 'r')
    
    # Read the contents of that file
    contents = file.read()
    
    soup = BeautifulSoup(contents, 'xml')
    
    # Extracting the data
    settDate = soup.find_all('settDate')
    publishingPeriodCommencingTime = soup.find_all('publishingPeriodCommencingTime')
    fuelTypeGeneration = soup.find_all('fuelTypeGeneration')

    data = []
    
    # Loop to store the data in a list named 'data'
    for i in range(0, len(fuelTypeGeneration)):
        rows = [ settDate[i].get_text(), publishingPeriodCommencingTime[i].get_text(), fuelTypeGeneration[i].get_text()]
        data.append(rows)
    
    # Converting the list into dataframe
    df = pd.DataFrame(data, columns=['settDate', 'publishingPeriodCommencingTime', 
                                    'fuelTypeGeneration' ], dtype = float)
    df.rename(columns={ "publishingPeriodCommencingTime" : "Time", "settDate" : "Date", "fuelTypeGeneration": "Demand" }, inplace = True)
    df['Time'] = df['Time'].apply(lambda x: x[:5])
    # os.remove(os.getcwd() + r'/demand_elexon.xml')
    result = df.to_dict('records')
    return result
    

    # print(df)