#!/usr/bin/python3
import urllib.request
from bs4 import BeautifulSoup
import follow, getSQLdata
import pymysql
import logging

def findTeamCode(cursor, team):
    try:
        result = getSQLdata.findTeamCode(cursor,team)
    except:
        result = ''
    return result

logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of report.py')

teamStats = {}
cursor = getSQLdata.openDatabase()
logging.debug('Cursor value: ' + str(cursor))

domain_page = 'http://www.bbc.co.uk'

leagues = ['P','C','1','2']
for league in leagues:
    print(league)
    results_page = '/sport/football/premier-league/results'
    if league == 'C':
        results_page = '/sport/football/championship/results'
    if league == '1':
        results_page = '/sport/football/league-one/results'
    if league == '2':
       results_page = '/sport/football/league-two/results'

    page = urllib.request.urlopen(domain_page + results_page)
    soup = BeautifulSoup(page, 'html.parser')
    homeTeam = soup.find('span',{'class':'team-home teams'})

    for matchDetails in soup.find_all('tr',{'class':'report'}):
        team = matchDetails.find('span',{'class':'team-home teams'}).get_text().strip()
        homeTeam = findTeamCode(cursor,team)
        
        score = matchDetails.find('abbr',{'title':'Score'}).get_text().strip()
        
        team = matchDetails.find('span',{'class':'team-away teams'}).get_text().strip()
        awayTeam = findTeamCode(cursor,team)

    # Now update the fixture table
        logging.debug('Home: ' + str(homeTeam) + ' Away: ' + str(awayTeam))
        matchCode = getSQLdata.setFixtures(cursor,homeTeam,awayTeam)
    
        if matchCode == '****':
            continue
        
        link = matchDetails.find('a',{'class':'report'})
        try:
            if 'href' in link.attrs:
                report_page = domain_page + link.attrs['href']
        except:
            report_page = ''
    
    # Have link so fill stats page
        if homeTeam is not '' and score is not '' and awayTeam is not '':
            statsData = follow.link(report_page)
            if statsData == '****':
                continue
            teamStats = follow.splitStatsData(homeTeam,awayTeam,statsData,matchCode,score)
            getSQLdata.setStats(cursor,teamStats,matchCode)
        
getSQLdata.closeDatabase(cursor)

logging.debug('End of program')