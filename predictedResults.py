#!/usr/bin/python3
import logging
import pymysql
import getSQLdata, playerTest
import argparse, dispData, matchStats,playerTest2
from players import Team,Player

def findHomeStats(cur, homeCode, home, playersHome):
    topTeamGoals = 0
    topTeamConceded = 0
          
    topPlayers = matchStats.getTopEleven(cur, homeCode)
    for topPlayer in topPlayers:
        name = topPlayer[0]
        try:
            topTeamGoals += playersHome[name].score 
            topTeamConceded += playersHome[name].conceded
        except:
            pass
    
    home.goals = topTeamGoals
    home.conceded = topTeamConceded
    
    lastTeamGoals = 0
    lastTeamConceded = 0
    lastMatch = matchStats.getLastMatch(cur, homeCode)
    if lastMatch[0] == homeCode:
        opposition = lastMatch[1]
    else:
        opposition = lastMatch[0]
    
    squad = matchStats.getLastEleven(cur, homeCode, opposition)

    for number in range (3, 14):
        name = squad[number]
        lastTeamGoals += playersHome[name].score 
        lastTeamConceded += playersHome[name].conceded

            
    home.goals = (home.goals + lastTeamGoals) / 2
    home.conceded = (home.conceded + lastTeamConceded) / 2
    
    return home
    
def findAwayStats(cur, awayCode, away, playersAway):
    topTeamGoals = 0
    topTeamConceded = 0
          
    topPlayers = matchStats.getTopEleven(cur, awayCode)
    for topPlayer in topPlayers:
        name = topPlayer[0]
        topTeamGoals += playersAway[name].score
        topTeamConceded += playersAway[name].conceded
    
    away.goals = topTeamGoals
    away.conceded = topTeamConceded
    
    lastTeamGoals = 0
    lastTeamConceded = 0
    lastMatch = matchStats.getLastMatch(cur, awayCode)
    if lastMatch[0] == awayCode:
        opposition = lastMatch[1]
    else:
        opposition = lastMatch[0]
    
    squad = matchStats.getLastEleven(cur, awayCode, opposition)

    for number in range (3, 14):
        name = squad[number]
        lastTeamGoals += playersAway[name].score
        lastTeamConceded += playersAway[name].conceded
    
    away.goals = (away.goals + lastTeamGoals) / 2
    away.conceded = (away.conceded + lastTeamConceded) / 2
    
    return away
    
def leaguePosition(league, pos):
    
    league = str(league)
    if league == 'PL':
        pos = pos
    elif league == 'CH':
        pos += 20
    elif league == 'L1':
        pos += 44
    elif league == 'L2':
        pos += 68
    else:
        pos += 92
        
    return pos
    
def predict(home,away):
    if home.goals > away.conceded:
        homeScore = away.conceded
    else:
        homeScore = home.goals
    if away.goals > home.conceded:
        awayScore = home.conceded
    else:
        awayScore = away.goals
        
    print ('Predicted score: {}-{}'.format(int(homeScore), int(awayScore)))
    if homeScore > awayScore:
        print('Home Win')
    elif homeScore < awayScore:
        print('Away Win')
    else:
        print('Draw')          

def predicted(homeTeam, awayTeam):

    cursor = getSQLdata.openDatabase()
    
    homeCode = getSQLdata.findTeamCode(cursor,homeTeam)
    awayCode = getSQLdata.findTeamCode(cursor,awayTeam)

    home = {}
    away = {}
    playersHome = {}
    playersAway = {}

    home = Team(homeTeam,0,0,0,0)
    away = Team(awayTeam,0,0,0,0)

    playersHome = playerTest.teamPlayers(homeCode)
    playersAway = playerTest.teamPlayers(awayCode)

    home = findHomeStats(cursor, homeCode, home, playersHome)
    away = findAwayStats(cursor, awayCode, away, playersAway)

# Give home side a half goal advantage and away side half goal disadvantage
    home.goals += 0.5
    away.conceded += 0.5

# Now take into account league position

    homePos = matchStats.findPosition(cursor, homeCode)
    awayPos = matchStats.findPosition(cursor, awayCode)
    home.position = homePos[1]
    away.position = awayPos[1]
    leagueDifference = home.position - away.position

    homeMulti = leaguePosition(homePos[0],homePos[1])
    awayMulti = leaguePosition(awayPos[0],awayPos[1])

    homeMulti = (101 - homeMulti) / 100
    awayMulti = (101 - awayMulti) / 100

    home.goals = home.goals * homeMulti
    home.conceded = home.conceded * awayMulti 
    away.goals = away.goals * awayMulti
    away.conceded = away.conceded * homeMulti

# Find the form and adjust the goals scored/conced accordingly
    homeForm = matchStats.getHomeForm(cursor, homeCode)
    for result in homeForm:
        if result[0]  == 'A':
            home.conceded += .1
        elif result[0] == 'W':
            home.goals += .1  
            print(home.goals)
        elif result[0] == 'X':
            home.conceded += .1
            home.goals += .1
        
    awayForm = matchStats.getAwayForm(cursor, awayCode)
    for result in awayForm:
        if result[0] == 'H':
            away.conceded += .1
        elif result[0] == 'A':
            away.goals += .1  
        elif result[0] == 'X':
            away.conceded += .1
            away.goals += .1
        
# Have team played before and add .5 to the winner
    results = matchStats.getResults(cursor, homeCode, awayCode)
    if len(results) > 0:
        for result in results:
            print(result[3])
            if result[1] == 'H' and homeCode == result[2]:
                home.goals += .5
                print(home.goals)
            if result[1] == 'A' and awayCode == result[3]:
                away.goals += .5
        
    print('Home goals: {} conceded: {}'.format(round(home.goals,2),round(home.conceded,2)))
    print('Away goals: {} conceded: {}'.format(round(away.goals,2),round(away.conceded,2)))
    predict(home,away)

    print('League difference: ' + str(abs(leagueDifference)))
    goalsInGame = (matchStats.getHomeAverageScore(cursor, homeCode)[0] + \
                 matchStats.getAwayAverageScore(cursor, awayCode)[0]) / 2
    print('Goals per game: {}'.format(round(goalsInGame,2)))