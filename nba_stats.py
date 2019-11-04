# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:46:03 2019

@author: yiqi
"""
############# Script that performs web scraping #######################
from time import sleep
import requests
import pandas as pd

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' +
    'AppleWebKit/537.36 (KHTML, like Gecko) ' +
    'Chrome/61.0.3163.100 Safari/537.36'
)

REQUEST_HEADERS = {
    'user-agent': USER_AGENT,
}

NBA_URL = 'http://stats.nba.com/stats/teamgamelogs'
NBA_ID = '00'

NBA_SEASON_TYPES = {
    'regular': 'Regular Season',
    'playoffs': 'Playoffs',
    'preseason': 'Pre Season',
}

def scrape_teamgamelogs(season, season_type, sleep_for=None):
    """Process JSON from stats.nba.com teamgamelogs endpoint and return unformatted DataFrame."""
    if sleep_for:
        sleep(sleep_for)
    nba_params = {
        'LeagueID': NBA_ID,
        'Season': season,
        'SeasonType': season_type,
    }
    r = requests.get(
        NBA_URL,
        params=nba_params,
        headers=REQUEST_HEADERS,
        allow_redirects=True
    )
    r.raise_for_status()
    results = r.json()['resultSets'][0]
    headers = results['headers']
    rows = results['rowSet']
    return pd.DataFrame(rows, columns=headers)

# Spetify the seasons to scrape stats from
seasons = ['1996-97','1997-98','1999-00','2000-01','2001-02','2002-03','2003-04','2004-05','2005-06','2006-07','2007-08','2008-09','2009-10','2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17', '2017-18', '2018-19']
season_types = ['regular', 'playoffs']
i = 0
for season in seasons:
    for stype in season_types:
        df_cr = scrape_teamgamelogs(season, NBA_SEASON_TYPES[stype], sleep_for=None)
        if i == 0:
            df = df_cr
        else:
            df = pd.concat([df, df_cr], sort=False)
        i += 1

# Select the needed columns in df        
cols = [col for col in df.columns if '_RANK' not in col]
cols = [col for col in cols if '_PCT' not in col]
cols = [col for col in cols if col not in ['PLUS_MINUS', 'REB', 'BLKA', 'PFD']]
df = df[cols]

# Write dataframe to a csv file
df.to_csv('nba_stats_1996-2018.csv')

