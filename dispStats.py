#!/usr/bin/python3
import getSQLdata, logging
import argparse, dispData

logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of dispStats.py')

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

# Average home team stats
results = getSQLdata.getHomeAvg(cursor,homeCode)
dispData.printRes(results,'Average','Home')
# Average of the visiting team
results = getSQLdata.getHomeAwayAvg(cursor,homeCode)
dispData.printRes(results,'Average','Away')
# Highest Home stats
results = getSQLdata.getHomeMax(cursor,homeCode)
maxResults = results
dispData.printRes(results,'Max','Home')
# Lowest home team stats
results = getSQLdata.getHomeMin(cursor,homeCode)
minResults = results
dispData.printRes(results,'Min','Home')
# Display the range
rangeResults = dispData.calcRange(maxResults,minResults)
dispData.printRes(rangeResults,'Range','Home')
# Total number of games played
results = getSQLdata.countHomeGames(cursor,homeCode)
print('Total number of home games: ' + str(results[0]))
    
print('Away Team Stats: ' + args.awayTeam)
# Average stats when playing away from home
results = getSQLdata.getAwayAvg(cursor,awayCode)
dispData.printRes(results,'Average','Away')
# Stats of the home team the away team is visiting
results = getSQLdata.getAwayHomeAvg(cursor,awayCode)
dispData.printRes(results,'Average','Home')
# Max away stats
results = getSQLdata.getAwayMax(cursor,awayCode)
maxResults = results
dispData.printRes(results,'Max','Away')
# Min away stats
results = getSQLdata.getAwayMin(cursor,awayCode)
minResults = results
dispData.printRes(results,'Min','Away')
# Display the range
rangeResults = dispData.calcRange(maxResults,minResults)
dispData.printRes(rangeResults,'Range','Away')
# Number of games played away from home
results = getSQLdata.countAwayGames(cursor,awayCode)
print('Total number of away games: ' + str(results[0]))

