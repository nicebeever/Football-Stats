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
            'Notts County':'NOTCOU','Sheffield Wednesday':'SHEWED','brighton-and-hove-albion':'BRIGHT',
            'wolverhampton':'WOLVES','doncaster-rovers':'DONCAS','stevenage':'STEVEN'}

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
    except:
        results = None
        logging.debug('findTeamCode Team ' + str(team) + ' not found')
        
    if results == None:
        return updateTeamCode(cur,team)
        
    return results[0]
    
    
def updateTeamCode(cur,team):
    logging.debug('updateTeamCode for: ' + team)
    
    start2 = team.find(' ')
    matchCode = '******'
    results = None
    
    if start2 > 0:
        matchCode = (team[0:3]+team[start2+1:start2+4]).upper()
    else:
        matchCode = (team[0:6]).upper()
        
    sql = "SELECT count(*) FROM `TeamNames` where `Code` = %s"
    try:
        cur.execure(sql, matchCode)
        results = cur.fetchone()
    except:
        logging.debug('updateTeamCode SQL failed to find matchCode ')
        
    if results == None:
        logging.debug('updateTeamCode insert code into table: ' + matchCode)
        try:
            sql = "INSERT INTO TeamNames VALUES ('%s','%s')" % (team, matchCode)
            cur.execute(sql)
            logging.debug('updateTeamCode INSERT SQL')
        except:
            logging.warning('updateTeamCode Insert SQL Failed')   
            
    return matchCode
    

def setFixtures(cur,home,away):
    logging.debug('setFixture table: ' + str(home) + ' v ' +str(away))
    sql = "SELECT count(*) FROM `Fixtures` where `MatchCode` = %s"
    code = str(home)+str(away)+str(season)
    logging.debug('setFixture matchCode: ' + str(code))
    try:
        cur.execute(sql, code)
        numbers = cur.fetchone()
    except:
        logging.warning('SetFixtures sql failed: ' + sql)

    if numbers[0] < 1:
        try:
            # the \ just splits the below line
            sql = "INSERT INTO Fixtures VALUES ('%s','%s','%s','%s')" % \
                    (home, away, season, code)
            cur.execute(sql)
            logging.debug('setFixtures Insert sql')    
            return code
        except:
            logging.warning('setFixtures Failed')
                
    return '****'
    
def setStats(cur,stats,matchcode):
    sql = "SELECT count(*) FROM `Stats` where `MatchCode` = %s"
    try:
        cur.execute(sql, matchcode)
        numbers = cur.fetchone()
    except:
        logging.warning('setStats failed sql: ' +  matchcode)
    
    if numbers[0] < 1:
        try:
            sql = "INSERT INTO `Stats` VALUES ('%s','%s',%s,%s,%s,%s,%s,%s,'%s' \
                                             ,%s,%s,%s,%s,%s,%s)" % \
                (matchcode,stats[matchcode]['homeTeam'],stats[matchcode]['homeGoals']  \
                 ,stats[matchcode]['homePossession'],stats[matchcode]['homeShots'] \
                 ,stats[matchcode]['homeShotsOnTarget'],stats[matchcode]['homeCorners'] \
                 ,stats[matchcode]['homeFouls'],stats[matchcode]['awayTeam'] \
                 ,stats[matchcode]['awayPossession'],stats[matchcode]['awayShots'] \
                 ,stats[matchcode]['awayShotsOnTarget'],stats[matchcode]['awayCorners'] \
                 ,stats[matchcode]['awayFouls'],stats[matchcode]['awayGoals']) 
            cur.execute(sql)
            logging.debug('setStats insert SQL worked')
        except:
            logging.warning('setStats failed SQL: ' + SQLSTATE())
            logging.debug('setStats: ' + str(stats))
    else:
        logging.debug('setStats found record for Match Code: ' + matchcode)

def getAwayAvg(cur,team):
    # Find the away team average results
    try:
        sql = "SELECT AVG(awayPossession), AVG(awayShots), AVG(awayShotsOnTarget), \
                AVG(awayCorners), AVG(awayFouls), AVG(awayGoals), AVG(homeGoals) \
                 FROM `Stats` WHERE awayTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except:
        logging.warning('getAwayAvg SQL failed for team: ' + team)
        
    return result

def getAwayHomeAvg(cur,team):
    # Find the home team results when the team was playing away
    try:
        sql = "SELECT AVG(homePossession), AVG(homeShots), AVG(homeShotsOnTarget), \
                AVG(homeCorners), AVG(homeFouls), AVG(homeGoals) \
                 FROM `Stats` WHERE awayTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except:
        logging.warning('getAwayHomeAvg SQL failed for team: ' + team)
        
    return result


