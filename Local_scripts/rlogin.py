import praw
import ftplib
import requests

def find_pw(username):
	with open('pw.txt','r') as f:
		stuff = f.readlines()
		try:
			ret = next(x[1] for x in [t.split('\t') for t in stuff] if x[0] == username).rstrip()
		except StopIteration:
			raise LookupError("User not found: %s" % username)
		return ret

def login(username, subreddit='mlplounge'):
	r = praw.Reddit("Watcher of /r/%s, by /u/%s" % (subreddit, username))
	sub = r.get_subreddit(subreddit)
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

# -- New OAuth stuff

def find_app_info(app_name):
	with open('secrets.txt', 'r') as f:
		stuff = f.readlines()
		ret = [i.rstrip() for i in next(x[1:] for x in [t.split('\t') for t in stuff] if x[0] == app_name)]
		return ret

def set_auth(r, app_name, username, version):
	[client_id, client_secret, redirect_uri] = find_app_info(app_name)
	password = find_pw(username)
	client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
	post_data = {"grant_type": "password", "username": username, "password": password, "duration": "permanent"}
	headers = {"User-Agent": "{0}/{1} by {2}".format(app_name, version, username)}
	response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
	print(response.json())
	token = response.json()['access_token']
	r.set_oauth_app_info(client_id, client_secret, redirect_uri)
	r.set_access_credentials({'flair','privatemessages','submit'}, token)
	return token

def get_auth_r(username, app_name, version="2.0"):
	uas = "{0}/{1} by {2}".format(app_name, version, username)
	r = praw.Reddit(uas)
	set_auth(r, app_name, username, version)
	return r

if __name__ == '__main__':
	r = praw.Reddit('OAuth tests')
	print(set_auth(r, 'DailyBloom','Gummy_Bot'))
	sub = r.get_subreddit('test')
	r.submit(sub, "Testing new OAuth2 authentication", text="[](/gummy)")