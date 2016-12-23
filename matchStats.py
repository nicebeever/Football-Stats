#!/usr/bin/python3
import logging
import pymysql

def findPosition(cur,teamCode):
     # Find the position of team.
    try:
        sql = "SELECT `division`,`position` from `PremierLeague` where teamCode = %s"
        cur.execute(sql, (teamCode))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('findPosition SQL failed ' + error)
    return result
    
def getTeamsAround(cur, league, position):
   # Find out the teams around this position
    upperTeamPos = position - 4
    if upperTeamPos < 0:
        upperTeamPos = 1 
        
    lowerTeamPos = position + 4
    try:
        sql = "SELECT `teamCode` from `PremierLeague` WHERE division = %s AND \
            `position` BETWEEN %s AND %s"
        cur.execute(sql,(league,upperTeamPos,lowerTeamPos))
        result = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('getTeamsAround SQL failed ' + error)
    
    return result

def findHomeResults(cur, homeTeam, awayTeams):
    # Find the results for the home team
    sql = "SELECT `Score`,`result`,`awayCode` FROM `Results` WHERE homeCode = %s AND \
            `awayCode` IN %s" 
    try:
        cur.execute(sql,(homeTeam,awayTeams))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('findHomeResults SQL failed ' + error)
    
    return results
    
def findAwayResults(cur, awayTeam, homeTeams):
    # Find the results for the home team
    sql = "SELECT `Score`,`result` FROM `Results` WHERE awayCode = %s AND \
            `homeCode` IN %s" 
    try:
        cur.execute(sql,(awayTeam,homeTeams))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('findAwayResults SQL failed ' + error)
    
    return results
    
def getForm(cur, team):
    home = team + '%1617'
    away = '%' + team + '1617'
    sql = "SELECT `result`,`homeCode` FROM `Results` where `matchCode` like %s OR `matchCode` like %s\
              ORDER BY `date` DESC limit 10"
    print('L = Lost Home O = Lost away D = Draw Home Y = Draw away W = Win Home A = Win away') 
              
    try:
        cur.execute(sql,(home,away))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('getForm SQL failed ' + error)
        
    form = ''
    for res in results:
        # Lost at Home
        if res[0] == 'A' and res[1] == team:
            form += 'L'
        # Lost away from home
        elif res[0] == 'H' and res[1] != team:
            form += 'O'
        # Drawn at Home
        elif (res[0] == 'D' or res[0] == 'X') and res[1] == team:
            form += 'D'
        # Drawn away from home
        elif (res[0] == 'D' or res[0] == 'X') and res[1] != team:
            form += 'Y'
        # Won away from home
        elif res[0] == 'A' and res[1] != team:
            form += 'A'
        else:
            form += str(res[0])
            
    return form

def getHomeForm(cur, team):
    home = team + '%1617'
    sql = "SELECT `result` FROM `Results` where `matchCode` like %s \
              ORDER BY `date` DESC limit 10"
              
    try:
        cur.execute(sql,(home))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('getHomeForm SQL failed ' + error)
            
    return results
    
def getAwayForm(cur, team):
    away = '%' + team + '1617'
    sql = "SELECT `result` FROM `Results` where `matchCode` like %s \
              ORDER BY `date` DESC limit 10"
              
    try:
        cur.execute(sql,(away))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('getAwayForm SQL failed ' + error)
            
    return results

def getMatchSquad(cur, team):
    sql = "SELECT * FROM `MatchDaySquad` where `Team` = %s"
    try:
        cur.execute(sql,(team))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('getMatchSquad SQL failed ' + error)
        
    return results
    
def getResults(cur, team, opposition):
    sql = "SELECT `Score`,`result`, `homeCode`, `awayCODE` FROM `Results` WHERE \
               (`homeCode` = %s AND `awayCode` = \
                   %s) OR (`homeCode` = %s AND `awayCode` = %s)"
    try:
        cur.execute(sql,(team,opposition,opposition,team))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('getResults SQL failed ' + error)
        
    return results         
    
def getTopEleven(cur, team):
    sql ="SELECT `Code` FROM `Player` WHERE `Team` = %s ORDER BY `Apperances` DESC LIMIT 11"
    try:
        cur.execute(sql,team)
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('getTopEleven SQL failed ' + error)
        
    return results 
    
def getLastMatch(cur, team):
    sql ="SELECT `homeCode`,`awayCode` FROM `Results` WHERE `homeCode` = %s \
            OR `awayCode` = %s ORDER BY `date` DESC LIMIT 1"
    try:
        cur.execute(sql,(team,team))
        results = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getLastMatch SQL failed ' + error)
        
    return results 

def getLastEleven(cur, team, opposition):
    sql ="SELECT * FROM `MatchDaySquad` WHERE `Team` = %s AND `Opposition` = %s"
    try:
        cur.execute(sql,(team, opposition))
        results = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getLastEleven SQL failed ' + error)
        
    return results 
    
def getHomeAverageScore(cur, team):
    sql = 'SELECT avg(substring(score,2,1) + substring(score,4,1)) \
            FROM `Results` where homeCode= %s ORDER BY `date` DESC LIMIT 6'
            
    try:
        cur.execute(sql,team)
        results = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getHomeAverageScore SQL failed ' + error)
        
    return results

def getAwayAverageScore(cur, team):
    sql = 'SELECT avg(substring(score,2,1) + substring(score,4,1)) \
            FROM `Results` where awayCode= %s ORDER BY `date` DESC LIMIT 6'
    try:
        cur.execute(sql,team)
        results = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getAwayAverageScore SQL failed ' + error)
        
    return results
        