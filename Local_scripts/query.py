import sqlite3
import sys

db = sqlite3.connect('plounge.db3')
data = db.execute("SELECT body FROM comments WHERE author = '%s'" % sys.argv[1])
data = [d[0] for d in data]
with open('query.txt','w') as f:
	f.write('\n'.join(data))
db.close()