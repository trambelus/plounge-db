#!/usr/bin/env python

import sqlite3

db = sqlite3.connect('plounge.db3')
r1 = " ".join([r[0] for r in db.execute("SELECT body FROM comments WHERE body LIKE '%eevn%'").fetchall()])
r2 = " ".join([r[0] for r in db.execute("SELECT body FROM comments WHERE body LIKE '%even%'").fetchall()])
print("1: %d\t2: %d" % (len(r1),len(r2)))
print("Eevn: %d\nEven: %d" % (r1.count("eevn"), r2.count("even")))