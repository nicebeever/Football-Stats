#!/usr/bin/python3
from bs4 import BeautifulSoup
import logging
import pymysql, getSQLdata, predictedResults
import dispData, matchStats, playerTest2
import urllib.request

logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of fixtureBetting.py')

domain_page = 'http://www.skysports.com'
logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

cursor = getSQLdata.openDatabase()
logging.debug('Cursor value: ' + str(cursor))

leagues = ['P','C','1','2']
for league in leagues:

    sub_page = '/premier-league-fixtures'
    if league == 'C':
        sub_page = '/championship-fixtures'
    if league == '1':
        sub_page = '/league-1-fixtures'
    if league == '2':
        sub_page = '/league-2-fixtures'
        
    page = urllib.request.urlopen(domain_page + sub_page)
    soup = BeautifulSoup(page, 'html.parser')
    
    for fixture in soup.find_all('div', {'class':'fixres__item'}):
        for num,team in enumerate(fixture.find_all('span',{'class':'swap-text__target'})):
            team = team.get_text()
            if num == 0:
                homeTeam = team
            elif num == 1:
                awayTeam = team
        print()
        print(homeTeam + ' v ' + awayTeam)
        
        
        predictedResults.predicted(homeTeam,awayTeam)