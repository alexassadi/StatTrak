from collections.abc import Iterable
import pandas as pd
from bs4 import BeautifulSoup
import requests
import lxml

league_links = {'Premier League':'/9/Premier-League-Stats',
                'La Liga':'/12/La-Liga-Stats',
                'Serie A':'/11/Serie-A-Stats',
                'Ligue 1':'/13/Ligue-1-Stats',
                'Bundesliga':'/20/Bundesliga-Stats'}

table_names = {'Premier League':'results2022-202391_overall',
                'La Liga':'results2022-2023121_overall',
                'Serie A':'results2022-2023111_overall',
                'Ligue 1':'results2022-2023131_overall',
                'Bundesliga':'results2022-2023201_overall'}

def get_league_id(choice):
    if choice == 'Premier League':
        return '9'
    elif choice == 'La Liga':
        return '12'
    elif choice == 'Serie A':
        return '11'
    elif choice == 'Ligue 1':
        return '13'
    elif choice == 'Bundesliga':
        return '20'

def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item

def get_headers(table):
    headers = []
    for i in table.find_all('th'):
        if 'col' in str(i):
            title = i.text
            headers.append(title)
    return headers
            
def get_stats(table):
    names = []
    stats = []
    
    body = table.find('tbody')
    
    for j in body.find_all('tr'):
        name = j.find('th')
        names.append(name.text)
        player = []
        for jj in j.find_all('td'):
            player.append(jj.text)
        stats.append(player)
            
    overall = list(zip(names,stats))
    return overall

def clean_data(overall,n):
    final = []
    for player in overall:
        for i in player:
            final.append(i)

    final = list(flatten(final))

    chunk = [final[x:x+n] for x in range(0, len(final), n)]
    
    chunks = []
    for i in chunk:
        if not '' in i:
            chunks.append(i)
        else:
            continue
    return chunks

def input_data(chunks,mydata):
    for i in chunks:
        length = len(mydata)
        mydata.loc[length] = i
    return mydata
             
def get_passing_combined(soup,league_id):
    
    # Retrieve the table data from html text
    table = soup.find('table', id='stats_passing_{}'.format(league_id))
    
    # Retrieve the column names from the table
    headers = get_headers(table)
    
    # Modify headers
    headers = headers[6:35]
    headers[11] = 'Attt'
    headers[14] = 'Attt'
    headers[17] = 'Attt'

    # Create DataFrame with headers
    mydata = pd.DataFrame(columns = headers)

    # Retrieve stats from the table
    overall = get_stats(table)
    
    chunks = clean_data(overall,29)     

    mydata = input_data(chunks,mydata)
    
    # Modify data and perform calculations
    mydata = mydata.astype({'90s':'float64','Att':'int','Ast':'int','xAG':'float64'})
    mydata['Att/90'] = mydata['Att'] / mydata['90s']
    mydata['Ast/90'] = mydata['Ast'] / mydata['90s']
    
    # Create final table
    mydata_final = mydata[['Player','90s','Ast','Att/90','Ast/90']]

    return mydata_final

def get_shooting_combined(soup,league_id):
    table = soup.find('table', id='stats_shooting_{}'.format(league_id))

    headers = get_headers(table)

    headers = headers[3:26]

    mydata = pd.DataFrame(columns=headers)

    overall = get_stats(table)

    chunks = clean_data(overall,23)

    mydata = input_data(chunks,mydata)

    mydata_final = mydata[['Player', '90s', 'Gls', 'Sh/90', 'SoT/90']]
    mydata_final = mydata_final.astype({'90s':'float64'})
    
    return mydata_final

def get_defensive_combined(soup,league_id):
    
    table = soup.find('table', id='stats_defense_{}'.format(league_id))
    
    headers = get_headers(table)

    headers = headers[5:27]
    headers[10] = 'Tkll'

    mydata = pd.DataFrame(columns = headers)

    overall = get_stats(table)

    chunks = clean_data(overall,22)

    mydata = input_data(chunks,mydata)

    mydata = mydata.astype({'90s':'float64','Tkl':'int'})

    mydata['Tkl/90'] = mydata['Tkl'] / mydata['90s']

    mydata_final = mydata[['Player','90s','Tkl/90']]
    
    return mydata_final

