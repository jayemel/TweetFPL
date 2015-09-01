#!/usr/bin/env python

## A quick and dirty twitter bot that automatically tweets FPL2015 information

import time, sched
from TweetFPLAuth import *

MESSAGE_FILE = 'Schedule.csv'
START_TIME = time.time()

def tweet_event(message):
	print "TWEET:", time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()), message

print 'Running TweetFPL, the FPL 2015 twitter message server.\n'

scheduler = sched.scheduler(time.time, time.sleep)

# Open the file and load messages into a list
messages = []
with open(MESSAGE_FILE) as f:
	for line in f:
		if line:
			# Throw away comments
			if line[0] is not '#':
				# Split the line into a list
				data = line.rstrip().split(';')
				# Convert the date and time into UTC
				trigger = time.mktime(time.strptime(' '.join(data[0:2]), '%d/%m/%Y %H:%M:%S'))
				# Only accept future messages
				if (trigger > START_TIME):
					# Register the trigger
					scheduler.enterabs(trigger, 1, tweet_event, (data[-1],))

# Run the scheduler
scheduler.run()