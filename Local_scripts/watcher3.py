#!/usr/bin/env python3

import sqlite3
import threading
import time
import praw
import dbt
import stats

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

def monitor(db, sub, thread):

	while True:

		cs = sub.get_comments(limit=None)
		try:
			for c in cs:
				query = """INSERT INTO comments
					(id, parent_id, author, body, udate, permalink)
					VALUES (?, ?, ?, ?, '%s', ?);""" % time.strftime("%Y-%m-%d %X",time.gmtime(c.created_utc))
				l_created = time.strftime("%Y-%m-%d %X",time.localtime(c.created_utc))
				author = c.author.name if c.author != None else "[deleted]"
				data = (c.name, c.parent_id, author, c.body, c.permalink,)
				try:
					db.execute(query,data)
					# if author != "[deleted]":
					# 	dbt.buildPage(author);
					# 	stats.sendPage("%s.js" % author)
					print("%s: %s by %s" % (l_created, c.name, author))
				except sqlite3.IntegrityError as ex:
					pass

				if not thread.is_alive():
					break

			db.commit()
		except Exception as ex:
			print(ex)
			time.sleep(5)
		
		if not thread.is_alive():
			break

		ps = sub.get_new(limit=None)
		try:
			for s in ps:
				query = """INSERT INTO submissions
					(id, title, author, selftext, url, udate, permalink)
					VALUES (?, ?, ?, ?, ?, '%s', ?);""" % time.strftime("%Y-%m-%d %X",time.gmtime(s.created_utc))
				l_created = time.strftime("%Y-%m-%d %X",time.localtime(s.created_utc))
				author = s.author.name if s.author != None else "[deleted]"
				data = (s.name, s.title, author, s.selftext, s.url, s.permalink,)
				try:
					db.execute(query,data)
					print("%s: %s by %s" % (l_created, s.name, author))
				except sqlite3.IntegrityError as ex:
					pass
				if not thread.is_alive():
					break
			db.commit()
		except Exception as ex:
			print(ex)
			time.sleep(5)

		if not thread.is_alive():
			break

		#time.sleep(5)

	db.close()

def wait():
	while input() != "q":
		pass
	print("Saving...")

def main():
	r = praw.Reddit("watcher.py: comment gatherer: https://github.com/trambelus/plounge-db")
	sub = r.get_subreddit('mlplounge')
	db = init_db("plounge3.db3")
	thread = threading.Thread(target=wait)
	thread.start()
	monitor(db, sub, thread)

if __name__ == '__main__':
	main()