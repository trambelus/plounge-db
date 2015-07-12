#!/usr/bin/env python

import sqlite3
import matplotlib as mp
import matplotlib.pyplot as plt
import sys
import numpy as np

DATES = 16
WS = 25

QUERY = '''
SELECT v1.ud, 100*CAST(nsp AS FLOAT)/ntl pct, nsp, ntl FROM
(SELECT DATE(udate) ud, COUNT(*) ntl FROM comments c1
  GROUP BY ud) v1
LEFT OUTER JOIN
(SELECT DATE(udate) ud, COUNT(*) nsp FROM comments c2
  WHERE body LIKE '%%%s%%' GROUP BY ud) v2
ON v1.ud = v2.ud ORDER BY v1.ud
'''
DBPATH = 'plounge.db3'

def graph(trend, dbpath=DBPATH, savepath=None):
	if savepath == None:
		savepath = '%s.png' % trend
	db = sqlite3.connect(dbpath)
	data = db.execute(QUERY % trend).fetchall()
	data = list(map(list,zip(*[[i if i != None else 0 for i in j] for j in data])))
	w = [1.0/WS]*WS
	d2 = np.convolve(data[1],w,'valid')
	d2 = np.roll(d2, WS//2)
	print(data[1])
	ds = len(data[1])//DATES
	plt.figure(num=None, figsize=(16,9), dpi=100, facecolor='w', edgecolor='k')
	plt.plot(list(range(len(data[1]))), data[1])
	plt.plot(list(range(len(d2))), d2, color='r', linewidth=4)
	plt.xticks([i*ds for i in range(DATES)],[data[0][i*ds] for i in range(DATES)], rotation=45)
	plt.ylabel("Percentage of daily comments containing '%s'" % trend)
	plt.savefig(savepath)
	plt.show()

if __name__ == '__main__':
	graph(sys.argv[1])