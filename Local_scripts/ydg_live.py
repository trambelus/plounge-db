#!/usr/bin/env python3
# File: ya_dun_goofed.py
# I hope no real programmers end up reading this

import sqlite3
import threading
import time
import rlogin
import praw
import sys

def init_db(filename):
	db = sqlite3.connect(filename)
	db.execute("""CREATE TABLE IF NOT EXISTS submissions (
			id TEXT NOT NULL PRIMARY KEY UNIQUE,
			author TEXT,
			title TEXT,
			selftext TEXT,
			url TEXT,
			udate DATE NOT NULL,
			permalink TEXT
		);""")
	db.execute("""CREATE TABLE IF NOT EXISTS comments (
			id TEXT NOT NULL PRIMARY KEY UNIQUE,
			parent_id TEXT,
			author TEXT,
			body TEXT,
			udate DATE NOT NULL,
			permalink TEXT
		);""")
	return db

def monitor(db, sub, thread, r, start="zzzzzz"):

	ps = sub.get_new(limit=None)
	for s in ps:
		try:
			print(s)
		except UnicodeEncodeError:
			print("(unprintable title)")

		tries = 3 # Attempt to process each submission three times.
		while tries > 0:
			try:
				query = """INSERT OR IGNORE INTO submissions
					(id, title, author, selftext, url, udate, permalink)
					VALUES (?, ?, ?, ?, ?, '%s', ?);""" % time.strftime("%Y-%m-%d %X",time.gmtime(s.created_utc))
				author = s.author.name if s.author != None else "[deleted]"
				data = (s.name, s.title, author, s.selftext, s.url, s.permalink,)
				db.execute(query,data)
				print(("%s: submission by %s" % (time.strftime("%Y-%m-%d %X",time.gmtime(s.created)),author)))
				def readcomments(s,l):
					for c in s:
						try:
							if type(c) == praw.objects.MoreComments:
								mc = c.comments()
								print("Loading %d more comment%s..." % (len(mc), "" if len(mc) == 1 else "s"))
								readcomments(mc,l+1)
								continue

							query = """INSERT OR IGNORE INTO comments
								(id, parent_id, author, body, udate, permalink)
								VALUES (?, ?, ?, ?, '%s', ?);""" % time.strftime("%Y-%m-%d %X",time.gmtime(c.created_utc))
							author = c.author.name if c.author != None else "[deleted]"
							data = (c.name, c.parent_id, author, c.body, c.permalink,)
							try:
								db.execute(query,data)
								print(("%s:%s %s (%s)" % (time.strftime("%Y-%m-%d %X",time.gmtime(c.created))," "*l,author,c.name)))
							except sqlite3.IntegrityError as ex:
								pass
							if not thread.is_alive():
								break
							readcomments(c.replies,l+1)
						except Exception as ex:
							print(ex)
				readcomments(s.comments,1)
				db.commit()
				if not thread.is_alive():
					break
				tries = 0 # Success!
			except Exception as ex:
				tries = tries - 1
				print(ex) # Probably a server error
				time.sleep(2) # Wait and hope for the best

	db.close()

def wait():
	while input() != "q":
		pass
	print("Saving...")

def main(argv):
	r = praw.Reddit('/r/mlplounge consolidation script')
	sub = r.get_subreddit('mlplounge')
	db = init_db("plounge4.db3") # This'll be consolidated by another script
	thread = threading.Thread(target=wait)
	thread.start()
	if len(argv) == 3 and argv[1] == '-s' and len(argv[2]) == 6:
		print("Starting at %s" % argv[2])
		monitor(db, sub, thread, r, argv[2])
	else:
		monitor(db, sub, thread, r)

if __name__ == '__main__':
	main(sys.argv)
	#24oq2k