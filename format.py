from commentParser import *
from commentFinder import topLevelCommentFrom, updateMLBDailyDate
import pprint
from jsonFileHandler import pickFile, placedFile

date = "27.06.17"


handicappers = {
	"MLB": ["ratbehr", "insiderlocks"]
}


def parse_Ndborro(comment):
	return "Ndborro: "+ comment

def parse_FadeTheTrap(comment):
	return "FadeTheTrap: "+ comment

#dictionary to pick correct parse fucntion from commentParser
extractPicksFromComment = {
	"ratbehr": parse_ratbehr,
	"insiderlocks": parse_insiderlocks,
	"Ndborro": parse_Ndborro,
	"FadeTheTrap": parse_FadeTheTrap,

}



def updatePicksFromUser(thread, user):
	rawComment = topLevelCommentFrom(thread, user)
	if(rawComment == -1):
		print("updatePicksFromUser({},{}): no comment".format(thread, user))
		return
	betDict = extractPicksFromComment[user](rawComment)
	pprint.pprint(betDict)

	pickFile.writeBets(betDict)


	return betDict

def updatePicksFromThread(thread):
	for key in handicappers:
		if(key in thread):
			for user in handicappers[key]:
				updatePicksFromUser(thread, user)





