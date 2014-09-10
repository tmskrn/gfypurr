# todo: 
# collect all post id's that i've posted on and read them out first
# move on to new and look for fresh posts with >10 upvotes
# improve the message layout
# tidy up code
# only post replies to users requesting a gfycat mirror

import re
import praw
import time
import requests
import ConfigParser
import json
from pprint import pprint
config = ConfigParser.ConfigParser()

praw = praw.Reddit('gfypurr: bot to search for gifs and rehost them on gfycat.')

config.read('gfypurr_config.cfg')
praw.login(config.get('login', 'username'), config.get('login', 'password'))

already_done = set()
subreddits = config.get('settings', 'subreddits').split(',')

def main():
	running = True
	while running:
		for sr in subreddits:
			try:
				subreddit = praw.get_subreddit(sr)
				# for submission in subreddit.get_hot(limit=50):
				#  	if not submission.id in already_done and not sr == 'soccer' or 'gifs' or 'funny':
				#  		find_post_add_comment(submission)
				for submission in subreddit.get_new(limit=100):
					if time.time() - submission.created_utc < 10800 and submission.score > 10 \
						and not submission.id in already_done:
						find_post_add_comment(submission)
				print '/r/%s done.' % subreddit
				time.sleep(2)
			except KeyboardInterrupt:
				running = False
				print "Script interrupted by user."
				break

def find_post_add_comment(submission):
	if '.gif' in submission.url and not 'gfycat' in submission.url:
		gfy_url = get_gfycat(submission)
		submission.add_comment('[gfycat mirror](%s) \n\n I am automatic. If you are unhappy with what I do, shoot me a message.' % gfy_url)
		print ('successfully added comment on: \'%s\'' % submission.title)
		time.sleep(float(config.get('settings', 'wait')))	

def get_gfycat(submission):
	print(submission.title, time.strftime("%Y-%m-%d %H:%M:%S"))
	gfycat_response = requests.get('http://upload.gfycat.com/transcode?fetchUrl=%s' % submission.url).json()
	gfy_url = 'http://www.gfycat.com/%s' % gfycat_response["gfyname"]
	already_done.add(submission.id)
	print gfy_url
	return gfy_url

main()