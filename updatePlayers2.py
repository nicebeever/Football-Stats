#!/usr/bin/python3

from bs4 import BeautifulSoup
import logging,re
import urllib.request,getSQLdata

def updateMatchSquad(cur,dupPage):
    soup = BeautifulSoup(dupPage, 'html.parser')
    formation = soup.find('div', class_="span10 strap1 -center -ondark -interact text-h5 arrangement").get_text()
    lastGame = soup.find('div', class_="col span1/1 text-s -center").get_text()
    pos = lastGame.find(' on ')
    date = lastGame[pos + 4:]
    lastGame = lastGame[22:pos]
    pos = lastGame.find (' vs ')
    team = lastGame[:pos]
    opposition = lastGame [pos+4:]
    playerList = []
    allPlayers = soup.find_all('li', class_="tp")
    for player in allPlayers:
        name = player.find('a').get('href')
        pos = name.rfind('/') + 1
        name=name[pos:]
        name=name.upper().replace('-',' ')
        name=name.replace('  ','').replace(' ','')
        print(name)
        name = linksRegEx.search(str(player))
        name = str(name)
        pos = name.rfind('/')
        pos2 = name.rfind('"')
        if name.find('"') == pos2:
            pos2 = len(name) - 1
        name = name.replace('-', ' ')
        name = name.title()
        name = name[pos+1:pos2]
        name = name.upper().replace(' ','')
        playerList.append(name)

domain_page = 'http://www.skysports.com'
sub_page = '/football/teams'
logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
cursor = getSQLdata.openDatabase()
page = urllib.request.urlopen(domain_page + sub_page)
soup = BeautifulSoup(page, 'html.parser')

digitsRegEx = re.compile(r'[0-9]+')

positionRegEx = re.compile(r'Position: .+')
nameRegEx = re.compile(r'Name: .+')
linksRegEx = re.compile('<a[^>]* href="([^"]*)"')

links = soup.find_all('optgroup',{'label':'Premier League'})

for link in links:
    teamRegEx = re.compile(r'"/[a-z-]+')
    teams = teamRegEx.findall(str(link)) 
    teamsRegEx = re.compile(r'/[a-z-]+')
    
    teams = teamsRegEx.findall(str(teams)) 
    
logging.debug('updatePlayer looping around teams')
saveTeam = ' '
 
squad = '/sheffield-united-squad'
team = 'SHEUTD'
    
page = urllib.request.urlopen(domain_page + squad)
dupPage = urllib.request.urlopen(domain_page + squad)
updateMatchSquad(cursor,dupPage)
soup = BeautifulSoup(page, 'html.parser')
    
playerStats = {}
links = []
            
divs = soup.find('table',{'title':'Goalkeeper'})
findplayerDetails(divs, "Goalkeeper", team)

divs = soup.find('table',{'title':'Defender'})
findplayerDetails(divs, "Defender", team)

divs = soup.find('table',{'title':'Midfielder'})
findplayerDetails(divs, "Midfielder", team)

divs = soup.find('table',{'title':'Attacking Midfielder'})
findplayerDetails(divs, "Attacking Midfielder", team)

divs = soup.find('table',{'title':'Striker'})
findplayerDetails(divs, "Striker", team)