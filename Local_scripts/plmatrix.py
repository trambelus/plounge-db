#!/usr/bin/env python

import sqlite3
import matplotlib as mp
import matplotlib.pyplot as plt
import sys

QUERY = '''SELECT
  100*CAST(a.N AS FLOAT)/T sun, 
  100*CAST(b.N AS FLOAT)/T mon, 
  100*CAST(c.N AS FLOAT)/T tue, 
  100*CAST(d.N AS FLOAT)/T wed, 
  100*CAST(e.N AS FLOAT)/T thu, 
  100*CAST(f.N AS FLOAT)/T fri, 
  100*CAST(g.N AS FLOAT)/T sat 
  FROM (
    (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments GROUP BY hour) z
    LEFT JOIN
    (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
      AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '0' GROUP BY hour) a
    ON (z.hour = a.hour) LEFT JOIN
    (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
      AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '1' GROUP BY hour) b
    ON (z.hour = b.hour) LEFT JOIN
    (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
      AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '2' GROUP BY hour) c
    ON (z.hour = c.hour) LEFT JOIN
    (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
      AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '3' GROUP BY hour) d
    ON (z.hour = d.hour) LEFT JOIN
    (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
      AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '4' GROUP BY hour) e
    ON (z.hour = e.hour) LEFT JOIN
    (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
      AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '5' GROUP BY hour) f
    ON (z.hour = f.hour) LEFT JOIN
    (SELECT STRFTIME('%H',udate) hour, COUNT(*) N FROM comments WHERE author = '{0}'
      AND udate > DATE('2014-12-01') AND STRFTIME('%w',udate) = '6' GROUP BY hour) g
    ON (z.hour = g.hour) LEFT JOIN
    (SELECT COUNT(*) T FROM comments WHERE author = '{0}'
      AND udate > DATE('2014-12-01'))
  )'''
DBPATH = 'plounge.db3'

def matrix(user, dbpath=DBPATH, savepath=None):
	if savepath == None:
		savepath = 'mat\\%s.png' % user
	db = sqlite3.connect(dbpath)
	data = db.execute(QUERY.format(user)).fetchall()
	data = list(map(list,zip(*[[i if i != None else 0 for i in j] for j in data])))
	print(data)
	db.close()
	plt.imshow(data)
	plt.show()

def main():
	if len(sys.argv) != 2:
		print("Usage: plmatrix.py [user]")
		return
	matrix(sys.argv[1])

if __name__ == '__main__':
	main()