def get_league_basic(soup):
    table = soup.find('table', id='stats_squads_standard_for')
    table2 = soup.find('table', id='stats_squads_standard_against')
    
    headers = get_headers(table)
    headers = headers[6:]
    headers[22] = 'Gls/90'
    headers[23] = 'Ast/90'
    
    mydata = pd.DataFrame(columns = headers)
    mydata2 = pd.DataFrame(columns = headers)
    
    overall = get_stats(table)
    overall2 = get_stats(table2)
    
    chunks = clean_data(overall,32)
    chunks2 = clean_data(overall2,32)
    
    mydata = input_data(chunks,mydata)
    mydata2 = input_data(chunks2,mydata2)
    print(mydata.to_string())
    mydata_concat = pd.concat([mydata,mydata2])

    mydata_concat = mydata_concat.astype({'90s':'float64','CrdY':'int','CrdR':'int'})
    mydata_concat['CrdY/90'] = mydata_concat['CrdY'] / mydata_concat['90s']
    mydata_concat['CrdR/90'] = mydata_concat['CrdR'] / mydata_concat['90s']

    mydata_final = mydata_concat[['Squad','MP','Poss','CrdY/90','CrdR/90','Gls/90','Ast/90']]

    return mydata_final

def get_league_shooting(soup):
    table = soup.find('table', id='stats_squads_shooting_for')

    headers = get_headers(table)
    headers = headers[3:]
    headers[12] = 'FKS'
    
    mydata = pd.DataFrame(columns = headers)
    
    overall = get_stats(table)
    
    chunks = clean_data(overall,20)

    mydata = input_data(chunks,mydata)
    mydata = mydata.astype({'90s':'float64','FKS':'int'})
    
    mydata['FKS/90'] = mydata['FKS'] / mydata['90s']
    
    mydata_final = mydata[['Squad','Sh/90','SoT/90','FKS/90']]

    return mydata_final

def get_league_defensive(soup):
    table = soup.find('table', id='stats_squads_defense_for')

    headers = get_headers(table)
    headers = headers[5:]
    headers[8] = 'TKL'
    
    mydata = pd.DataFrame(columns = headers)
    
    overall = get_stats(table)
    
    chunks = clean_data(overall,19)

    mydata = input_data(chunks,mydata)
    
    mydata = mydata.astype({'90s':'float64','Tkl':'int'})
    
    mydata['Tkl/90'] = mydata['Tkl'] / mydata['90s']

    mydata_final = mydata[['Squad','Tkl/90']]

    return mydata_final

def get_league_passing_types(soup):
    table = soup.find('table', id='stats_squads_passing_types_for')

    headers = get_headers(table)
    headers = headers[4:]
    headers[6] = 'FKP'
    
    mydata = pd.DataFrame(columns = headers)
    
    overall = get_stats(table)
    
    chunks = clean_data(overall,18)

    mydata = input_data(chunks,mydata)
    
    mydata = mydata.astype({'90s':'float64','FKP':'int','TI':'int','CK':'int'})
    mydata['FKP/90'] = mydata['FKP'] / mydata['90s']
    mydata['TI/90'] = mydata['TI'] / mydata['90s']
    mydata['CK/90'] = mydata['CK'] / mydata['90s']
    
    mydata_final = mydata[['Squad','FKP/90','TI/90','CK/90']]

    return mydata_final

def get_league_misc(soup):
    table = soup.find('table', id='stats_squads_misc_for')

    headers = get_headers(table)
    headers = headers[3:]
    headers[6] = 'FKP'
    
    mydata = pd.DataFrame(columns = headers)
    
    overall = get_stats(table)
    
    chunks = clean_data(overall,19)

    mydata = input_data(chunks,mydata)
    
    mydata = mydata.astype({'90s':'float64','Off':'int'})
    mydata['Off/90'] = mydata['Off'] / mydata['90s']

    mydata_final = mydata[['Squad','Off/90']]

    return mydata_final

def get_league_links(choice):
    league_link = league_links[choice]
    table_name = table_names[choice]
    url = 'https://fbref.com/en/comps' + league_link
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', id=table_name)
    
    links = []
    for i in table.find_all('a'):
        html = i.get('href')
        if 'squads' in html:
            links.append(html)
            
    for i in range(len(links)):
        links[i] = 'https://fbref.com' + links[i]
        
    links
    
    teams = []
    for link in links:
        split = link.split('/')
        split = split[-1]
        split = split.split('-')
        split = split[:-1]
        team = (' ').join(split)
        teams.append(team)
    teams
    
    team_links = {}
    for i in range(len(teams)):
        team_links[teams[i]] = links[i]
    team_links
    return team_links, url