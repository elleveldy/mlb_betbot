from pinnacleClient import PinnacleClient
from commentFinder import updateMLBDailyDate
from format import updatePicksFromThread
from jsonFileHandler import pickFile, placedFile
import json
import time


class MLBBot():
	def __init__(self, username, password):
		self.pinnacle = PinnacleClient(username, password)

		self.availableBalance = 0
		self.outstandingTransactions = 0
		self.totalBankRoll = self.availableBalance + self.outstandingTransactions
		self.UNIT_PERCENTAGE = 0.05
		self.unit = 0.1
		self.minimumBetSize = 16
		self.currentMLBDailyDate = updateMLBDailyDate()


		self.events = self.pinnacle.getMLBOddsWithTeamNames()

	def get_availableBalance(self):
		return self.pinnacle.get_balance()['availableBalance']

	def get_oustandingTransactions(self):
		return self.pinnacle.get_balance()['oustandingTransactions']

	def updateEconomicStatus(self):
		balance = self.pinnacle.get_balance()
		self.availableBalance = balance['availableBalance']
		self.outstandingTransactions = balance['outstandingTransactions'] 
		self.totalBankRoll = self.availableBalance + self.outstandingTransactions
		self.unit = self.totalBankRoll*self.UNIT_PERCENTAGE
		if self.unit < self.minimumBetSize:
			self.unit = minimumBetSize
		print("\n******************\nEconomic status:")
		print("self.availableBalance: ", self.availableBalance )
		print("self.outstandingTransactions", self.outstandingTransactions) 
		print("self.totalBankRoll", self.totalBankRoll) 
		print("self.unit", self.unit)
		print("**********************") 

	def updateMLBevents(self):
		self.events = self.pinnacle.getMLBOddsWithTeamNames()


	# date and user should be unneccesary
	def placeBet(self, date, user, bet, stake):
		print("placedBet attempting to place:{}|{}|{}|{}".format(date,user,bet,stake))
		if not placedFile.hasBet(date, user, bet):
			# self.pinnacle.place_bet(bet, stake)
			placedFile.writeBet(date, user, bet)
			print("Placed bet: ", bet, "from user: ", user)
		else:
			print("Bet:", bet, "Already in file")

	def place_bet(self, bet, units):
		pass
		
	def find_bet(self, teamName, betType, spread = None):
		bet = {"sportId":str(3), "period": 0} #baseball sport id

		for event in self.events:
			if(teamName in event):
				bet['eventId'] = str(event['id'])
				bet['lineId'] = str(event['periods'][0]['lineId'])

				if(teamName == event['Team1']):
					bet['team'] = 'Team1'
				elif(teamName == event['Team2']):
					bet['team'] = 'Team2'

				if(betType == "SPREAD"):
					for pointSpread in event['periods'][2]['spreads']:
						if pointSpread['hdp'] == spread:
							bet['altLineId'] = pointSpread['altLineId']
							if(bet['team'] == 'Team1'):
								bet['odds'] = pointSpread['away']
							else:
								bet['odds'] = pointSpread['home']
				elif(betType == "MONEYLINE"):
					if(bet['team'] == "Team2"):
						bet['odds'] = event['periods'][0]['home']
					elif(bet['team'] == "Team1"):
						bet['odds'] = event['periods'][0]['away']
		return bet


	def oddsSatisfactory(self, pickOdds, betOdds):
		minimal_acceptable_odds_factor = 0.95
		if(float(betOdds)/float(pickOdds) >= minimal_acceptable_odds_factor):
			return True
		else:
			return False



username = "ED974228"
password = "#B0tSw4g9"



bot = MLBBot(username, password)
# while(1):
print(bot.oddsSatisfactory(1.56, 1.45))
# 	time.sleep(120)
# updatePicksFromThread("MLB Daily")
# bot.updateEconomicStatus()
# bot.updateMLBevents()

# availablePicks = pickFile.read()
# date = updateMLBDailyDate()
# if date in availablePicks:
# 	for user in availablePicks[date]:
# 		for bet in availablePicks[date][user]:
# 			if(not placedFile.hasBet(date, user, bet)):
# 				print("Date: {}, user: {}, bet: {} not in placedFile, placing bet...".format(date,user,bet))
# 				stake = float(bet['units']) * bot.unit
# 				bot.placeBet(date, user, bet, stake)
# 			else:
# 				print("Bet already in placedFile")
# 				continue

# print (json.dumps(bot.events, sort_keys=True, indent=4, separators=(',', ': ')))