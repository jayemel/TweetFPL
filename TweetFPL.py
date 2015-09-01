#!/usr/bin/env python

## A quick and dirty twitter bot that automatically tweets FPL2015 information

import time, sched

MESSAGE_FILE = 'Schedule.csv'
START_TIME = time.time()

scheduler = shed.scheduler(time.time, time.sleep)

# Open the file and load messages into a list
messages = []
with open(MESSAGE_FILE) as f:
	for line in f:
		# Throw away comments
		if line[0] is not '#':
			# Split the line into a list
			data = line.split(';')
			# Convert the date and time into UTC
			trigger = time.mktime(time.strptime(' '.join(data[0:2]), '%d/%m/%Y %H:%M'))
			# Only accept future messages
			if (trigger > START_TIME):
				# Need to check if there is already a tweet at that time
				