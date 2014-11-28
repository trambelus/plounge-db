import sqlite3
import time
import rlogin
import ftplib
import datetime
UPDATE_INTERVAL = 3600

def log(msg):
	print("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), msg))

def buildPage(user):

	with open('user_update_cache.txt','r') as f:
		lastupdated = [s.split(" ") for s in f.readlines() if s != '\n' and ' ' in s]
	lu = dict(lastupdated)
	if user in lu and time.time() - int(lu[user]) < UPDATE_INTERVAL:
		return
	lu[user] = str(int(time.time()))+'\n'
	with open('user_update_cache.txt','w') as f:
		f.write("".join([" ".join(map(str,[t_usr, t_time])) for t_usr, t_time in lu.iteritems()]))

	s = "jQuery(function($){Morris.Area({element:'morris-area-chart',data:["
	db = sqlite3.connect('plounge.db3')
	for i in range(24):
		lc = len(db.execute("""SELECT * FROM comments WHERE author = ? 
				AND time(udate) > time('%02d:00') 
				AND time(udate) < time('%02d:00');""" % (i, i+1), (user,)).fetchall())
		ls = len(db.execute("""SELECT * FROM submissions WHERE author = ? 
				AND time(udate) > time('%02d:00') 
				AND time(udate) < time('%02d:00');""" % (i, i+1), (user,)).fetchall())
		s = s + "{period:'%02d:00',comments:%d,posts:%d}," % (i, lc, ls)
	s = s + """],xkey:'period',ykeys:['comments','posts'],labels:['Comments','Posts'],pointSize:2,hideHover:'auto',resize:true,parseTime:false});Morris.Area({element:'morris-area-chart-2',data:["""
	
	date_iter = datetime.date(2014,10,16)
	date_today = datetime.date.today()
	delta = datetime.timedelta(days=1)
	while date_iter < date_today:
		dt = date_iter.strftime("%Y-%m-%d")
		lc = len(db.execute("""SELECT * FROM comments WHERE author = ? 
				AND DATE(udate) = DATE('%s');""" % dt, (user,)).fetchall())
		ls = len(db.execute("""SELECT * FROM submissions WHERE author = ? 
				AND DATE(udate) = DATE('%s');""" % dt, (user,)).fetchall())
		s = s + ("""{period:'%s',comments:%d,posts:%d},""" % (dt, lc, ls))
		date_iter += delta

	
	# lc = db.execute("SELECT DATE(udate), COUNT(*) AS n FROM comments WHERE author = ? AND udate > date('2014-10-18') GROUP BY DATE(udate)", (user,)).fetchall()
	# da = dict(lc)
	# ls = db.execute("SELECT DATE(udate), COUNT(*) AS n FROM submissions WHERE author = ? AND udate > date('2014-10-18') GROUP BY DATE(udate)", (user,)).fetchall()
	# for k in da:
	# 	da[k] = [da[k], 0]
	# for st in ls:
	# 	da[st[0]] = [da[st[0]][0] if st[0] in da else 0, st[1]]
	# it = iter(sorted(da.iteritems()))
	# for el in it:
	# 	s = s + ("""{
 #            period: '%s',
 #            comments: %d,
 #            posts: %d
 #        },""" % (el[0], el[1][0], el[1][1]))

	
	s = s + """],xkey:'period',ykeys:['comments','posts'],labels:['Comments','Posts'],pointSize:2,hideHover:'auto',resize:true,parseTime:false});"""

	q1 = db.execute("SELECT author, COUNT(*) AS n FROM comments WHERE parent_id IN (SELECT id FROM comments WHERE author = '%s') GROUP BY author ORDER BY n DESC LIMIT 25" % user).fetchall()
	s1 = "".join(['<tr><td>%s</td><td>%d</td>' % (el[0], el[1]) for el in q1])
	q2 = db.execute("SELECT author, COUNT(*) AS n FROM comments WHERE id IN (SELECT parent_id FROM comments WHERE author = '%s') GROUP BY author ORDER BY n DESC LIMIT 25" % user).fetchall()
	s2 = "".join(['<tr><td>%s</td><td>%d</td>' % (el[0], el[1]) for el in q2])

	s = s + """document.getElementById("UsersWhoReplied").innerHTML='<table><tr><th>Users who replied to this user</th><th>Times</th></tr>%s</table>';document.getElementById("UsersRepliedTo").innerHTML='<table><tr><th>Users this user replied to</th><th>Times</th></tr>%s</table>';});""" % (s1, s2)

	ftp = rlogin.getFTP()
	rlogin.FTPlogin(ftp)
	ftp.cwd('userstats')
	with open('userstats\\%s.js' % user,'w') as f:
		f.write(s)
	with open('userstats\\%s.js' % user,'r') as f:
		ftp.storbinary('STOR %s.js' % user, f)
	print("%s.js transfer successful" % user)

	
	
def main():
	buildPage('Morichalion')

if __name__ == '__main__':
	main()



#SELECT DATE(udate) AS d, COUNT(*) as subs, NULL as coms FROM submissions WHERE author = 'BurlyHermit' GROUP BY d
#UNION
#SELECT DATE(udate) AS d, NULL as subs, COUNT(*) as coms FROM comments WHERE author = 'BurlyHermit' GROUP BY d
#ORDER BY d;
# most popular PLoungers
#select author, count(*) as n from comments where id in (select parent_id from comments) group by author order by n desc