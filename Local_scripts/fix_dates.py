#!/usr/bin/env python

import praw
import sqlite3
import threading
import time

def log(msg):
    print(("%s:\t%s" % (time.strftime("%Y-%m-%d %X"), msg)))

def dump_ids():
    db = sqlite3.connect('plounge.db3')
    l = [i[0] for i in db.execute('SELECT id FROM comments').fetchall()]
    with open('ids2.txt','w') as f:
        f.write('\n'.join(l))
    db.close()

def correct(db, quit_thread):
    r = praw.Reddit('Un-derping a database: /u/__brony__')
    with open('ids2.txt','r') as f:
        l = [i[:-1] for i in f.readlines()]
    while len(l) > 0:
        try:
            c_id = l[0]
            c = r.get_info(thing_id=c_id)
            created = time.strftime("%Y-%m-%d %X",time.gmtime(c.created_utc))
            print("%s\t %s\t%d\t%s" % (c_id, created, c.score, c.author))
            db.execute("UPDATE comments SET udate = '%s' WHERE id = '%s'" % (created, c_id))
            db.execute("UPDATE comments SET score = %d WHERE id = '%s'" % (c.score, c_id))
            l = l[1:]
            with open('ids2.txt','w') as f:
                f.write('\n'.join(l))
            if not quit_thread.is_alive():
                break
        except Exception as ex:
            log(ex)
            time.sleep(3)

def wait():
    while input() != "q":
        pass
    print("Stopping...")

def main():
    db = sqlite3.connect('plounge.db3')
    quit_thread = threading.Thread(target=wait)
    quit_thread.start()
    correct(db, quit_thread)
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
    #dump_ids()