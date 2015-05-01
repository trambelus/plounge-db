#!/usr/bin/env python
# Gives a user's info

import requests
import sqlite3
import rlogin
import time

ID_LINK = '305kgd'
USERNAME = 'AboutThisPlounger'

def scan(sub):
    while True:
        posts = sub.get_new(limit=64)
        for s in posts:
            if ID_LINK in s.selftext and not already_commented(s):
                return s

def already_commented(s):
    return USERNAME in [rep.author.name for rep in s.comments if rep.author != None]

def assemble_info(s):
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
    [r, sub] = rlogin.login(USERNAME)
    while True:
        s = scan(sub)
        assemble_info(s)


if __name__ == '__main__':
    main()