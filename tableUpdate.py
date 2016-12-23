from bs4 import BeautifulSoup
import logging
import urllib.request,getSQLdata
import argparse

def fillTableData(page_data,table):
    for team in page_data.find_all('tr',{'class':'team'}):
        teamName = team.find('td',{'class':'team-name'}).get_text()
        tableData.setdefault(teamName,{'position':0,'teamCode':' ','played':0,
                                 'won':0,'drawn':0,'lost':0,
                                 'goalsFor':0,'goalsAgainst':0,
                                 'goalDifference':0,'points':0,'lastTen':' ','table':' '})
        tableData[teamName]['position'] = int(team.find('span',{'class':'position-number'}).get_text())
        tableData[teamName]['teamCode'] = getSQLdata.findTeamCode(cursor,teamName)
        tableData[teamName]['played'] = int(team.find('td',{'class':'played'}).get_text())
        tableData[teamName]['won'] = int(team.find('td',{'class':'won'}).get_text())
        tableData[teamName]['drawn'] = int(team.find('td',{'class':'drawn'}).get_text())
        tableData[teamName]['lost'] = int(team.find('td',{'class':'lost'}).get_text())
        tableData[teamName]['goalsFor'] = int(team.find('td',{'class':'for'}).get_text())
        tableData[teamName]['goalsAgainst'] = int(team.find('td',{'class':'against'}).get_text())
        tableData[teamName]['goalDifference'] = int(team.find('td',{'class':'goal-difference'}).get_text())
        tableData[teamName]['points'] = int(team.find('td',{'class':'points'}).get_text())
        lastTen = ''
        for form in team.find_all('li'):
            result = form.find('span').get_text()
            if result == 'Win':
                lastTen += 'W'
            elif result == 'Loss':
                lastTen += 'L'
            else:
                lastTen += 'D'
        tableData[teamName]['lastTen'] = lastTen
        tableData[teamName]['table'] = table


domain_page = 'http://www.bbc.co.uk/sport/football'
sub_page_prem = '/premier-league/table'
sub_page_champ = '/championship/table'
sub_page_L1 = '/league-one/table'
sub_page_L2 = '/league-two/table'
cursor = getSQLdata.openDatabase()
logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
page = urllib.request.urlopen(domain_page + sub_page_prem)
soup = BeautifulSoup(page, 'html.parser') 
tableData = {}

logging.debug('Premiership table update')  
for page_text in soup.find_all('table',{"data-competition-slug":"premier-league"}):
    fillTableData(page_text,'PL')
 
logging.debug('Championship table update')     
page = urllib.request.urlopen(domain_page + sub_page_champ)
soup = BeautifulSoup(page, 'html.parser')
for page_text in soup.find_all('table',{"data-competition-slug":"championship"}):
    fillTableData(page_text,'CH')

logging.debug('League One table update')  
page = urllib.request.urlopen(domain_page + sub_page_L1)
soup = BeautifulSoup(page, 'html.parser') 
for page_text in soup.find_all('table',{"data-competition-slug":"league-one"}):
    fillTableData(page_text,'L1')

logging.debug('League Two table update')  
page = urllib.request.urlopen(domain_page + sub_page_L2)
soup = BeautifulSoup(page, 'html.parser') 
for page_text in soup.find_all('table',{"data-competition-slug":"league-two"}):
    fillTableData(page_text,'L2')
    
getSQLdata.createTable(cursor, tableData)
cursor = getSQLdata.closeDatabase(cursor)