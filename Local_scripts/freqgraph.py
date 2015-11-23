#!/usr/bin/env python3

from silent import silent
with silent():
	import requests
	import sqlite3
	import rlogin
	import time
	from imgurpython import ImgurClient
	import sys
	import matplotlib as mp
	import matplotlib.pyplot as plt
	import numpy as np

DBNAME = 'plounge.db3'
DATES = 16
WIN_SZ = 25

def get_id_secret():
	ret = []
	with open('imgur_info.txt','r') as f:
		ret = [s.rstrip() for s in f.readlines()]
	return ret

def main():
	db = sqlite3.connect(DBNAME)
	[client_id, client_secret] = get_id_secret()
	client = ImgurClient(client_id, client_secret)
	while True:
		print("%s" % frequency_graph(db, sys.argv[1], client))
		return

def frequency_graph(db, kw, client):
	query = '''SELECT v1.ud, 100*CAST(nsp AS FLOAT)/ntl pct, nsp, ntl FROM
	(SELECT DATE(udate) ud, COUNT(*) ntl FROM comments c1
	  GROUP BY ud) v1
	LEFT OUTER JOIN
	(SELECT DATE(udate) ud, COUNT(*) nsp FROM comments c2
	  WHERE body LIKE '%%%ss%%' GROUP BY ud) v2
	ON v1.ud = v2.ud ORDER BY v1.ud'''
	res = db.execute(query % kw)
	data = list(map(list,zip(*[[i if i != None else 0 for i in j] for j in res])))
	dstart = next((i for i, x in enumerate(data[1]) if x), None)
	if dstart != None:
		data[0] = data[0][dstart:]
		data[1] = data[1][dstart:]

	w = [1.0/WIN_SZ]*WIN_SZ
	d2 = np.convolve(data[1],w,'valid')
	d2 = np.pad(d2, (WIN_SZ//2,0), 'minimum')
	ds = len(data[1])//DATES
	plt.figure(num=None, figsize=(16,9), dpi=100, facecolor='w', edgecolor='k')
	plt.plot(list(range(len(data[1]))), data[1])
	plt.plot(list(range(len(d2))), d2, color='r', linewidth=4)
	plt.xticks([i*ds for i in range(DATES)],[data[0][i*ds] for i in range(DATES)], rotation=45)
	plt.ylabel("Number of daily comments containing '%s'" % kw)
	plt.title("Frequency graph for %s" % kw)

	plt.savefig('freq\\%s.png' % kw)
	# Upload to Imgur
	imgur_response = client.upload_from_path('freq\\%s.png' % kw)
	return imgur_response['link']

if __name__ == '__main__':
	main()