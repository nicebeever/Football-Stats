#!/usr/bin/python3
import logging, sys
import pymysql
import getSQLdata
import argparse, dispData, matchStats,playerTest2

logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of matchDetails2.py')

def getTeamStats(cursor,teamCode,oppCode):
    # Average Home stats
    results = getSQLdata.getHomeAvg(cursor,teamCode)
    dispData.printRes(results,'Average','Home')
    # Form from last 10 games
    results = getSQLdata.getTeamForm(cursor,teamCode)
    last10 = matchStats.getForm(cursor,(teamCode))
    print('Position: ' + str(results[0]) + ' Form: ' + last10 + ' Division: ' + results[2])
    # Favorite formations
    formation = getSQLdata.getTeamFormations(cursor,teamCode)
    if len(formation) > 0:
        print('Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
    # Won against formation
    formation = getSQLdata.getOppFormationsWhenWonAtHome(cursor,teamCode)
    if len(formation) > 0:
        print('Won Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
    # Drawn against formation
    formation = getSQLdata.getOppFormationsWhenDrawnAtHome(cursor,teamCode)
    if len(formation) > 0:
        print('Drawn Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
    # Lost against formation
    formation = getSQLdata.getOppFormationsWhenLostAtHome(cursor,teamCode)
    if len(formation) > 0:
        print('Lost Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))        

def positionResults(cursor,teamCode,oppCode,HorA):
    position = matchStats.findPosition(cursor, oppCode)
    teamsAround = matchStats.getTeamsAround(cursor,position[0],position[1])
    if HorA == 'H':
        results = matchStats.findHomeResults(cursor,teamCode,teamsAround)
    else:
        results = matchStats.findAwayResults(cursor,oppCode,teamsAround)
    homeWin = 0 
    awayWin = 0
    draw = 0
    homeScore = 0
    awayScore = 0
    for matchResult in results:
        if matchResult[1] == 'H':
            homeWin += 1
        elif matchResult[1] == 'A':
            awayWin += 1
        else:
            draw += 1
        score = matchResult[0]
        homeScore += int(score[1:2])
        awayScore += int(score[3:4])
    if HorA == 'H':
        print('Teams played at home around away team position')    
        print('Won: ' + str(homeWin) + ' Drawn: ' +str(draw) + ' Lost: '+str(awayWin))
        print('Scored: ' + str(homeScore) + ' Conceded: ' + str(awayScore))
    else:
        print('Teams played away around home team position')    
        print('Won: ' + str(awayWin) + ' Drawn: ' +str(draw) + ' Lost: '+str(homeWin))
        print('Scored: ' + str(awayScore) + ' Conceded: ' + str(homeScore))
        
# Team Stats

    if HorA == 'H':
        playerTest2.teamSquad(teamCode)
    else:
        playerTest2.teamSquad(oppCode)
    
# Number of home games
    results = getSQLdata.countHomeGames(cursor,teamCode)
    if HorA == 'H':
        print('Total number of home games: ' + str(results[0]))
    else:
        print('Total number of away games: ' + str(results[0]))
    print()


def getStats(homeTeam,awayTeam):
    logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
    logging.debug('Start of matchDetails2.py')
    cursor = getSQLdata.openDatabase()
    logging.debug('Cursor value: ' + str(cursor))
    sys.stdout = open("footballFile.txt","w")
    homeCode = getSQLdata.findTeamCode(cursor,homeTeam)
    if homeCode == '':
        print('Unable to find team code')
    awayCode = getSQLdata.findTeamCode(cursor,awayTeam)
    if awayCode == '':
        print('Unable to find team code')
    print('Home Team Stats: ' + homeTeam)
    getTeamStats(cursor,homeCode,awayCode)
    positionResults(cursor,homeCode,awayCode,'H')
    print('Away Team Stats: ' + awayTeam)
    getTeamStats(cursor,awayCode,homeCode)
    positionResults(cursor,homeCode,awayCode,'A')
    sys.stdout.close()
    
    return
#******************************************

# Old code maybe

#*******************************************






##    print('Away Team Stats: ' + awayTeam)
# Average stats when playing away from home
####    results = getSQLdata.getAwayAvg(cursor,awayCode)
##    dispData.printRes(results,'Average','Away')
# Form from last 10 games
##    results = getSQLdata.getTeamForm(cursor,awayCode)
##    last10 = matchStats.getForm(cursor,(awayCode))
##    print('Position: ' + str(results[0]) + ' Form: ' + last10 + ' Division: ' + results[2])
# Favorite formations
##    formation = getSQLdata.getTeamFormations(cursor,awayCode)
##    if len(formation) > 0:
##        print('Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
# Won against formation
##    formation = getSQLdata.getOppFormationsWhenWonAway(cursor,awayCode)
##    if len(formation) > 0:
##        print('Won Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
# Drawn against formation
##    formation = getSQLdata.getOppFormationsWhenDrawnAway(cursor,awayCode)
##    if len(formation) > 0:
##        print('Drawn Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))
# Lost against formation
##    formation = getSQLdata.getOppFormationsWhenLostAway(cursor,awayCode)
##    if len(formation) > 0:
##        print('Lost Against Formation: ' + formation[0][0] + ' Used: ' +str(formation[0][1]))

##    position = matchStats.findPosition(cursor, homeCode)
##    teamsAround = matchStats.getTeamsAround(cursor,position[0],position[1])
##    results = matchStats.findAwayResults(cursor,awayCode,teamsAround)
##    won = 0 
##    lost = 0
##    draw = 0
##    scored = 0
##    conceded = 0
##    for matchResult in results:
##        if matchResult[1] == 'A':
##            won += 1
##        elif matchResult[1] == 'H':
##            lost += 1
##        else:
####            draw += 1
##        score = matchResult[0]    
##        scored += int(score[3:4])
##        conceded += int(score[1:2])
##    print('Teams played away around home team position')     
##    print('Won: ' + str(won) + ' Drawn: ' +str(draw) + ' Lost: '+str(lost))
##    print('Scored: ' + str(scored) + ' Conceded: ' + str(conceded))
# Team Stats
##    playerTest2.teamSquad(awayCode)
# Number of games played away from home
####    results = getSQLdata.countAwayGames(cursor,awayCode)
##    print('Total number of away games: ' + str(results[0]))
