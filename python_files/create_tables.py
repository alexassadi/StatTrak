from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
import functools as ft
import get_links
import input_data

def get_passing_combined(soup,league_id):

    url = league_links[0][team_choice]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    
    # Retrieve the table data from html text
    table = soup.find('table', id='stats_passing_{}'.format(league_id))
    
    # Retrieve the column names from the table
    headers = get_headers(table)
    
    # Modify headers
    headers = headers[8:37]
    headers[11] = 'Attt'
    headers[14] = 'Attt'
    headers[17] = 'Attt'

    # Create DataFrame with headers
    mydata = pd.DataFrame(columns = headers)
    print(mydata)

    # Retrieve stats from the table
    overall = get_stats(table)
    
    chunks = clean_data(overall,29,False)

    mydata = input_data(chunks,mydata)
    print(mydata)
    
    # Modify data and perform calculations
    mydata = mydata.astype({'90s':'float64','Att':'int','Ast':'int','xAG':'float64'})
    mydata['Att/90'] = mydata['Att'] / mydata['90s']
    mydata['Ast/90'] = mydata['Ast'] / mydata['90s']
    
    # Create final table
    mydata_final = mydata[['Player','90s','Ast','Att/90','Ast/90']] #'Att/90','Ast/90'

    return mydata_final