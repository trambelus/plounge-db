#!/usr/bin/env python

import praw
import sqlite3
import threading
import time

FILENAME = 'ds_tmp.db3'

def init_db(filename):
	db = sqlite3.connect(filename)
	db.execute("""CREATE TABLE IF NOT EXISTS scores (
			id TEXT NOT NULL PRIMARY KEY UNIQUE,
			score INT
		);""")
	return db

def log(msg):
    print(("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), msg)))

def dump_ids():
    db = sqlite3.connect('plounge.db3')
    l = [i[0] for i in db.execute('SELECT id FROM comments WHERE score IS NULL').fetchall()]
    with open('ids2.txt','w') as f:
        f.write('\n'.join(l))
    db.close()

def correct(db, quit_thread):
    r = praw.Reddit('Un-derping a database: /u/__brony__')
    while True:
        with open('ids2.txt','r') as f:
            l = [i.rstrip() for i in f.readlines()]
        while len(l) > 0:
            try:
                c_id = l[0]
                c = r.get_info(thing_id=c_id)
                created = time.strftime("%Y-%m-%d %X",time.gmtime(c.created_utc))
                print("%s\t %s\t%3d\t%s" % (c_id, created, c.score, c.author))
                # db.execute("UPDATE comments SET udate = '%s' WHERE id = '%s'" % (created, c_id))
                # db.execute("UPDATE comments SET score = %d WHERE id = '%s'" % (c.score, c_id))
                query = "REPLACE INTO scores (id, score) VALUES (?, ?)"
                data = (c.name, c.score)
                db.execute(query, data)
                l = l[1:]
                with open('ids2.txt','w') as f:
                    f.write('\n'.join(l))
                if not quit_thread.is_alive():
                    break
            except Exception as ex:
                log("%s: %s" % (type(ex), ex))
                time.sleep(3)

def wait():
    while input() != "q":
        pass
    print("Stopping...")

def main():
    db = init_db(FILENAME)
    quit_thread = threading.Thread(target=wait)
    quit_thread.start()
    correct(db, quit_thread)
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
    #dump_ids()