import praw


reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("sportsbook")

def topLevelCommentFrom(subtitle, username):
	#returns unformatted comment from thread, user
	thread = -1
	for submission in subreddit.hot(limit=20):
		if(subtitle in submission.title):
			print("Looking for comments in: ", submission.title)
			thread = submission
			break
	if(thread == -1):
		print("topLevelCommentFrom({}, {}) ERROR: thread not found").format(subtitle, username)
		return -1

	for top_level_comment in thread.comments:
		print (top_level_comment)
		if(top_level_comment.author in [username]):
			return top_level_comment.body
			
	print("topLevelCommentFrom(", username, ") ERROR: No top level comment found")
	return -1

def americanToEuropeanDate(date):
	month, day, year = date.split('/')
	return str(day)+"/"+month+"/"+year

def updateMLBDailyDate():
	for submission in subreddit.hot(limit=20):
		if("MLB Daily" in submission.title):
			rawDate = submission.title.split('-')[1].split(" ")[1]
			break
	return americanToEuropeanDate(rawDate)