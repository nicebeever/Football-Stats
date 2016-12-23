#!/usr/bin/python3
import getSQLdata, logging
import argparse, dispData
import logging,re
import urllib.request
from bs4 import BeautifulSoup
#from players import Player


def createPlayer(playerNum,details):
    name = details[0]
    team = details[1]
    goals = details[2]
    red = details[3]
    yellow = details[4]
    subs = details[5]
    point = details[6]
    starts = details[7]
    pos = details[8]
    playerNum = Player(name,team,goals,red,yellow,subs,point,starts,pos)
    logging.debug('createPlayer: ' + playerNum.getName())


logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of dispTeam.py')

domain_page = 'http://www.skysports.com'
linksRegEx = re.compile('<a[^>]* href="([^"]*)"')

parser = argparse.ArgumentParser(description='Run football team report')
parser.add_argument('-v','--verbose',
                    action='store_true',
                    help='increase output verbosity')

parser.add_argument('team',
                    help='Football Team')
                    
args = parser.parse_args()

player = ''

if args.verbose:
    print("Verbosity turned on")
    
if args.team == '':
    print('Requires a team name')
    
squad = args.team
squad = squad.replace(' ', '-')
squad = '/' + squad.lower() + '-squad'
cursor = getSQLdata.openDatabase()
logging.debug('Cursor value: ' + str(cursor))
    
team = getSQLdata.findTeamCode(cursor,args.team)
if team == '':
    print('Unable to find team code')
    
print('Team Stats: ' + args.team)

page = urllib.request.urlopen(domain_page + squad)

soup = BeautifulSoup(page, 'html.parser')
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
    
print(playerList)
cursor = getSQLdata.openDatabase()
teamCode = getSQLdata.findTeamCode(cursor, team)
oppositionCode = getSQLdata.findTeamCode(cursor, opposition)
if getSQLdata.countMatchDaySquad(cursor, teamCode, oppositionCode, date)[0] < 1:
    getSQLdata.updateMatchDaySquad(cursor, playerList, teamCode, oppositionCode, formation, date)
    

    

