#!/usr/bin/env python
# Gives a user's info: activity graphs, emotes, etc.

import requests
import sqlite3
import rlogin
import time
from imgurpython import ImgurClient
from collections import Counter
from wordcloud import WordCloud
import sys
import warnings

ID_LINK = '305kgd'
USERNAME = 'AboutThisPlounger'
DBNAME = 'plounge.db3'
# Word cloud options
FONT_PATH = 'C:\\Windows\\Fonts\\Helvetica.ttf'
WIDTH = 1280
HEIGHT = 720


def get_id_secret():
	ret = []
	with open('imgur_info.txt','r') as f:
		ret = [s.rstrip() for s in f.readlines()]
	return ret

def scan(sub):
	while True:
		posts = sub.get_new(limit=64)
		for s in posts:
			if ID_LINK in s.selftext and not already_commented(s):
				return s
	

def already_commented(s):
	return USERNAME in [rep.author.name for rep in s.comments if rep.author != None]

def word_cloud(db, user, client):
	# Grab comments
	res = db.execute("SELECT body FROM comments WHERE author = '%s'" % user)
	words = " ".join([r[0] for r in res]) # Make it all one big happy string
	# Generate and save the wordcloud	
	wc = WordCloud(font_path=FONT_PATH, width=WIDTH, height=HEIGHT)
	wc.generate(words)
	wc.to_file('wc\\%s.png' % user)
	# Upload to Imgur
	imgur_response = client.upload_from_path('wc\\%s.png' % user)
	return imgur_response['link']


def assemble_info(db, s, client):
	user = s.author.name
	query = '''SELECT v1.ud, 100*CAST(IFNULL(nsp,0) AS FLOAT)/ntl pct FROM
		(SELECT DATE(udate) ud, COUNT(*) ntl FROM comments c1
		GROUP BY ud) v1
		LEFT OUTER JOIN
		(SELECT DATE(udate) ud, COUNT(*) nsp FROM comments c2
		WHERE author = '%s' GROUP BY ud) v2
		ON v1.ud = v2.ud ORDER BY v1.ud'''


# Scans for AMAs, assembles all information, posts comment.
def main():
	#[r, sub] = rlogin.login(USERNAME)
	db = sqlite3.connect(DBNAME)
	[client_id, client_secret] = get_id_secret()
	client = ImgurClient(client_id, client_secret)
	while True:
		word_cloud(db, sys.argv[1], client)
		return
		#s = scan(sub)
		#assemble_info(db, s, client)

if __name__ == '__main__':
	warnings.filterwarnings("ignore")
	main()

# Old word cloud code:
	# import re
	# words = re.findall(r'\w+', words)
	# words = [w.rstrip().rstrip('.,?!\n') for w in words]
	# top_words = [' '.join([i[0]]*i[1]) for i in Counter(words).most_common(MAX_WORDS)]
	# print(len(top_words))
	# tw_clip = ' '.join(top_words[:MAX_WORDS])
	# # Create word cloud
	# url = "http://cloudmaker.gatheringpoint.com/index.php"
	# params = {"height":"720", "textblock":tw_clip, "height":"1280"}
	# #j = requests.get(url, params=params)
	# print(j)
	# img_url = j.json()['url']
	# print("Word cloud: ", img_url)
	# # Upload to imgur
	# imgur_response = client.upload_from_url(img_url, config=None, anon=True)