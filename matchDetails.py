#!/usr/bin/python3
import logging
import pymysql
import getSQLdata
import argparse, dispData, matchStats,playerTest2

logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of matchDetails.py')

cursor = getSQLdata.openDatabase()
logging.debug('Cursor value: ' + str(cursor))

parser = argparse.ArgumentParser(description='Run football team report')
parser.add_argument('-v','--verbose',
                    action='store_true',
                    help='increase output verbosity')

parser.add_argument('homeTeam',
                    help='Home Football Team')
                    
parser.add_argument('awayTeam', 
                    help='Away Football Team')

cursor = getSQLdata.openDatabase()

args = parser.parse_args()
if args.verbose:
    print("Verbosity turned on")
    
if args.homeTeam == '':
    print('Requires at least one team name')
    
homeCode = getSQLdata.findTeamCode(cursor,args.homeTeam)
if homeCode == '':
    print('Unable to find team code')
    
awayCode = getSQLdata.findTeamCode(cursor,args.awayTeam)
if awayCode == '':
    print('Unable to find team code')
    
print('Home Team Stats: ' + args.homeTeam)
# Average Home stats
results = getSQLdata.getHomeAvg(cursor,homeCode)
dispData.printRes(results,'Average','Home')
# Form from last 10 games
results = getSQLdata.getTeamForm(cursor,homeCode)
last10 = matchStats.getForm(cursor,(homeCode))
print('Position: ' + str(results[0]) + ' Form: ' + last10 + ' Division: ' + results[2])
# Favorite formations
formation = getSQLdata.getTeamFormations(cursor,homeCode)
if len(formation) > 0:
    print('Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
# Won against formation
formation = getSQLdata.getOppFormationsWhenWonAtHome(cursor,homeCode)
if len(formation) > 0:
    print('Won Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
# Drawn against formation
formation = getSQLdata.getOppFormationsWhenDrawnAtHome(cursor,homeCode)
if len(formation) > 0:
    print('Drawn Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
# Lost against formation
formation = getSQLdata.getOppFormationsWhenLostAtHome(cursor,homeCode)
if len(formation) > 0:
    print('Lost Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))

position = matchStats.findPosition(cursor, awayCode)
teamsAround = matchStats.getTeamsAround(cursor,position[0],position[1])
results = matchStats.findHomeResults(cursor,homeCode,teamsAround)
won = 0 
lost = 0
draw = 0
scored = 0
conceded = 0
for matchResult in results:
    if matchResult[1] == 'H':
        won += 1
    elif matchResult[1] == 'A':
        lost += 1
    else:
        draw += 1
    score = matchResult[0]    
    scored += int(score[1:2])
    conceded += int(score[3:4])
print('Teams played at home around away team position')    
print('Won: ' + str(won) + ' Drawn: ' +str(draw) + ' Lost: '+str(lost))
print('Scored: ' + str(scored) + ' Conceded: ' + str(conceded))
# Team Stats
playerTest2.teamSquad(homeCode)
    
# Number of home games
results = getSQLdata.countHomeGames(cursor,homeCode)
print('Total number of home games: ' + str(results[0]))
print()

print('Away Team Stats: ' + args.awayTeam)
# Average stats when playing away from home
results = getSQLdata.getAwayAvg(cursor,awayCode)
dispData.printRes(results,'Average','Away')
# Form from last 10 games
results = getSQLdata.getTeamForm(cursor,awayCode)
last10 = matchStats.getForm(cursor,(awayCode))
print('Position: ' + str(results[0]) + ' Form: ' + last10 + ' Division: ' + results[2])
# Favorite formations
formation = getSQLdata.getTeamFormations(cursor,awayCode)
if len(formation) > 0:
    print('Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
# Won against formation
formation = getSQLdata.getOppFormationsWhenWonAway(cursor,awayCode)
if len(formation) > 0:
    print('Won Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
# Drawn against formation
formation = getSQLdata.getOppFormationsWhenDrawnAway(cursor,awayCode)
if len(formation) > 0:
    print('Drawn Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
# Lost against formation
formation = getSQLdata.getOppFormationsWhenLostAway(cursor,awayCode)
if len(formation) > 0:
    print('Lost Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))

position = matchStats.findPosition(cursor, homeCode)
teamsAround = matchStats.getTeamsAround(cursor,position[0],position[1])
results = matchStats.findAwayResults(cursor,awayCode,teamsAround)
won = 0 
lost = 0
draw = 0
scored = 0
conceded = 0
for matchResult in results:
    if matchResult[1] == 'A':
        won += 1
    elif matchResult[1] == 'H':
        lost += 1
    else:
        draw += 1
    score = matchResult[0]    
    scored += int(score[3:4])
    conceded += int(score[1:2])
print('Teams played away around home team position')     
print('Won: ' + str(won) + ' Drawn: ' +str(draw) + ' Lost: '+str(lost))
print('Scored: ' + str(scored) + ' Conceded: ' + str(conceded))
# Team Stats
playerTest2.teamSquad(awayCode)
# Number of games played away from home
results = getSQLdata.countAwayGames(cursor,awayCode)
print('Total number of away games: ' + str(results[0]))