def getAwayMax(cur,team):
    try:
        sql = "SELECT MAX(awayPossession), MAX(awayShots), MAX(awayShotsOnTarget), \
         MAX(awayCorners), MAX(awayFouls), MAX(awayGoals) \
          FROM `Stats` WHERE awayTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getAwayMax SQL failed for team: ' + team + ' ' + str(error))

    return result

def getAwayMin(cur,team):
    try:
        sql = "SELECT MIN(awayPossession), MIN(awayShots), MIN(awayShotsOnTarget), \
                MIN(awayCorners), MIN(awayFouls), MIN(awayGoals) \
                 FROM `Stats` WHERE awayTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getAwayMin SQl failed for team: ' + team + ' ' + str(error))

    return result
    
def countAwayGames(cur,team):
    try:
        sql ="SELECT COUNT(*) FROM `Stats` where awayTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('countAwayGames SQL failed for team:' + team + ' ' + str(error))
        
    return result

def getHomeAvg(cur,team):
    try:
        sql = "SELECT AVG(homePossession), AVG(homeShots), AVG(homeShotsOnTarget), \
                AVG(homeCorners), AVG(homeFouls), AVG(homeGoals), AVG(awayGoals) \
                 FROM `Stats` WHERE homeTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getHomeAvg SQl failed for team: ' + team + ' ' + str(error))
        
    return result
    
def getHomeAwayAvg(cur,team):
    try:
        sql = "SELECT AVG(awayPossession), AVG(awayShots), AVG(awayShotsOnTarget), \
                AVG(awayCorners), AVG(awayFouls), AVG(awayGoals) \
                 FROM `Stats` WHERE homeTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getHomeAwayAvg SQl failed for team: ' + team + ' ' + str(error))
        
    return result
    
def getHomeMax(cur,team):
    try:
        sql = "SELECT MAX(homePossession), MAX(homeShots), MAX(homeShotsOnTarget), \
                MAX(homeCorners), MAX(homeFouls), MAX(homeGoals) \
                 FROM `Stats` WHERE homeTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getHomeMax SQl failed for team: ' + team + ' ' + str(error))
        
    return result

def getHomeMin(cur,team):
    try:
        sql = "SELECT MIN(homePossession), MIN(homeShots), MIN(homeShotsOnTarget), \
                MIN(homeCorners), MIN(homeFouls), MIN(homeGoals) \
                FROM `Stats` WHERE homeTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getHomeMin SQl failed for team: ' + team + ' ' + str(error))
        
    return result
    
def countHomeGames(cur,team):
    try:
        sql ="SELECT COUNT(*) FROM `Stats` where homeTeam = %s"
        cur.execute(sql, (team))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('countHomeGames SQL failed for team: ' + team + ' ' + str(error))

        
    return result

def countPlayerData(cur,playerName,teamName):
    try:
        sql = "Select COUNT(*) from `Player` where Name = %s and Team = %s"
        cur.execute(sql, (playerName, teamName))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('countPlayerDetails SQL failed ' + str(error))
        
    return result[0]
    
def countPlayer(cur,code,teamName):
    try:
        sql = "Select COUNT(*) from `Player` where Code = %s and Team = %s"
        cur.execute(sql, (code, teamName))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('countPlayer SQL failed ' + str(error))
        
    return result[0]
    
def updatePlayerData(cur,player,playerStats):
    try:
        sql = 'UPDATE `Player` SET Goals = %s, RedCards = %s, YellowCards = %s \
        , Apperances = %s, Subs = %s, FantasyScore = %s WHERE Name = "%s" and Team = "%s" ' \
         % (playerStats['goals'] ,playerStats['redCards'] \
         ,playerStats['yellowCards'] ,playerStats['apperances'] \
         ,playerStats['subs'] ,playerStats['fantasyScore'], player \
         ,playerStats['team'])
        cur.execute(sql)
    except pymysql.InternalError as error:
        logging.warning('updatePlayerData SQL Insert failed: ' + \
               str(player) + ' ' + str(error))

