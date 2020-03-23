import urllib2
import urllib
import base64
import json 
import uuid
import requests



def Odds_toDecimal(american):
	if american > 0:
		return ((float(american)/100.0) + 1)
	else:
		return ((100.0/float(abs(american))) + 1)



# MLB_home_team = "Team2"
fullTeamNames = ["Baltimore Orioles", "Tampa Bay Rays", "Chicago Cubs", "Miami Marlins", "Minnesota Twins", "Cleveland Indians",
					"Colorado Rockies", "Los Angeles Dodgers", "Detroit Tigers", "San Diego Padres", "Toronto Blue Jays", "Kansas City Royals",
					"Houston Astros", "Seattle Mariners", "Texas Rangers", "New York Yankees", "Cincinnati Reds", "Washington Nationals",
					"Philadelphia Phillies", "Arizona Diamondbacks", "Milwaukee Brewers", "Atlanta Braves", "LAA Angels", "Boston Red Sox",
					 "New York Mets", "San Francisco Giants", "Pittsburgh Pirates", "St. Louis Cardinals", "Oakland Athletics", "Chicago White Sox"]
teamInitials = {}

def MLB_FullTeam_Name(partialName):
	for team in fullTeamNames:
		if partialName.lower() in team.lower():
			return team

def get_MLB_events():
	url = 'https://api.pinnacle.com/v1/odds?sportid=3&leagueids=246&oddsFormat=DECIMAL'

	username = "ED974228"
	password = "#B0tSw4g9"
	b64str = "Basic " + base64.b64encode('{}:{}'.format(username,password).encode('utf-8')).decode('ascii')
	headers = {'Content-length' : '0',
			   'Content-type' : 'application/xml',
			   'Authorization' : b64str}

	req = urllib2.Request(url, headers=headers)
	responseData = urllib2.urlopen(req).read()
	ofn = 'api_leagues.txt'
	with open(ofn, 'w') as ofile:
		ofile.write(responseData)
	return responseData

def get_MLB_fixtures():
	#Used to get the names of teams in event.
	url = 'https://api.pinnacle.com/v1/fixtures?sportId=3&leagueIds=246'

	username = "ED974228"
	password = "#B0tSw4g9"
	b64str = "Basic " + base64.b64encode('{}:{}'.format(username,password).encode('utf-8')).decode('ascii')
	headers = {'Content-length' : '0',
			   'Content-type' : 'application/xml',
			   'Authorization' : b64str}

	req = urllib2.Request(url, headers=headers)
	responseData = urllib2.urlopen(req).read()
	ofn = 'api_leagues.txt'
	with open(ofn, 'w') as ofile:
		ofile.write(responseData)
	return responseData



def get_balance():
	url = 'https://api.pinnacle.com/v1/client/balance'

	username = "ED974228"
	password = "#B0tSw4g9"
	b64str = "Basic " + base64.b64encode('{}:{}'.format(username,password).encode('utf-8')).decode('ascii')
	headers = {'Content-length' : '0',
			   'Content-type' : 'application/xml',
			   'Authorization' : b64str}

	req = urllib2.Request(url, headers=headers)
	responseData = urllib2.urlopen(req).read()
	ofn = 'api_leagues.txt'
	with open(ofn, 'w') as ofile:
		ofile.write(responseData)
	return responseData

def place_bet(bet, stake):

	username = "ED974228"
	password = "#B0tSw4g9"
	
	url = "https://api.pinnacle.com/v1/bets/place"
	b64str = base64.b64encode("{}:{}".format(username,password).encode('utf-8'))
	headers = {'Content-length' : '1',
			   'Content-type' : 'application/json',
			   'Authorization' : "Basic " + b64str.decode('utf-8')}
	print "\n\n\n**************************"
	print "Basic " + b64str.decode('utf-8')
	print "**************************\n\n\n"
	values = {
			"uniqueRequestId":uuid.uuid1().hex,
			"acceptBetterLine": "True",
			"oddsFormat":"DECIMAL",
			"stake": str(13),
			"winRiskStake":"RISK",
			"sportId":str(3),
			"eventId":str(738341297),  
			"period":"0",     
			"betType":"MONEYLINE",
			"team": 'Team1',
			"lineId":str(402941863)
	}

	data2 = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}

	# req = urllib2.Request(url, headers = headers)
	response = requests.post(url, data={}, headers=headers)
	print "Response:\n", response
	response = json.loads(response)
	print("Bet status: " + response["status"])
	print response





#Only fyll game moneyline for now
def MLB_makeBet(pick, stake):
	teamName = MLB_FullTeam_Name(pick['team'])
	bet = {
	'type': 'MONEYLINE',
	'sportId': 3,
	'period': 0,
	}

	#find correct event
	for event in events:
		if event["Team1"] == teamName:
			bet['eventId'] = event['id']
			bet['lineId'] = event['periods'][0]['lineId']
			bet['team'] = 'Team1'
		elif  event["Team2"] == teamName:
			bet['eventId'] = event['id']
			bet['lineId'] = event['periods'][0]['lineId']
			bet['team'] = 'Team2'

	return bet



bet = {'team': "indians", 'type': 'MONEYLINE', 'odds': 177}


print(bet)

place_bet(bet, 13)