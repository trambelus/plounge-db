import praw
import ftplib

def find_pw(username):
	with open('pw.txt','r') as f:
		stuff = f.readlines()
		ret = next(x[1] for x in [t.split('\t') for t in stuff] if x[0] == username).rstrip()
		return ret

def login(username):
	r = praw.Reddit("Watcher of the PLounge, by __brony__")
	sub = r.get_subreddit('mlplounge')
	r.login(username, find_pw(username))
	return [r, sub]

def getFTP():
	return ftplib.FTP('mlplounge.science')

def FTPlogin(ftp):
	return ftp.login('plounge-stats',find_pw('plounge-stats'))

def notify(url, user, subject="Notification!"):
	r = praw.Reddit("Little bot by __brony__ for general notifications")
	r.login('plounge_alert_bot', find_pw('plounge_alert_bot'))
	r.send_message('%s' % user,'%s' % subject,'Link [here!](%s)' % url)
	print("Notified %s!" % user)