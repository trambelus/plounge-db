#!/usr/bin/env python
# Prints out PLounge stats and stuff
import sqlite3
import ftplib
import rlogin
import time
import os

def log(msg):
	print("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), msg))

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
		log("Merging databases...")
		db = sqlite3.connect('plounge.db3')
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
		log("Merge successful.")
		log("Building stats list...")

		# statsWeek
		l = db.execute("SELECT author, count(*) FROM comments WHERE udate > datetime('now','-7 days', 'localtime') AND author != '[deleted]' GROUP BY author ORDER BY count(*) DESC").fetchall()
		with open("statsWeek.txt",'w') as f:
			stats = ["<tr><td>%d</td><td>%s</td><td>%d</td></tr>" % tuple([i+1]+list(l[i])) for i in range(len(l))]
			f.write("\n".join(stats))
		# with open("statsWeekA.txt",'w') as f:
		# 	stats = ["%d:%s:%d" % tuple([i+1]+list(l[i])) for i in range(len(l))]
		# 	f.write("\n".join(stats))
		ftp = rlogin.getFTP()

		# statsDay
		l = db.execute("SELECT author, count(*) FROM comments WHERE udate > datetime('now','-1 days', 'localtime') AND author != '[deleted]' GROUP BY author ORDER BY count(*) DESC").fetchall()
		with open("statsDay.txt",'w') as f:
			stats = ["<tr><td>%d</td><td>%s</td><td>%d</td></tr>" % tuple([i+1]+list(l[i])) for i in range(len(l))]
			f.write("\n".join(stats))
		#with open("statsDayA.txt",'w') as f:
		#	stats = ["%d:%s:%d" % tuple([i+1]+list(l[i])) for i in range(len(l))]
		#	f.write("\n".join(stats))

		log("Connecting to Pizza's server...")
		log(rlogin.FTPlogin(ftp))
		for f_ in ['statsWeek.txt','statsDay.txt']:
			with open(f_,'r') as f:
				ftp.storbinary('STOR %s' % f_, f)
				log("%s transfer successful." % f_)

		with open("lastUpdated.txt", 'w') as f:
			f.write(time.strftime("%Y-%m-%d %X") + " EST")
		with open("lastUpdated.txt", 'r') as f:
			ftp.storbinary('STOR lastUpdated.txt', f)

		# ftp.cwd('admin')
		# for f_ in ['statsWeekA.txt','statsDayA.txt']:
		# 	with open(f_,'r') as f:
		# 		ftp.storbinary('STOR %s' % f_, f)
		# 		log("%s transfer successful." % f_)
		db.close()
		ftp.quit()
		log("Sleeping...")
		time.sleep(300)

if __name__ == '__main__':
	main()

# Most frequent replier:
# select author, count(*) as n from comments where parent_id in (select id from comments where author = '%s') group by author order by n desc
# Most frequently replied to:
# select author, count(*) as n from comments where id in (select parent_id from comments where author = '%s') group by author order by n desc
# Emotes:
# select body as b, count(*) as n from comments where body like '[%](/%)%' group by b order by n desc

			#["    %3d: %20s: %d" % tuple([i+1]+list(l[i])) for i in range(len(l))]