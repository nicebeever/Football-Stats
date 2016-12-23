from bs4 import BeautifulSoup
import logging,re
import urllib.request,getSQLdata
import argparse

def fillResultData(page_data):
    date = page_text.find('caption').get_text()
    date = getDateRegEx.findall(date)
    if len(date) > 0:
        logging.debug('Start of resultUpdate.py' + str(date))
        date = date[0]
        datenumbers = getNumRegEx.findall(date)
        pos = date.find(' ')
        pos2 = date.rfind(' ')
        month = date[pos+1:pos2]
        monthNumber =monthNum[month]
        date = datenumbers[1]+'-'+str(monthNumber)+'-'+datenumbers[0]

        for details in page_text.find_all('td',{'class':'match-details'}):
            homeTeam = (details.find('span',{'class':'team-home teams'}).get_text()).strip()
            homeCode = getSQLdata.findTeamCode(cursor,homeTeam)
            awayTeam = (details.find('span',{'class':'team-away teams'}).get_text()).strip()
            awayCode = getSQLdata.findTeamCode(cursor,awayTeam)
            matchCode = homeCode + awayCode + season
            tableData.setdefault(matchCode,{'homeCode':homeCode,'Score':' ','awayCode':awayCode,\
                        'result': ' ','date':date})
        # Maybe postponed so try and find a score
            try:
                score = details.find('abbr',{'title':'Score'}).get_text()
            except:
                continue
            pos = score.find('-')
            homeScore = int(score[:pos])
            awayScore = int(score[pos+1:])
        
            if homeScore > awayScore:
                result = 'H'
            elif homeScore < awayScore:
                result='A'
            elif homeScore == 0 and awayScore == 0:
                result = 'D'
            else:
                result = 'X'
            tableData[matchCode]['result'] = result
            tableData[matchCode]['Score'] = score
        
monthNum = {'January':1,'Febuary':2,'March':3,'April':4,'May':5,'June':6,'July':7,\
             'August':8,'September':9,'October':10,'November':11,'December':12}

logging.basicConfig(level = logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of resultUpdate.py')

domain_page = 'http://www.bbc.co.uk/sport/football'
sub_page_prem = '/premier-league/results'
sub_page_champ = '/championship/results'
sub_page_L1 = '/league-one/results'
sub_page_L2 = '/league-two/results'
getDateRegEx = re.compile(r'[0-9].+')
getNumRegEx = re.compile(r'[0-9]+')
cursor = getSQLdata.openDatabase()

logging.debug('Premiership result update')
page = urllib.request.urlopen(domain_page + sub_page_prem)
soup = BeautifulSoup(page, 'html.parser') 
tableData = {}
season = '1617'
for page_text in soup.find_all('table',{"class":"table-stats"}):
    fillResultData(page_text)

logging.debug('Championship result update')    
page = urllib.request.urlopen(domain_page + sub_page_champ)
soup = BeautifulSoup(page, 'html.parser')
for page_text in soup.find_all('table',{"class":"table-stats"}):
  fillResultData(page_text)
  
logging.debug('League One result update')  
page = urllib.request.urlopen(domain_page + sub_page_L1)
soup = BeautifulSoup(page, 'html.parser') 
for page_text in soup.find_all('table',{"class":"table-stats"}):
    fillResultData(page_text)

logging.debug('League Two result update')  
page = urllib.request.urlopen(domain_page + sub_page_L2)
soup = BeautifulSoup(page, 'html.parser') 
for page_text in soup.find_all('table',{"class":"table-stats"}):
   fillResultData(page_text)
   
getSQLdata.createResultsTable(cursor, tableData)
cursor = getSQLdata.closeDatabase(cursor)