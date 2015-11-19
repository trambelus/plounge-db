#!/usr/bin/env python
# Prints out PLounge stats and stuff
import sqlite3
import ftplib
import rlogin
import time
import os
import shutil

def log(msg):
	print(("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), str(msg))))

def sendPage(filename):
	ftp = rlogin.getFTP()
	rlogin.FTPlogin(ftp)
	ftp.cwd('userstats')
	with open(filename,'r') as f:
		ftp.storbinary('STOR %s' % filename, f)
	ftp.quit()
	os.remove(filename)

def main():
	while True:
		s = process()
		time.sleep(s)

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
			permalink TEXT
		);""")
	return db
		
def process():
	db = None
	ftp = None
	try:
		log("Merging databases...")
		shutil.copy('plounge.db3','D:\\plounge.db3')
		db = init_db('plounge.db3')
		for s in ['plounge2.db3', 'plounge3.db3']:
			db.execute("attach '%s' as source;" % s)
			try:
				db.execute("""INSERT OR IGNORE INTO submissions
					(id, author, title, selftext, url, udate, permalink)
					SELECT id, author, title, selftext, url, udate, permalink
					FROM source.submissions;""")
				db.execute("""INSERT OR IGNORE INTO comments
					(id, parent_id, author, body, udate, permalink)
					SELECT id, parent_id, author, body, udate, permalink
					FROM source.comments;""")
			except sqlite3.Error as err:
				log(" ".join(["Error:",str(type(err)),'\n',str(err)]))
			db.execute("detach source;")
			log('%s complete' % s)

		try:
			db.execute("attach 'ds_tmp.db3' as sdb;")
			db.execute("""REPLACE INTO comments
				(id, parent_id, author, body, udate, permalink, score)
				SELECT comments.id, comments.parent_id, comments.author, comments.body, comments.udate, comments.permalink, sdb.scores.score
				FROM sdb.scores INNER JOIN comments ON (sdb.scores.id = comments.id)
				""")
			db.execute("detach sdb;")
			log('ds_tmp.db3 complete')
		except sqlite3.Error as err:
			log(" ".join(["ds_tmp.db3 error: ",str(err)]))
		log("Building stats list...")

		# statsWeek (comments)
		l = db.execute("SELECT author, count(*) FROM comments WHERE udate > datetime('now','-7 days', 'localtime') AND author != '[deleted]' AND body != ';-;' GROUP BY author ORDER BY count(*) DESC").fetchall()
		with open("statsWeek.txt",'wb') as f:
			stats = ["<tr><td>%d</td><td>%s</td><td>%d</td></tr>" % tuple([i+1]+list(l[i])) for i in range(len(l))]
			f.write(bytes("\n".join(stats),'UTF-8'))
		# with open("statsWeekA.txt",'w') as f:
		# 	stats = ["%d:%s:%d" % tuple([i+1]+list(l[i])) for i in range(len(l))]
		# 	f.write("\n".join(stats))

		# statsDay (comments)
		l = db.execute("SELECT author, count(*) FROM comments WHERE udate > datetime('now','-1 days', 'localtime') AND author != '[deleted]' AND body != ';-;' GROUP BY author ORDER BY count(*) DESC").fetchall()
		with open("statsDay.txt",'wb') as f:
			stats = ["<tr><td>%d</td><td>%s</td><td>%d</td></tr>" % tuple([i+1]+list(l[i])) for i in range(len(l))]
			f.write(bytes("\n".join(stats),'UTF-8'))
		#with open("statsDayA.txt",'w') as f:
		#	stats = ["%d:%s:%d" % tuple([i+1]+list(l[i])) for i in range(len(l))]
		#	f.write("\n".join(stats))

		# statsWeek (submissions)
		l = db.execute("SELECT author, count(*) FROM submissions WHERE udate > datetime('now','-7 days', 'localtime') AND author != '[deleted]' GROUP BY author ORDER BY count(*) DESC").fetchall()
		with open("statsWeekS.txt",'wb') as f:
			stats = ["<tr><td>%d</td><td>%s</td><td>%d</td></tr>" % tuple([i+1]+list(l[i])) for i in range(len(l))]
			f.write(bytes("\n".join(stats),'UTF-8'))

		# statsDay (submissions)
		l = db.execute("SELECT author, count(*) FROM submissions WHERE udate > datetime('now','-1 days', 'localtime') AND author != '[deleted]' GROUP BY author ORDER BY count(*) DESC").fetchall()
		with open("statsDayS.txt",'wb') as f:
			stats = ["<tr><td>%d</td><td>%s</td><td>%d</td></tr>" % tuple([i+1]+list(l[i])) for i in range(len(l))]
			f.write(bytes("\n".join(stats),'UTF-8'))

		# beesWeek
		l = db.execute("SELECT author, COUNT(*) N, permalink FROM comments WHERE udate > datetime('now','-7 days', 'localtime') AND author != '[deleted]' AND (id LIKE '%5r') GROUP BY author ORDER BY n DESC").fetchall()
		with open("beesWeek.txt",'wb') as f:
			stats = ['<tr><td>%s</td><td>%s</td><td><a href="%s">Latest</a></td></tr>' % tuple(l[i]) for i in range(len(l))]
			f.write(bytes("\n".join(stats),'UTF-8'))
		#  OR id LIKE '%5s'
		# beesAll
		l = db.execute("SELECT author, COUNT(*) N, permalink FROM comments WHERE author != '[deleted]' AND (id LIKE '%5r') GROUP BY author ORDER BY n DESC").fetchall()
		with open("beesAll.txt",'wb') as f:
			stats = ['<tr><td>%s</td><td>%s</td><td><a href="%s">Latest</a></td></tr>' % tuple(l[i]) for i in range(len(l))]
			f.write(bytes("\n".join(stats),'UTF-8'))

		# beesRecent
		l = db.execute("SELECT author, udate, permalink FROM comments WHERE author != '[deleted]' AND (id LIKE '%5r') ORDER BY udate DESC").fetchall()
		with open("beesRecent.txt",'wb') as f:
			stats = ['<tr><td>%s</td><td>%s</td><td><a href="%s">Latest</a></td></tr>' % tuple(l[i]) for i in range(len(l))]
			f.write(bytes("\n".join(stats),'UTF-8'))

		# ;-;
		l = db.execute("SELECT author, count(*) FROM comments WHERE udate > datetime('now','-7 days', 'localtime') AND author != '[deleted]' AND body = ';-;' GROUP BY author ORDER BY count(*) DESC").fetchall()
		with open(";-;.txt",'wb') as f:
			stats = ["<tr><td>%d</td><td>%s</td><td>%d</td></tr>" % tuple([i+1]+list(l[i])) for i in range(len(l))]
			f.write(bytes("\n".join(stats),'UTF-8'))

		log("Connecting to server...")
		ftp = ftplib.FTP('mlplounge.science')
		log(ftp.login('plounge-stats',rlogin.find_pw('plounge-stats')))
		for f_ in ['statsWeek.txt','statsDay.txt','statsWeekS.txt','statsDayS.txt','beesWeek.txt','beesAll.txt','beesRecent.txt',';-;.txt']:
			with open(f_,'rb') as f:
				log(str(ftp.storbinary('STOR %s' % f_, f)) + " - %s" % f_)

		with open("lastUpdated.txt", 'w') as f:
			f.write(time.strftime("%Y-%m-%d %X") + " EDT (UTC-4)")
		with open("lastUpdated.txt", 'rb') as f:
			ftp.storbinary('STOR lastUpdated.txt', f)

		# ftp.cwd('admin')
		# for f_ in ['statsWeekA.txt','statsDayA.txt']:
		# 	with open(f_,'r') as f:
		# 		ftp.storbinary('STOR %s' % f_, f)
		# 		log("%s transfer successful." % f_)
	except Exception as ex:
		print(ex)
		return 45
	finally:
		if db:
			db.close()
		if ftp:
			ftp.quit()
	log("Sleeping...")
	return 300
		

if __name__ == '__main__':
	main()

# Most frequent replier:
# select author, count(*) as n from comments where parent_id in (select id from comments where author = '%s') group by author order by n desc
# Most frequently replied to:
# select author, count(*) as n from comments where id in (select parent_id from comments where author = '%s') group by author order by n desc
# Emotes:
# select body as b, count(*) as n from comments where body like '[%](/%)%' group by b order by n desc

			#["    %3d: %20s: %d" % tuple([i+1]+list(l[i])) for i in range(len(l))]

# db = mysql.connect(host='107.152.101.194',user='muffinne_prank',passwd='353BEQP15X',db='muffinne_prankings')

# # Self-replies:
# SELECT c.author AS a, COUNT(*) AS n FROM 
# comments AS c LEFT OUTER JOIN comments ON c.parent_id = comments.id
# WHERE a != '[deleted]'
# AND a = comments.author
# GROUP BY a ORDER BY n DESC