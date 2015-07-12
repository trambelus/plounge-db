#!/usr/bin/env python

import praw
import rlogin
import warnings
import time

USERNAME = 'Gummy_Bot'
STREAM_LINK = 'http://cytu.be/r/thebestpony'
SUBREDDIT = 'mylittlepony'
TERM = 'Reaction'
AUTHOR = 'Pinkie_Pie'
# SUBREDDIT = 'onetruekekerino'
# TERM = 'Reaction'
# AUTHOR = 'kekerino'
MODS = ['__brony__',
		'kekerino',
		'Orschmann',
		'optimistic_outcome',
		'Chinch335',
		'IllusionOf_Integrity',
		'Pathogen-David',
		'spokesthebrony',
		'TheeLinker',
		'Lankygit',
		'xHaZxMaTx',
		'Raging_Mouse',
		'DoomedCivilian']
AUTO = ['__brony__',
		'kekerino',
		'spokesthebrony',
		'TheeLinker',
		'Lankygit',
		'xHaZxMaTx',
		'Raging_Mouse',
		'DoomedCivilian']
# AUTO = []
CLOSE_MIN = 60
WARN_MIN = 1
WARN_MSG = "Automated warning: this Live thread will close in one minute."

def log(msg):
	print("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), msg))

def scan_for_thread(subreddit):
	while True:
		news = subreddit.get_new()
		for s in news:
			if s.author != None and s.author.name == AUTHOR and TERM.lower() in s.title.lower():
				log('Found thread with id %s' % s.name)
				return s

def scan_for_contributors(r, submission, thread, started):
	done = []
	warned = False
	closed = False
	while True:
		submission.refresh()
		coms = submission.comments
		for c in coms:
			if c.author == None:
				continue
			if c.author.name not in done:
				invite_contributor(r, c.author.name, thread)
				#done.append(c.author.name)
			if time.time() > started + (60 * (CLOSE_MIN-WARN_MIN)) and not warned:
				#update(r, thread, WARN_MSG)
				warned = True
			if time.time() > started + (60 * CLOSE_MIN):
				#close_thread(r, thread)
				return

def create_live_thread(r, title, permalink):
	url = 'http://www.reddit.com/api/live/create'
	resources = "[Unofficial stream link](%s)\n\n[Official reaction thread](%s)" % (STREAM_LINK, permalink)
	data = {
		'description':'/r/mylittlepony: Live %s' % title,
		'nsfw': False,
		'resources': resources,
		'title': title, 
	}
	res = r.request_json(url, data=data)
	ret = res['data']['id']
	log('Created live thread with id %s' % ret)
	return ret

def invite_contributor(r, contributor, thread):
	url = 'http://www.reddit.com/api/live/%s/invite_contributor' % thread
	if contributor in MODS:
		data = {
			'name': contributor,
			'permissions': '+all',
			'type': 'liveupdate_contributor'
		}
		log('Inviting %s with full permissions' % contributor)
	else:
		data = {
			'name': contributor,
			'permissions': '+update',
			'type': 'liveupdate_contributor'
		}
		log('Inviting %s with update permission' % contributor)
	try:
		r.request_json(url, data=data)
	except praw.errors.APIException as ex:
		print(ex)
		#log('Warning: duplicate invitee')
		pass

def update(r, thread, msg):
	log('Posting update: "%s"' % msg)
	url = 'http://www.reddit.com/api/live/%s/update' % thread
	data = { 'body': msg, }
	r.request_json(url, data=data)

def close_thread(r, thread):
	log('Closing thread')
	url = 'http://www.reddit.com/api/live/%s/close_thread' % thread
	data = {}
	r.request_json(url)


def main():
	[r, subreddit] = rlogin.login(USERNAME, subreddit=SUBREDDIT)
	submission = scan_for_thread(subreddit)
	#thread = create_live_thread(r, submission.title, submission.permalink)
	thread = 'uwyz7p30mw62'
	started = time.time()
	with open('autoadd.txt','r') as f:
		auto = AUTO + [i.rstrip() for i in f.readlines()]
	for user in set(auto):
		invite_contributor(r, user, thread)
	scan_for_contributors(r, submission, thread, started)

if __name__ == '__main__':
	warnings.filterwarnings("ignore")
	main()
	input()