from bs4 import BeautifulSoup
import logging,re
import urllib.request,getSQLdata
domain_page = 'http://www.skysports.com'
link = '/football/player/134576/didier-ndong'
squad = '/arsenal-squad'
team='west-ham'
positionRegEx = re.compile(r'Position: .+')
nameRegEx = re.compile(r'Name: .+')
playerStats = {}

print(domain_page + squad)
page = urllib.request.urlopen(domain_page + squad)
soup = BeautifulSoup(page, 'html.parser')

formation = soup.find('div', class_="span10 strap1 -center -ondark -interact text-h5 arrangement").get_text()
print(formation)
#allPlayers = soup.find_all('li', class_="tp")
#print(allPlayers)
