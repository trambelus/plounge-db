#!/usr/bin/env python

import sqlite3

sdb = sqlite3.connect("plounge.db3");
ddb = sqlite3.connect("plounge_transfer_test.db3");

# Comments: id, parent_id, author, body, udate, permalink

ddb.execute("""CREATE TABLE IF NOT EXISTS comments (
			id TEXT NOT NULL PRIMARY KEY UNIQUE,
			parent_id TEXT,
			author TEXT,
			body TEXT,
			udate DATE NOT NULL,
			permalink TEXT
		)""")

ddb.execute("""CREATE TABLE IF NOT EXISTS submissions (
			id TEXT NOT NULL PRIMARY KEY UNIQUE,
			author TEXT,
			title TEXT,
			selftext TEXT,
			url TEXT,
			udate DATE NOT NULL,
			permalink TEXT
		)""")

print("Grabbing comments...")
db_list = sdb.execute("SELECT * FROM comments;").fetchall()
total = len(db_list)
i = 0
for comment in db_list:
	ddb.execute("INSERT OR IGNORE INTO comments VALUES (?,?,?,?,?,?);", tuple(comment))
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
	ddb.execute("INSERT OR IGNORE INTO submissions VALUES (?,?,?,?,?,?,?);", tuple(sub))
	if i % 1000 == 0:
		print("%d%% complete" % (50*float(i)/total+50))
	i = i + 1
ddb.commit()
ddb.close()