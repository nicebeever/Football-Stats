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
    allPlayers = soup.find_all('li',{"class":"tp"})
    for player in allPlayers:
        playerLink = player.find('a').get('href')
        pos = playerLink.rfind('/')
        pos2 = len(playerLink)
        name = playerLink.replace('-', ' ')
        name = name.title()
        name = name[pos+1:pos2]
        print(name)
        name = name.upper().replace(' ','')
        print(name)
        playerList.append(name)
    
    teamCode = getSQLdata.findTeamCode(cur, team)
#    oppositionCode = getSQLdata.findTeamCode(cur, opposition)
 #   if getSQLdata.countMatchDaySquad(cur, teamCode, oppositionCode, date)[0] < 1:
  #      getSQLdata.updateMatchDaySquad(cur, playerList, teamCode, oppositionCode, formation, date)

def findplayerDetails(divs, position, team):
    try:    
        trs = divs.find_all('tr',{'class':'text-h6 -center'})
        for tr in divs.find_all('tr',{'class':'text-h6 -center'}):
            tag = tr.find_all('td')
            for id , tg in enumerate(tr.find_all('td')):
                if id == 0:
                    name = (tg.find('h6').get_text().strip())
                    Code = name.replace("  "," ")
                    Code = Code.upper().replace(' ','')
                    playerStats.setdefault(name,{'team':team,'apperances':0,'subs':0,'goals':0,
                                 'yellowCards':0,'redCards':0,'fantasyScore':0,
                                 'position':position,'Code':Code})
                elif id == 1:
                    gamesPlayed = digitsRegEx.findall(tg.get_text().strip())
                    if len(gamesPlayed) > 0:
                        playerStats[name]['apperances'] = gamesPlayed[0]
                        playerStats[name]['subs'] = gamesPlayed[1]
                elif id == 2:
                    goals = digitsRegEx.findall(tg.get_text())
                    if len(goals) > 0:
                        playerStats[name]['goals'] = goals[0]
                elif id == 3:
                    yellow = digitsRegEx.findall(tg.get_text())
                    if len(yellow) > 0:
                        playerStats[name]['yellowCards'] = yellow[0]
                elif id == 4:
                    red = digitsRegEx.findall(tg.get_text())
                    if len(red) > 0:
                        playerStats[name]['redCards'] = red[0]
                elif id == 5:
                    points = digitsRegEx.findall(tg.get_text())
                    if len(points) > 0:
                         playerStats[name]['fantasyScore'] = points[0]
    except:
        pass
         
team_links = {'brighton':'brighton-and-hove-albion','wolverhampton':'wolverhampton-wanderers',
               'doncaster':'doncaster-rovers','stevenage':'stevenage-borough'}

domain_page = 'http://www.skysports.com'
sub_page = '/football/teams'
logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
cursor = getSQLdata.openDatabase()
page = urllib.request.urlopen(domain_page + sub_page)
soup = BeautifulSoup(page, 'html.parser')

positionRegEx = re.compile(r'Position: .+')
nameRegEx = re.compile(r'Name: .+')
linksRegEx = re.compile('<a[^>]* href="([^"]*)"')
                    
#leagues = ['P','C','1','2']
leagues =['C']
for league in leagues:

    links = soup.find_all('optgroup',{'label':'Premier League'})
    if league == 'C':
        links = soup.find_all('optgroup',{'label':'Championship'})
    if league == '1':
        links = soup.find_all('optgroup',{'label':'League One'})
    if league == '2':
        links = soup.find_all('optgroup',{'label':'League Two'})
    logging.debug('updatePlayer looking links')

    teamRegEx = re.compile(r'"/[A-Za-z ]+')
    teams = links[0].get_text()

    teamNames = teamRegEx.findall(teams) 

    #links = teams.lower().replace(' ','-').split()
    links='huddersfield'

    logging.debug('updatePlayer looping around teams')

    for link in links:
        team = link.replace('-',' ').title()
        if link in team_links:
            link = team_links[link]
     #   squad = '/' + link + '-squad'
        squad ='/huddersfield-town-squad'
        
        logging.debug('Looking for squad page: ' + squad)
        page = urllib.request.urlopen(domain_page + squad)
        dupPage = urllib.request.urlopen(domain_page + squad)
        updateMatchSquad(cursor,dupPage)
        soup = BeautifulSoup(page, 'html.parser')
        digitsRegEx = re.compile(r'[0-9]+')
        playerStats = {}
        logging.debug('playerStats for team: ' + team)
        
        teamCode = getSQLdata.findTeamCode(cursor, team)

        divs = soup.find('table',{'title':'Goalkeeper'})
        findplayerDetails(divs, "Goalkeeper", teamCode)
        
        divs = soup.find('table',{'title':'Defender'})
        findplayerDetails(divs, "Defender", teamCode)

        divs = soup.find('table',{'title':'Midfielder'})
        findplayerDetails(divs, "Midfielder", teamCode)

        divs = soup.find('table',{'title':'Attacking Midfielder'})
        findplayerDetails(divs, "Attacking Midfielder", teamCode)

        divs = soup.find('table',{'title':'Striker'})
        findplayerDetails(divs, "Striker", teamCode)
                
        for player in playerStats:
            if getSQLdata.countPlayerData (cursor,player,playerStats[player]['team']) > 0:              
                getSQLdata.updatePlayerData(cursor,player,playerStats[player])
            else:
                getSQLdata.writePlayerData (cursor,player,playerStats[player])    