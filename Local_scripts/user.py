#!/usr/bin/env python
import praw
import sqlite3
import re
import time
import sys

def log(msg):
	print(("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), msg)))

def init_db(filename):
	db = sqlite3.connect(filename)
	# Above line creates the file if it doesn't exist
	# Lines below add the tables if they don't exist
	db.execute("""CREATE TABLE IF NOT EXISTS submissions (
			id TEXT NOT NULL PRIMARY KEY UNIQUE,
			author TEXT,
			title TEXT,
			selftext TEXT,
			url TEXT,
			udate DATE NOT NULL,
			permalink TEXT,
			subreddit TEXT,
			score INT
		);""")
	db.execute("""CREATE TABLE IF NOT EXISTS comments (
			id TEXT NOT NULL PRIMARY KEY UNIQUE,
			parent_id TEXT,
			author TEXT,
			body TEXT,
			udate DATE NOT NULL,
			permalink TEXT,
			subreddit TEXT,
			score INT
		);""")
	return db

def update_all(r, db, user):
	for sort_order in ['hot','new','top','controversial']:
		cs = user.get_comments(sort=sort_order, limit=1000)
		for c in cs:
			try:
				created = time.strftime("%Y-%m-%d %X",time.gmtime(c.created-46800))
				query = """INSERT INTO comments
						(id, parent_id, author, body, udate, permalink, subreddit, score)
						VALUES (?, ?, ?, ?, '%s', ?, ?, ?);""" % created
				author = c.author.name if c.author != None else "[deleted]"
				subreddit = re.search('/r/(.*?)/',c.permalink).group(0)[3:-1]
				data = (c.name, c.parent_id, author, c.body, c.permalink, subreddit, c.score)
				try:
					db.execute(query,data)
					print("-%s: comment by %s on %s" % (created,author,subreddit))
				except sqlite3.IntegrityError as ex:
					continue
			except Exception as ex:
				log(ex)
			db.commit()

def main(username):
	r = praw.Reddit('user.py: user comment saver: http://github.com/trambelus/plounge-db')
	db = init_db('%s.db3' % username)
	user = r.get_redditor(username)
	update_all(r,db,user)

if __name__ == '__main__':
	main(sys.argv[1])