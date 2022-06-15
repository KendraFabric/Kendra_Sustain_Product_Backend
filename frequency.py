import pandas as pd
from bs4 import BeautifulSoup
import os
import requests

def frequency():
    url = 'https://api.bmreports.com/BMRS/FREQ/v1?APIKey=3pyyl4iymgrn812&ServiceType=xml'
    r = requests.get(url, allow_redirects=True)
    open('freq_elexon.xml', 'wb').write(r.content)


    # Open XML file
    file = open(os.getcwd() + r'/freq_elexon.xml', 'r')
    
    # Read the contents of that file
    contents = file.read()
    
    soup = BeautifulSoup(contents, 'xml')
    
    # Extracting the data
    reportSnapshotTime = soup.find_all('reportSnapshotTime')
    spotTime = soup.find_all('spotTime')
    frequency = soup.find_all('frequency')

    data = []
    
    # Loop to store the data in a list named 'data'
    for i in range(0, len(frequency)):
        rows = [ reportSnapshotTime[i].get_text(), spotTime[i].get_text(), frequency[i].get_text()]
        data.append(rows)
    
    # Converting the list into dataframe
    df = pd.DataFrame(data, columns=['reportSnapshotTime', 'spotTime', 
                                    'frequency' ], dtype = float)
    df.rename(columns={ "reportSnapshotTime" : "date", "spotTime" : "time", "frequency": "frequency" }, inplace = True)

    # os.remove(os.getcwd() + r'/freq_elexon.xml')

    result = df.to_dict('records')
    return result