#!/usr/bin/env python

## A quick and dirty twitter bot that automatically tweets FPL2015 information

import time, sched

MESSAGE_FILE = 'Schedule.csv'
START_TIME = time.time()

def tweet_event(message):
	print "TWEET:", time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()), message

print 'Running TweetFPL, the FPL 2015 twitter message server.\n'

scheduler = sched.scheduler(time.time, time.sleep)

# Open the file and load messages into a list
messages = []
# Previous trigger time and default priority
priority = [0,1]
with open(MESSAGE_FILE) as f:
	for line in f:
		# Throw away comments
		if line[0] is not '#':
			# Split the line into a list
			data = line.rstrip().split(';')
			# Convert the date and time into UTC
			trigger = time.mktime(time.strptime(' '.join(data[0:2]), '%d/%m/%Y %H:%M'))
			# Only accept future messages
			if (trigger > START_TIME):
				# Check if there is already a tweet at that time
				if priority[0] is trigger:
					# Increment the priority
					priority[1] += 1
				else:
					# Reset the priority
					priority[1] = 1
				# Set the current trigger time
				priority[0] = trigger
				# Register the trigger
				scheduler.enterabs(priority[0], priority[1], tweet_event, (data[-1],))

# Run the scheduler
scheduler.run()