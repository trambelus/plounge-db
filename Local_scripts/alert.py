#!/usr/bin/env python

import rlogin
import sqlite3
import string
import rlogin
import praw
import time

def mention_notify(r, url, user, author, body, abbreviated=False):
	a2 = ''.join([o if o != '_' else '\_' for o in author])
	body = ''.join([o if o != '_' else '\_' for o in body])
	if abbreviated:
		r.send_message('%s' % user,'%s mentioned you!' % author,"[](/telegram) Link [here.](%s)" % url)
	else:
		r.send_message('%s' % user,'%s mentioned you!' % author,"[](/telegram) Link [here.](%s)\n\n%s said:\n\n[](/sp)\n\n-----\n\n%s\n\n[](/sp)\n\n-----\n\n^(Note: This is a PM. To opt out of these notifications, PM this account with 'disable' in the subject.)" % (url,a2,body))
	print(("Notified %s!" % user))

def process(url, author, body, is_selftext, parent_id):
	r = praw.Reddit('alerts.py: plounge alerter: https://github.com/trambelus/plounge-db')
	userspace = string.ascii_letters + string.digits + '_-/'
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
		if '/' in username:
			username = username[:username.find('/')]

		if author == username:
			continue
		if not is_selftext and str(r.get_info(thing_id=parent_id).author) == username:
			continue

		if len(usernames) >= 8:
			mention_notify(r, url, username, author, body, True)
			time.sleep(1)
		elif is_selftext or (len(usernames) > 3):
			mention_notify(r, url, username, author, body, False)
			time.sleep(1)

		
def special(author, url, body):
	userspace = string.ascii_letters + string.digits + '_-/'
	usernames = [s[3:] for s in ''.join([o if o in userspace else ' ' for o in body]).split() if s[:3] == '/u/']
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
		mention_notify(r, url, username, author, body, False)



if __name__ == '__main__':
	# special(t_author,t_url,t_body)
	pass