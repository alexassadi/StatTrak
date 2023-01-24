from fb import *
from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
import functools as ft
import streamlit as st

st.write('''#Gambling is wrong''')

league_choice = st.selectbox(
    'Which league would you like to vew stats for?: ',
     league_links.keys())

league_id = get_league_id(league_choice)
team_links, league_link = get_league_links(league_choice)

format_choice = st.selectbox(
    'Would you like team or player stats?: ',
     ['Team','Player'])

if format_choice == 'Player':
    #choice = input("What team would you like the stats for?: ")
    choice = st.selectbox(
    'Which team would you like to look at?: ',
     team_links.keys())
    url = team_links[choice]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    final_combined = get_shooting_combined(soup,league_id).merge(get_passing_combined(soup,league_id), how='outer', on=['Player', '90s']).merge(get_defensive_combined(soup,league_id), how='outer', on=['Player','90s'])
    st.write(final_combined)
elif format_choice == 'Team':
    url = league_link
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    league_combined = get_league_basic(soup).merge(get_league_shooting(soup), how='outer', on='Squad').merge(get_league_defensive(soup), how='outer', on='Squad').merge(get_league_passing_types(soup), how='outer', on='Squad').merge(get_league_misc(soup), how='outer', on='Squad')
    league_combined['FK/90'] = league_combined['FKS/90'] + league_combined['FKP/90']
    league_combined = league_combined[['Squad','MP','Poss','Gls/90','Sh/90','SoT/90','FK/90','Tkl/90','TI/90','CK/90','Off/90','CrdY/90','CrdR/90']]
    teams_choice = []
    for team in league_combined['Squad']:
        if st.checkbox(team):
            teams_choice.append(team)
    if st.checkbox('All'):
        teams_choice = list(league_combined['Squad'])
    st.write(league_combined[league_combined['Squad'].isin(teams_choice)])
    '''
    else:
        teams_choice = select.split(', ')
        url = league_link
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        league_combined = get_league_basic(soup).merge(get_league_shooting(soup), how='outer', on='Squad').merge(get_league_defensive(soup), how='outer', on='Squad').merge(get_league_passing_types(soup), how='outer', on='Squad').merge(get_league_misc(soup), how='outer', on='Squad')
        league_combined['FK/90'] = league_combined['FKS/90'] + league_combined['FKP/90']
        league_combined = league_combined[['Squad','MP','Poss','Gls/90','Sh/90','SoT/90','FK/90','Tkl/90','TI/90','CK/90','Off/90','CrdY/90','CrdR/90']]
        print(league_combined[league_combined['Squad'].isin(teams_choice)].to_string())
        '''