def writePlayerData(cur,player,team,playerStats):
    try:
        sql = "DELETE FROM `Player` WHERE Name = %s and Team = %s" 
        cur.execute(sql, (player,team))
    except pymysql.InternalError as error:
        logging.warning('writePlayerData delete failed: ' + str(player) +' ' + str(error))
    try:
        sql = 'INSERT INTO `Player` VALUES ("%s","%s",%s,%s,%s,%s,%s,%s,"%s","%s")' % \
            (player,playerStats['team'],playerStats['goals'] \
             ,playerStats['redCards'],playerStats['yellowCards'] \
             ,playerStats['apperances'],playerStats['subs'] \
             ,playerStats['fantasyScore'],playerStats['position']
             ,playerStats['Code'])
        cur.execute(sql)
    except pymysql.InternalError as error:
        logging.warning('writePlayerData SQL Insert failed: ' + \
                str(player) + ' ' + str(error))
        
def getPlayerDetails(cur,position, team):
    try:
        sql = "SELECT Name, Team, Goals, RedCards, YellowCards,Subs, FantasyScore, \
               Apperances, position FROM Player where position =%s and Team= %s \
               ORDER BY Apperances, FantasyScore DESC"
        cur.execute(sql, (position,team))
        result = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('getPlayerDetails SQL failed ' + str(error))
    return result
    
def getPlayer(cur,code, team):
    try:
        sql = "SELECT Name, Team, Goals, RedCards, YellowCards,Subs, FantasyScore, \
               Apperances, position FROM Player where Code =%s and Team= %s \
               ORDER BY Apperances, FantasyScore DESC"
        cur.execute(sql, (code,team))
        result = cur.fetchall()
    except pymysql.InternalError as error:
        logging.warning('getPlayer SQL failed ' + str(error))
    return result
        
def getNameDash(cur, name, team):
    try:
        sql = "Select Name FROM Player where Name like %s and Team=%s"
        cur.execute(sql)
    except pymysql.InternalError as error:
        logging.warning('getNameDash SQL failed ' + str(error))
        
def countMatchDaySquad(cur, team, opposition, date):
    try:
        sql = 'SELECT COUNT(*) FROM `MatchDaySquad` WHERE Team = %s AND opposition = %s \
                 AND date = %s'
        cur.execute(sql, (team, opposition, date))
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('countMatchDaySquad SQL failed ' + str(error))
    return result

def updateMatchDaySquad(cur, players, team, opposition, formation, date):
    try:
        sql = 'INSERT INTO `MatchDaySquad` VALUES("%s","%s","%s","%s","%s","%s","%s","%s", \
                 "%s","%s","%s","%s","%s","%s","%s")' % (team, opposition,formation, players[0], \
                   players[1],players[2],players[3],players[4],players[5],players[6],players[7],\
                   players[8],players[9],players[10],date)
        cur.execute(sql)
    except pymysql.InternalError as error:
        logging.warning('updateMatchDaySquad SQL failed ' + str(error))
        
def createTable(cur, tableData):
    cur.execute('DELETE FROM `PremierLeague` WHERE position BETWEEN 1 AND 96')
    for teamName in tableData:
        try:
            sql = 'INSERT INTO `PremierLeague` VALUES(%d,"%s",%d,%d,%d,%d,%d,%d,%d,%d,"%s","%s","%s")' % \
             (tableData[teamName]['position'],teamName, tableData[teamName]['played'], \
                 tableData[teamName]['won'], tableData[teamName]['drawn'], \
                 tableData[teamName]['lost'], tableData[teamName]['goalsFor'], \
                 tableData[teamName]['goalsAgainst'], tableData[teamName]['goalDifference'], \
                 tableData[teamName]['points'], tableData[teamName]['lastTen'], \
                 tableData[teamName]['teamCode'], tableData[teamName]['table'])
            cur.execute(sql)
        except pymysql.InternalError as error:
            logging.warning('createTable SQL failed ' + str(error))


def createResultsTable(cur, tableData):
    for gameCode in tableData:
        sql = ("SELECT COUNT(*) FROM `Results` WHERE `matchCode` = %s")
        cur.execute(sql, (gameCode))
        result = cur.fetchone()
        if result[0] < 1:
            try:
                sql = 'INSERT INTO `Results` VALUES("%s","%s","%s","%s","%s","%s")' % \
                 (tableData[gameCode]['homeCode'], tableData[gameCode]['Score'], \
                     tableData[gameCode]['awayCode'], tableData[gameCode]['result'], \
                     tableData[gameCode]['date'], gameCode) 
                cur.execute(sql)
            except pymysql.InternalError as error:
                logging.warning('createResultsTable SQL failed ' + str(error))
                
def getTeamForm(cur, team):
    sql = ("SELECT `position`,`form`,`division` FROM `PremierLeague` WHERE `teamCode` = %s ")
    try:
        cur.execute(sql, team)
        result = cur.fetchone()
    except pymysql.InternalError as error:
        logging.warning('getTeamForm SQL failed ' + str(error))
    return result
    
