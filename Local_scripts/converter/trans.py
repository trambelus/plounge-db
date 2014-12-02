#!/usr/bin/env python

import sqlite3
import MySQLdb

sdb = sqlite3.connect("plounge.db3");
db = MySQLdb.connect(host="107.152.101.194", # your host, usually localhost
                     user="muffinne_prank", # your username
                      passwd="gamie", # your password
                      db="muffinne_prankings") # name of the data base


# Comments: id, parent_id, author, body, udate, permalink

cur = db.cursor() 		
cur.execute("""CREATE TABLE IF NOT EXISTS comments (id MEDIUMINT NOT NULL AUTO_INCREMENT, parent_id TEXT, author TEXT, body TEXT, udate DATE NOT NULL, permalink TEXT, PRIMARY KEY (id))""")
cur.execute("""CREATE TABLE IF NOT EXISTS submissions (id MEDIUMINT NOT NULL AUTO_INCREMENT, author TEXT, title TEXT, selftext TEXT, url TEXT, udate DATE NOT NULL, permalink TEXT, PRIMARY KEY (id))""")


print("Grabbing comments...")
db_list = sdb.execute("SELECT * FROM comments;").fetchall()
total = len(db_list)
i = 0
for comment in db_list:
	cur.execute("INSERT OR IGNORE INTO comments VALUES (?,?,?,?,?,?);", tuple(comment))
	if i % 1000 == 0:
		print("%d%% complete" % (50*float(i)/total))
	i = i + 1
ddb.commit()

# Submissions: id, title, author, selftext, url, udate, permalink

print("Grabbing submissions...")
sub_list = sdb.execute("SELECT * FROM submissions;").fetchall()
total = len(sub_list)
i = 0
for sub in sub_list:
	cur.execute("INSERT OR IGNORE INTO submissions VALUES (?,?,?,?,?,?,?);", tuple(sub))
	if i % 1000 == 0:
		print("%d%% complete" % (50*float(i)/total+50))
	i = i + 1