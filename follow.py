import urllib.request
from bs4 import BeautifulSoup
import logging
import re

def link(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    stats = soup.find('div',{'id':'tab-1'})
    data = []
    
    try:
        data = stats.get_text(' ') # Have the separator as a space
    except:
        return '****'
    return data
    
def players(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    stats = soup.find('div',{'id':'tab-0'})
    players = []
    players = stats.get_text(',') # Have the separator as a space
    return players
    
def splitStatsData(homeTeam,awayTeam,statsData,matchCode,score):
    stats = {}
    logging.debug('splitStatsData: ' + statsData)
    splitRegEx = re.compile(r'\d+')
    split = splitRegEx.findall(statsData)  
    
    stats.setdefault(matchCode,{'homeTeam':' ','homePossession':0,'homeShots':0,
                                 'homeShotsOnTarget':0,'homeCorners':0,'homeFouls':0,
                                 'homeGoals':0,'awayGoals':0,
                                 'awayTeam':' ','awayPossession':0,'awayShots':0,
                                 'awayShotsOnTarget':0,'awayCorners':0,'awayFouls':0})
   # Find the dash in score
    dashPos = score.find('-')
   # Home team Stats 
    stats[matchCode]['homeTeam']          = homeTeam
    stats[matchCode]['homePossession']    = split[0]
    stats[matchCode]['homeShots']         = split[2]
    stats[matchCode]['homeShotsOnTarget'] = split[4]
    stats[matchCode]['homeCorners']       = split[6]
    stats[matchCode]['homeFouls']         = split[8]      
    stats[matchCode]['homeGoals']         = score[:dashPos]
   # Away team stats 
    stats[matchCode]['awayTeam']          = awayTeam  
    stats[matchCode]['awayPossession']    = split[1]
    stats[matchCode]['awayShots']         = split[3]
    stats[matchCode]['awayShotsOnTarget'] = split[5]
    stats[matchCode]['awayCorners']       = split[7]
    stats[matchCode]['awayFouls']         = split[9]
    stats[matchCode]['awayGoals']         = score[dashPos+1:]
        
    return stats
    
def splitPlayerStats(playerData):
    regex = re.compile(r'\w,[^,]*') # finds player number,player name and ends with ,
    split = splitRegex.findall(playerData)