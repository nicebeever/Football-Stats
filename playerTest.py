from players import Player 
import getSQLdata,matchStats

cursor = getSQLdata.openDatabase()

def teamPlayers(team):

    positions = ['Goalkeeper','Goal Keeper','Defender','Midfielder','Attacking Midfielder'\
                   ,'Striker']
    objectName = {}
    for position in positions:
        playersData = getSQLdata.getPlayerDetails(cursor,position,team)

        for playerData in playersData:
            footballer(objectName,playerData)
  
    matchSquad = matchStats.getMatchSquad(cursor,team)
    for squad in matchSquad:
        games = matchStats.getResults(cursor, team, squad[1])
        if len(games) > 0:
            for game in games:
                score = str(game[0]).strip()
                result = game[1]
                homeTeam = game[2]
                awayTeam = game[3]
                if homeTeam == team:
                    scored = int(score[:1])
                    conceded = int(score[2:])    
                elif awayTeam == team:
                    scored = int(score[2:])
                    conceded = int(score[:1])
            
                for number in range (3, 14):
                    playerName = squad[number]
                    if objectName.get(playerName) is None:
                        if getSQLdata.countPlayer(cursor,playerName,team) > 0:
                            playerData = getSQLdata.getPlayer(cursor,playerName,team)
                            footballer(objectName,playerData[0])
                            
                    objectName[playerName].match += 1
                    objectName[playerName].score = \
                      calculatePoints(objectName[playerName].score,scored)
                    objectName[playerName].conceded = \
                      calculatePoints(objectName[playerName].conceded,conceded)
                
    return objectName
    
def footballer(objectName,playerInfo):
    name = str(playerInfo[0])
    Team = str(playerInfo[1])
    Goals = int(playerInfo[2])
    Reds = int(playerInfo[3])
    yellow = int(playerInfo[4])
    subs = int(playerInfo[5])
    points = int(playerInfo[6])
    apps = int(playerInfo[7])
    pos = str(playerInfo[8])
    playerName = name.replace('-','').replace("'","")
    playerName = playerName.replace(' ','').upper()
    objectName[playerName] = Player(name,Team,Goals,Reds,yellow,subs,points,apps,pos)
    
def calculatePoints(playerScore,goals):
    contribution = goals / 11
    avgPoints = (playerScore + contribution) / 2
    return avgPoints