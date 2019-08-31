import requests, json, time
from plyer import notification
from collections import defaultdict
from sys import argv

def message(user):
  notification.notify (
    title = 'Codechef',
    message = user + ' is taking lead',
  )

class FriendSubmissionTracker(object):
	def __init__(self, contest_code, friendList, you):
		self.contest_code = contest_code
		friendList.append(you)
		self.friendList = friendList
		self.you = you

	def genrateRankList(self):
		contest_code = self.contest_code
		friendList = self.friendList
		friendRankList = []
		for friend in friendList:
			try:
				url = 'https://www.codechef.com/api/rankings/{}?search={}'.format(contest_code, friend)
				res = requests.get(url)
				res = res.json()
				res = res['list']
				if len(res) == 0:
					friendRankList.append([100000, friend])
					continue
				friendRankList.append([res[0]['rank'], friend])
			except Exception as e:
				break
		friendRankList.sort()
		return friendRankList

	def run(self):
		haveRank = defaultdict()
		friendList = self.friendList
		you = self.you
		for it in friendList:
			haveRank[it] = 1000000
		while True:
			ranklist = self.genrateRankList()
			temp = []
			yourRank = 0
			for it in ranklist:
				user = it[1]
				rank = it[0]
				if user == you:
					yourRank = rank
					break
			for it in ranklist:
				user = it[1]
				rank = it[0]
				if user == you:
					break
				if haveRank[user] > yourRank and rank < yourRank:
					message(user)
				haveRank[user] = rank


if __name__ == '__main__':
	# replace contest code as the current contest code
	if len(argv) > 1: # If there is  argument
		contest_code = argv[1]
	else:
		contest_code = input("Enter contest code : ")

	file = open('friendList.txt', 'r') 
	friendList = file.read()
	file.close()
	temp = list(friendList.split('\n'))
	friendList = list(temp)
	friendList = friendList[1:]
	file = open('yourHandle.txt', 'r') 
	your_handle = file.read()
	Contest = FriendSubmissionTracker(contest_code, friendList, your_handle)
	Contest.run()
