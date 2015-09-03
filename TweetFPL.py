#!/usr/bin/env python

## A quick and dirty twitter bot that automatically tweets FPL2015 information

import time, sched, tweepy

# Import the twitter authentication credentials
from TweetFPLAuth import *

MESSAGE_FILE = 'Schedule.csv'
START_TIME = time.time()

def tweet_event(message):
	print "TWEET:", time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()), message
	twitter.update_status(status=message)

print 'Running TweetFPL, the FPL2015 twitter message server.\n'

# Set up the Twitter library
auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)
twitter = tweepy.API(auth)

# Start up the scheduler
scheduler = sched.scheduler(time.time, time.sleep)

# Open the file and load messages into a list
with open(MESSAGE_FILE) as f:
	for line in f:
		if line:
			# Throw away comments
			if line[0] is not '#':
				# Split the line into a list
				data = line.rstrip().split(';')
				# Check that the tweets aren't too long
				if len(data[-1]) > 140:
						print 'Tweet is too long:', data[-1]
						exit()
				# Convert the date and time into UTC
				trigger = time.mktime(time.strptime(' '.join(data[0:2]), '%d/%m/%Y %H:%M:%S'))
				# Only accept future messages
				if (trigger > START_TIME):
					# Register the trigger
					scheduler.enterabs(trigger, 1, tweet_event, (data[-1],))

# Run the scheduler
scheduler.run()
