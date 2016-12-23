#!/usr/bin/python3
import logging
import pymysql
from players import Player

season = '1617'
db = pymysql.connect (host="localhost",
                          user="player",
                          passwd="Tykes",
                          db="soccer",
                          autocommit = True
                          )
                          
sky_team_names = {'Sheffield United':'SHEUTD','Manchester City':'MANCIT',
            'Manchester United':'MANUTD','Oxford United':'OXFUTD','Leicester City':'LEICES',
            'Stoke City':'STOKE','Tottenham Hotspur':'TOTTEN', 'West Bromwich Albion':'WESBRO',
            'West Ham United':'WESHAM','Birmingham City':'BIRMIN','Blackburn Rovers':
            'BLACKB','Burton Albion':'BURTON','Cardiff City':'CARDIF', 'Derby County':'DERBY',
            'Huddersfield Town':'HUDDER','Ipswich Town':'IPSWIC','Leeds United':'LEEDS',
            'Newcastle United':'NEWCAS','Norwich City':'NORWIC','Preston North End':'PRESTO',
            'Queens Park Rangers':'QPR','Rotherham United':'ROTHER','Wigan Athletic':'WIGAN',
            'AFC Wimbledon':'WIMBLE','Bolton Wanderers':'BOLTON','Bradford City':'BRADFO',
            'Charlton Athletic':'CHARLT','Coventry City':'COVENT','Fleetwood Town':'FLEETW',
            'Milton Keynes Dons':'MK DON','Northampton Town':'NORTHA','Oldham Athletic':'OLDHAM',
            'Peterborough United':'PETERB','Scunthorpe United':'SCUNTH','Shrewsbury Town':'SHREWS',
            'Southend United':'SOUTHE','Swindon Town':'SWINDO','Accrington Stanley':'ACCRIN',
            'Barnet FC':'BARNET','Cambridge United':'CAMBRI','Carlisle United':'CARLIS',
            'Cheltenham Town':'CHELTE','Colchester United':'COLCHE','Crawley Town':'CRAWLE',
            'Crewe Alexandra':'CREWE','Exeter City':'EXETER','Grimsby Town':'GRIMSB',
            'Hartlepool United':'HARTLE','Luton Town':'LUTON','Newport County':'NEWPOR',
            'Plymouth Argyle':'PLYMOU','Wycombe Wanderers':'WYCOMB','Nottingham Forest':'NOTFOR',
            'Notts County':'NOTCOU','Sheffield Wednesday':'SHEWED'}

def openDatabase():
    logging.debug('openDatabase')
    return db.cursor()

def readTeamNames(cur):
    logging.debug('readTeamName')
    cur.execute("Select * from TeamNames")
    for row in cur.fetchall():
        print (row)
    
def findTeamCode(cur,team):
    logging.debug('findTeamCode for: ' + team)
    
    if team in sky_team_names:
        return sky_team_names[team]
            
    sql = "SELECT `Code` FROM `TeamNames` where `Description` = %s" 
    try:
        cur.execute(sql, team)
        results = cur.fetchone()
    except pymysql.InternalError as error:
        logging.debug('findTeamCode Team ' + str(team)  + error)
        
    return results[0]
    
def getFormations(cur, team):
    
    sql = "SELECT `Formation`,`Opposition` FROM `MatchDaySquad` WHERE `Team` = %s"
    try:
        cur.execute(sql, team)
        formation = cur.fetchall()
    except pymysql.InternalError as error:
        logging.debug('getFormations SQL failed for: ' + team + error)
        
    return formation
        
def getHomeResultsData(cur ,team, opposition):
    
    sql = "SELECT `Score`,`result`, `date`, 'H' FROM `Results` WHERE `homeCode` = %s \
             AND `awayCode` = %s"
    try:
        cur.execute(sql, (team, opposition))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.debug('getHomeResultsData SQL failed for home: ' + team + error)
        
    return results
    
def getAwayResultsData(cur ,team, opposition):
    
    sql = "SELECT `Score`,`result`, `date`, 'A' FROM `Results` WHERE `homeCode` = %s \
             AND `awayCode` = %s"
    try:
        cur.execute(sql, (opposition, team))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.debug('getAwayResultsData SQL failed for away: ' + team + error) 
    resultsData.append(results)
    
    return result
    
def getHomeStatsData(cur ,team):

    sql = "SELECT `homeGoals`,`homePossession`, `homeShots`, `homeShotsOnTarget`,`homeCorners` \
             ,`homeFouls`  ,`awayTeam` FROM `Stats` where `homeTeam` = %s"
    try:
        cur.execute(sql, team)
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.debug('getHomeStatsData SQL failed for home: ' + team + error)
        
    return results
    
def getAwayStatsData(cur ,team):
    
    sql = "SELECT `awayGoals`,`awayPossession`, `awayShots`, `awayShotsOnTarget`,`awayCorners` \
             `awayFouls` `homeTeam` FROM `Stats` where 'awayTeam' = %s"
    try:
        cur.execute(sql, (team))
        results = cur.fetchall()
    except pymysql.InternalError as error:
        logging.debug('getAwayStatsData SQL failed for away: ' + team+  error)
    resultsData.append(results)
    
    return result
    
def closeDatabase(cur):    
    logging.debug('closeDatabase')
    db.close
    
logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
    
cursor = openDatabase()
 
teamFormation = getFormations(cursor, "BARNSL")
print(teamFormation[1][1])
teamStats = getHomeStatsData(cursor, "BARNSL")
print(teamStats[1])