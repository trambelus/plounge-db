#!/usr/bin/env python
# An Apple Bloom a day keeps the haters at bay

import time
import rlogin
import os
import sys

INCLUDE_POST_NUMS = False

def main():
	# Holds every line of the file
	file_strs = []
	# Import file
	with open(os.path.join(sys.path[0],'dailybloom.txt'),'r') as f:
		file_strs = [s.rstrip() for s in f.readlines()]
	# Get local current time in struct_time (tuple) format
	lt = time.localtime()
	# Compare date portion of tuple to what's in the file
	if lt[:3] == tuple(map(int,file_strs[0].split('-'))):
		print("Already posted today; exiting")
		return
	# Obtain Reddit and subreddit from praw via rlogin
	[r, sub] = rlogin.login('__brony__')
	# Which Bloom are we on today?
	index = int(file_strs[1])
	# Trim list to submissions only; separate titles and URLs 
	submissions = [s.split('\t') for s in file_strs[2:]]
	# If we've gone through all the file entries, exit.
	if len(submissions) <= index-3:
		print("No submissions left in file!")
		return
	# Construct post title
	title = submissions[index-3][0]
	if INCLUDE_POST_NUMS:
		title = 'Daily Bloom #%d: %s' % (index, submissions[index-3][0])
	url = submissions[index-3][1]
	# Print to confirm
	print(title)
	print(url)
	# Update information to put back in the file
	file_strs[1] = str(index+1)
	file_strs[0] = time.strftime('%Y-%m-%d')
	# The big line. Submit to the PLounge.
	r.submit(sub, title, url=url, send_replies=True)
	# Writeback
	with open('dailybloom.txt','w') as f:
		f.write('\n'.join(file_strs))

if __name__ == '__main__':
	main()