#!/usr/bin/env python3

from multiprocessing import Process, Queue # for userstats
from threading import Thread
import sqlite3 # database stuff
import threading # for the quit thread
import time
import stats
import alert
import praw
import warnings

try:
	import dbt
except ImportError:
	dbt_enabled = False

# Doesn't actually log, just prints a message to the console
#  with the current date and time.
def log(*msg, file=None):
	if file:
		print("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), msg), file=file)
	else:
		print("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), msg))

# Connects to the database. Creates it if it needs to.
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
			permalink TEXT
		);""")
	db.execute("""CREATE TABLE IF NOT EXISTS comments (
			id TEXT NOT NULL PRIMARY KEY UNIQUE,
			parent_id TEXT,
			author TEXT,
			body TEXT,
			udate DATE NOT NULL,
			permalink TEXT,
			score INT
		);""")
	return db

# Contains main loop. Pulls comments and submissions and stores them.
# db: database
# sub: subreddit object to poll
# thread: 
def monitor(db, sub, quit_thread):
	
	while True:
		#log("Getting comments")
		cs = sub.get_comments(limit=16)
		#log("Got comments")
		try:
			for c in cs:
				# create query string
				created = time.strftime("%Y-%m-%d %X",time.gmtime(c.created_utc))
				l_created = time.strftime("%Y-%m-%d %X",time.localtime(c.created_utc))
				query = """INSERT INTO comments
					(id, parent_id, author, body, udate, permalink)
					VALUES (?, ?, ?, ?, '%s', ?);""" % created
				author = c.author.name if c.author != None else "[deleted]"
				data = (c.name, c.parent_id, author, c.body, c.permalink,)
				try:
					db.execute(query,data) # attempt to execute query
					# if dbt_enabled: # build the userstats page if the stuff is enabled
					# 	if author != "[deleted]": # This 'user' doesn't get a page.
					# 		p = Process(target=dbt.buildPage, args=(author,))
					# 		p.start()
					print("-%s: %s by %s" % (l_created, c.name, author))
				except sqlite3.IntegrityError as ex:
					#print("." + c.name)
					break # IntegrityError means there was already a matching entry in the db.
					# In that case, just do nothing.
				#Thread(target=alert.process, args=(c.permalink, author, c.body, False, c.parent_id)).start()
				if not quit_thread.is_alive():
					break # exit the loop if the thread is done
				time.sleep(1)

			db.commit() # save db

		except Exception as ex:
			log(ex) # something went wrong, print it to console and carry on
		
		if not quit_thread.is_alive(): 
			log("Stopping")
			break # exit the loop if the thread is done

		ps = sub.get_new(limit=12)
		try:
			for s in ps: 
				# create query string
				created = time.strftime("%Y-%m-%d %X",time.gmtime(s.created_utc))
				l_created = time.strftime("%Y-%m-%d %X",time.localtime(s.created_utc))
				query = """INSERT INTO submissions
					(id, title, author, selftext, url, udate, permalink)
					VALUES (?, ?, ?, ?, ?, '%s', ?);""" % created
				author = s.author.name if s.author != None else "[deleted]"
				data = (s.name, s.title, author, s.selftext, s.url, s.permalink,)
				try:
					db.execute(query,data) # attempt to execute query
					print("-%s: %s by %s" % (l_created, s.name, author))
				except sqlite3.IntegrityError as ex:
					break # IntegrityError means there was already a matching entry in the db.
					# In that case, just do nothing.
				#Thread(target=alert.process, args=(s.permalink, author, s.body, True, None)).start()
				if not quit_thread.is_alive():
					break # exit the loop if the thread is done
				time.sleep(1)

			db.commit() # save db


		except Exception as ex:
			log(ex) # something went wrong, print it to console and carry on

		if not quit_thread.is_alive():
			log("Stopping")
			break # exit the loop if the thread is done

	db.close()

# This one runs in a separate thread.
# Waits for user to type "q" and press enter.
def wait():
	while input() != "q":
		pass
	print("Saving...")

def do_stats(queue):
	while queue.empty():
		s = stats.process()
		for i in range(s):
			if not queue.empty():			
				break
			time.sleep(1)

def main():
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		dbt_enabled = False # Disable userstats page creation (resource-heavy)
		# included as long as Pizza's site is broken

		r = praw.Reddit("watcher.py: comment gatherer: https://github.com/trambelus/plounge-db")
		sub = r.get_subreddit('mlplounge')

		db = init_db("plounge2.db3") # Connects to db, creates it if necessary
		quit_thread = threading.Thread(target=wait)
		quit_thread.start()
		print("Database connected")
		#queue = Queue()
		#Process(target=do_stats, args=(queue,)).start()
		monitor(db, sub, quit_thread) # setup done, start monitoring
		#queue.put('Done')

if __name__ == '__main__':
	main()