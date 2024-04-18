from collections.abc import Iterable
import pandas as pd
from bs4 import BeautifulSoup
import requests
import lxml
import datetime

get_player_links(league_choice, team_choice):
    prem_link = get_league_id(league_choice)
    league_links, league_link = get_league_links(league_choice)
    url = league_links[team_choice]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table', id='stats_standard_9')
    links = []
    for i in table.find_all('a'):
        html = i.get('href')
        if 'player' in html:
            links.append(html)
    links_new = []
    for i in links:
        if 'Match-Logs' in i:
            link = 'https://fbref.com' + i
            links_new.append(link)
    names = []
    for i in links_new:
        split = i.split('/')
        split2 = split[9].split('-')
        name = []
        for j in split2:
            if not j in ['Match','Logs']:
                name.append(j)
        names.append(' '.join(name))
    player_dict = dict(zip(names, links_new))
    return player_dict

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