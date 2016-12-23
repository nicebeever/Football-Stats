from players import Player 
import playerTest
import getSQLdata,matchStats

def teamSquad(team):
    homeTeam = {}
    cursor = getSQLdata.openDatabase()
    homeTeam = playerTest.teamPlayers(team)

    formation = getSQLdata.getTeamFormations(cursor,team)
    defenders = formation[0][0][:1]
    length = len(formation[0][0])
    attackers = formation[0][0][length-1:]
    midfielders = 10 - int(defenders) - int(attackers)
    print('Defenders: ' + str(defenders) + ' Midfielders: ' + str(midfielders) +\
          ' Attackers: ' + str(attackers))
          
    topTeamGoals = 0
    topTeamConceded = 0
          
    topPlayers = matchStats.getTopEleven(cursor, team)
    for topPlayer in topPlayers:
        name = topPlayer[0]
        try:
            topTeamGoals += (homeTeam[name].score/homeTeam[name].match)/11
            topTeamConceded += (homeTeam[name].conceded/homeTeam[name].match)/11
        except:
            pass
    print("Top team scored: %.2f conceded: %.2f" % (topTeamGoals,topTeamConceded))
    
    lastTeamGoals = 0
    lastTeamConceded = 0
    lastMatch = matchStats.getLastMatch(cursor, team)
    if lastMatch[0] == team:
        opposition = lastMatch[1]
    else:
        opposition = lastMatch[0]
    
    squad = matchStats.getLastEleven(cursor, team, opposition)

    for number in range (3, 14):
        name = squad[number]
        try:
            lastTeamGoals += (homeTeam[name].score/homeTeam[name].match)/11
            lastTeamConceded += (homeTeam[name].conceded/homeTeam[name].match)/11
        except:
            pass
    
    print("Last team scored: %.2f conceded: %.2f" % (lastTeamGoals,lastTeamConceded))
    averageTeamGoal = (topTeamGoals + lastTeamGoals) / 2
    averageTeamConceded = (topTeamConceded + lastTeamConceded) / 2
    
    print("Average scored: %.2f conceded: %.2f" % (averageTeamGoal,averageTeamConceded))