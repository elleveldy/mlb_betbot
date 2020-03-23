import itertools
import json
import os
from commentFinder import *

mlb_nicknames = {
	"Arizona Diamondbacks": ["dbacks", "d-backs", "diamondbacks"],
	"Atlanta Braves": ["braves"],
	"Baltimore Orioles": ["orioles"],
	"Boston Red Sox": ["red sox"],
	"Chicago Cubs":["cubs"],
	"Chicago White Sox":["whites", "white sox"],
	"Cincinnati Reds":["reds"],
	"Cleveland Indians":["indians"],
	"Colorado Rockies":["rockies"],
	"Detroit Tigers":["tigers"],
	"Miami Marlins": ["marlins"],
	"Houston Astros":["astros", "houston"],
	"Kansas City Royals":["royals", "kansas"],
	"LAA Angels":["angels", "laa"],
	"Los Angeles Dodgers":["dodgers"],
	"Milwaukee Brewers":["brewers","milwaukee"],
	"Minnesota Twins":["twins", "minnesota"],
	"New York Mets":["mets"],
	"New York Yankees":["yankees", "nyy"],
	"Oakland Athletics":["oakland", "athletics"],
	"Philadelphia Phillies": ["phillies", "philadelphia"],
	"Pittsburgh Pirates":["pirates"],
	"St. Louis Cardinals":["cardinals"],
	"San Diego Padres":["padres"],
	"San Francisco Giants":["giants"],
	"Seattle Mariners":["mariners"],
	"Tampa Bay Rays":["rays"],
	"Texas Rangers":["rangers"],
	"Toronto Blue Jays":["jays", "blue jays"],
	"Washington Nationals":["nationals", "washington", "nats"]
}

def fullTeamName(nickname):
	# find real name
	fullTeamName = nickname

	if ' ' in nickname:
		if nickname.split(' ')[1] == '':
			nickname = nickname.split(' ')[0]

	if nickname in mlb_nicknames:
		fullTeamName = nickname
	else:
		for team in mlb_nicknames:
			if nickname.lower() == team.lower():
				fullTeamName = team

			if nickname.lower() in mlb_nicknames[team]:
				fullTeamName = team

	if fullTeamName:
		return fullTeamName
	else:
		print("ERROR: FullTeamName({}) returning with: {}".format(nickname, fullTeamName))
		return fullTeamName
	#if real name not found, write to file: unkown name

def Odds_toDecimal(oddsString):
	if "+" in oddsString:
		american = int(oddsString.split('+')[1])
		return round(((float(american)/100.0) + 1), 3)
	else:
		american = int(oddsString.split('-')[1])
		return round(((100.0/float(abs(american))) + 1), 3)

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)


############################################################
###################INSIDERLOCKS#############################
############################################################
#Used for tables with formatting as in insiderlocks comments
def insiderlocks_tableRowToBet(tableRow):
	print("Handling tableRow:", tableRow)
	row = tableRow.split('|')
	if(hasNumbers(row[0])):
		betDict = {'units': row[0]}
	else:
		print("parse_insiderlocks(tableRow ERROR: no unit found in row[0] of tableRow: ", tableRow)
		return

	if("-" in row[1]):
		betDict['SPREAD'] = "-" + row[1].split('-')[1]
	elif("+" in row[1]):
		betDict['SPREAD'] = "+" + row[1].split('+')[1]
	print(" fullTeamName(row[1].split('-')[0]): ", fullTeamName(row[1].split('-')[0]))
	betDict['team'] = fullTeamName(row[1].split('-')[0])
	
	if("+" in row[2]):
		odds = row[2]
	elif("-" in row[2]):
		odds = row[2]

	betDict['odds'] = Odds_toDecimal(odds)
	betDict['betType'] = "SPREAD"

	return betDict


def makeBetList(tableString, user):
	date = updateMLBDailyDate()
	print ("tableString: ".format(tableString))

	bettingTable = {"bets": [], "date": date, "user": user}
	for line in tableString.split('\n'):
		if (not "?" in line) and ("|" in line):
			bettingTable["bets"].append(insiderlocks_tableRowToBet(line))
	return bettingTable

def parse_insiderlocks(rawComment):

	date = updateMLBDailyDate()
	tableString = ""
	for i in range(0, len(rawComment)):
		if(":--|:--|:--|:--|" in rawComment[i:i+16]):
			tableString = rawComment[i+17:len(rawComment)]
	table = makeBetList(tableString, "insiderlocks")
	return table
##########################################################################################
##########################################################################################

def unitsToWin(units, odds):
	return round(float(units)/(float(odds) - 1.0), 3)

def parse_ratbehr(rawComment):

	date = updateMLBDailyDate()
	print("date = americanToEuropeanDate(updateMLBDailyDate()) = ", date)
	print("parse_ratbehr(rawComment):")
	lineList = rawComment.split('\n')

	#if bullet points
	if(not "*" in  rawComment):
		print("No bullet points, fuck off ratbehr")
		return

	betList = []
	for line in lineList:
		bet = line.split(' ')
		print("bet = line.split(' ') = ", bet)
		if '*' in bet:
			betDict = {"betType": "MONEYLINE"}

			#If team name has space
			if len(bet) > 4:
				if bet[4] == '':
					betDict['team'] = fullTeamName(bet[1])
					betDict['odds'] = Odds_toDecimal(bet[2])
					units = bet[3].split('u')[0]
				else:
					betDict['team'] = fullTeamName(str(bet[1]) + " " + str(bet[2]))
					betDict['odds'] = Odds_toDecimal(bet[3])
					units = bet[4].split('u')[0]
			elif len(bet) == 4:
				betDict['team'] = fullTeamName(bet[1])
				betDict['odds'] = Odds_toDecimal(bet[2])
				units = bet[3].split('u')[0]
			#since ratbehr uses "towin" units for favourites:
			if float(units) > 2.0:
				betDict['units'] = units
			else:
				betDict['units'] = unitsToWin(units, betDict['odds'])
			betList.append(betDict)



	return {'user': "ratbehr", 'date': date, "bets": betList}

def commentToDict_Ndborro(rawComment):
	pass

def commentToDict_FadeTheTrap(rawComment):
	pass


print(fullTeamName("reds"))