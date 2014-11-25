#!/usr/bin/env python

from multiprocessing import Process
import sqlite3
import threading
import time
import rlogin
import dbt

def log(msg):
	print("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), msg))

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

		cs = sub.get_comments(limit=16)
		try:
			for c in cs:
				query = """INSERT INTO comments
					(id, parent_id, author, body, udate, permalink)
					VALUES (?, ?, ?, ?, '%s', ?);""" % time.strftime("%Y-%m-%d %X",time.gmtime(c.created-46800))
				author = c.author.name if c.author != None else "[deleted]"
				data = (c.name, c.parent_id, author, c.body, c.permalink,)
				try:
					db.execute(query,data)
					if author != "[deleted]":
						p = Process(target=dbt.buildPage, args=(author,))
						p.start()
					print("%s: new comment by %s" % (time.strftime("%Y-%m-%d %X",time.gmtime(c.created-46800)),author))
				except sqlite3.IntegrityError as ex:
					pass

				if not thread.is_alive():
					break

			db.commit()
		except Exception as ex:
			log(ex)
		
		if not thread.is_alive():
			break

		ps = sub.get_new(limit=16)
		try:
			for s in ps:
				query = """INSERT INTO submissions
					(id, title, author, selftext, url, udate, permalink)
					VALUES (?, ?, ?, ?, ?, '%s', ?);""" % time.strftime("%Y-%m-%d %X",time.gmtime(s.created-46800))
				author = s.author.name if s.author != None else "[deleted]"
				data = (s.name, s.title, author, s.selftext, s.url, s.permalink,)
				try:
					db.execute(query,data)
					print("%s: new submission by %s" % (time.strftime("%Y-%m-%d %X",time.gmtime(s.created-46800)),author))
				except sqlite3.IntegrityError as ex:
					pass
				if not thread.is_alive():
					break
			db.commit()
		except Exception as ex:
			log(ex)

		if not thread.is_alive():
			break


	db.close()

def wait():
	while raw_input() != "q":
		pass
	print("Saving...")

def main():
	[r, sub] = rlogin.login()
	print("Login successful")
	db = init_db("plounge2.db3")
	thread = threading.Thread(target=wait)
	thread.start()
	monitor(db, sub, thread)

if __name__ == '__main__':
	main()