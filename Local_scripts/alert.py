#!/usr/bin/env python

import rlogin
import sqlite3
import string
import rlogin
import praw
import time

def mention_notify(r, url, user, author, body, abbreviated=False):
	body = ''.join([o if o != '_' else '\_' for o in body])
	if abbreviated:
		r.send_message('%s' % user,'%s mentioned you!' % author,'[](/telegram) Link [here.](%s)' % url)
	else:
		r.send_message('%s' % user,'%s mentioned you!' % author,'[](/telegram) Link [here.](%s)\n\n%s said:\n\n[](/sp)\n\n-----\n\n%s' % (url,author,body))
	print(("Notified %s!" % user))

def process(url, author, body, is_selftext):
	userspace = string.letters + string.digits + '_-/'
	usernames = [s[3:] for s in ''.join([o if o in userspace else ' ' for o in body]).split() if s[:3] == '/u/']
	if len(usernames) == 0:
		return
	[r, sub] = rlogin.login()
	for username in list(set(usernames)):
		user = None
		try:
			user = r.get_redditor(username)
		except:
			continue
		if author == username:
			continue
		if '/' in username:
			username = username[:username.find('/')]
		if user.is_gold and (is_selftext or len(usernames) > 3):
			mention_notify(r, url, username, author, body, False)
			time.sleep(1)
		elif len(usernames) > 8:
			mention_notify(r, url, username, author, body, True)
			time.sleep(1)
		
def special(author, url, body):
	userspace = string.letters + string.digits + '_-/'
	usernames = [s[3:] for s in ''.join([o if o in userspace else ' ' for o in body]).split() if s[:3] == '/u/']
	[r, sub] = rlogin.login()
	for username in list(set(usernames)):
		try:
			user = r.get_redditor(username)
		except:
			continue
		mention_notify(r, url, username, author, body)

if __name__ == '__main__':
	pass