def getTeamFormations(cur, team):
    sql = "SELECT `Formation`,count(`Formation`) as games FROM `MatchDaySquad` \
                             WHERE `Team` = %s GROUP BY `Formation` ORDER BY games DESC"
    try:
        cur.execute(sql, team)
        results = cur.fetchall()    
    except pymysql.InternalError as error:
        logging.warning('getTeamFormations SQL failed ' + str(error))
    return results
    
def getOppFormationsWhenWonAtHome(cur, team):
    sql = "SELECT `Formation`, count(`Formation`) AS games FROM `MatchDaySquad` WHERE `team` IN ( \
            SELECT `awayCode` FROM `Results` WHERE `homeCode` = %s and `RESULT` = 'H') \
             AND `Opposition` = %s GROUP BY `Formation` ORDER BY games DESC"
    try:
        cur.execute(sql, (team, team))
        results = cur.fetchall()    
    except pymysql.InternalError as error:
        logging.warning('getOppFormationsWhenWonAtHome SQL failed ' + str(error))
    return results
    
def getOppFormationsWhenDrawnAtHome(cur, team):
    sql = "SELECT `Formation`, count(`Formation`) AS games FROM `MatchDaySquad` WHERE `team` IN ( \
            SELECT `awayCode` FROM `Results` WHERE (`homeCode` = %s and `RESULT` = 'D') OR  \
             (`homeCode` = %s and `RESULT` = 'X')) AND `Opposition` = %s \
              GROUP BY `Formation` ORDER BY games DESC"
    try:
        cur.execute(sql, (team, team, team))
        results = cur.fetchall()    
    except pymysql.InternalError as error:
        logging.warning('getOppFormationsWhenDrawnAtHome SQL failed ' + str(error))
    return results
    
def getOppFormationsWhenLostAtHome(cur, team):
    sql = "SELECT `Formation`, count(`Formation`) AS games FROM `MatchDaySquad` WHERE `team` IN ( \
            SELECT `awayCode` FROM `Results` WHERE `homeCode` = %s and `RESULT` = 'A')   \
             AND `Opposition` = %s GROUP BY `Formation` ORDER BY games DESC"
    try:
        cur.execute(sql, (team, team))
        results = cur.fetchall()    
    except pymysql.InternalError as error:
        logging.warning('getOppFormationsWhenDrawnAtHome SQL failed ' + str(error))
    return results
    
def getOppFormationsWhenWonAway(cur, team):
    sql = "SELECT `Formation`, count(`Formation`) AS games FROM `MatchDaySquad` WHERE `team` IN ( \
            SELECT `homeCode` FROM `Results` WHERE `awayCode` = %s and `RESULT` = 'A') \
             AND `Opposition` = %s GROUP BY `Formation` ORDER BY games DESC"
    try:
        cur.execute(sql, (team, team))
        results = cur.fetchall()    
    except pymysql.InternalError as error:
        logging.warning('getOppFormationsWhenWonAway SQL failed ' + str(error))
    return results
    
def getOppFormationsWhenDrawnAway(cur, team):
    sql = "SELECT `Formation`, count(`Formation`) AS games FROM `MatchDaySquad` WHERE `team` IN ( \
            SELECT `homeCode` FROM `Results` WHERE (`awayCode` = %s and `RESULT` = 'D') OR  \
             (`awayCode` = %s and `RESULT` = 'X')) \
              AND `Opposition` = %s GROUP BY `Formation` ORDER BY games DESC"
    try:
        cur.execute(sql, (team, team, team))
        results = cur.fetchall()    
    except pymysql.InternalError as error:
        logging.warning('getOppFormationsWhenDrawnAway SQL failed ' + str(error))
    return results
    
def getOppFormationsWhenLostAway(cur, team):
    sql = "SELECT `Formation`, count(`Formation`) AS games FROM `MatchDaySquad` WHERE `team` IN ( \
            SELECT `homeCode` FROM `Results` WHERE `awayCode` = %s and `RESULT` = 'H') \
             AND `Opposition` = %s GROUP BY `Formation` ORDER BY games DESC"
    try:
        cur.execute(sql, (team, team))
        results = cur.fetchall()    
    except pymysql.InternalError as error:
        logging.warning('getOppFormationsWhenLostAway SQL failed ' + str(error))
    return results

def closeDatabase(cur):    
    logging.debug('closeDatabase')
    db.close
