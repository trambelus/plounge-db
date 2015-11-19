#!/usr/bin/env python

import matplotlib.pyplot as plt
import sqlite3
# Data dump
# Source:
# select author, count(*) n from comments where udate > datetime('2015-10-09 19:34:58') group by author order by n desc
db = sqlite3.connect('plounge.db3')
data = db.execute("select substr(author,-1,1) title, count(*) n from (select author from comments where udate > datetime('2015-10-09 19:34:58') group by author) group by title order by n desc").fetchall()
db.close()
mlist = data
mdict = {"" : "Robot",
	"a": "Scientist",
	"A": "Battery",
	"b": "Nurse",
	"B": "Pajamas",
	"c": "Doctor",
	"C": "Surgeon",
	"d": "Zombie",
	"D": "Half-Zombie",
	"e": "Ghost",
	"E": "Ghost Pirate",
	"f": "Pirate",
	"F": "Pirate Ghost",
	"g": "Police Officer",
	"G": "Sheriff",
	"h": "President",
	"H": "Presidente",
	"i": "Lion",
	"I": "Tiger",
	"j": "Superhero",
	"J": "Supervillain",
	"k": "Moth",
	"K": "Silly Putty",
	"l": "Jedi",
	"L": "Sith",
	"m": "Prisoner",
	"M": "Escaped Convict",
	"n": "Princess",
	"N": "Baroness",
	"o": "Devil",
	"O": "Demon",
	"p": "Skeleton",
	"P": "Skelingeton",
	"q": "Knight",
	"Q": "Squire",
	"r": "Bee",
	"R": "Honey Bee",
	"s": "Vampire",
	"S": "Twilight Vampire",
	"t": "Dinosaur",
	"T": "Caveman",
	"u": "Soldier",
	"U": "Roman",
	"v": "Fairy",
	"V": "Elf",
	"w": "Cowboy",
	"W": "Cow",
	"x": "Prime Minister",
	"X": "Pig",
	"y": "Rabbit",
	"Y": "Wabbit",
	"z": "Hacker",
	"Z": "H4x0r",
	"_": "Almost Robot",
	"1": "Nurse Robot",
	"2": "Party Robot",
	"3": "Doctor Robot",
	"4": "Dancing Robot",
	"5": "Robot?",
	"6": "Cardboard Robot",
	"7": "Not Quite a Robot",
	"8": "Robit",
	"9": "Dancer",
	"0": "Clown",
}
keys = sorted(list(mdict.keys()))
scores = [(mdict[n], sum([mlist[i][0][-1] not in keys if n == '' else mlist[i][0][-1] == n for i in range(len(mlist))])) for n in keys]
ss = sorted(scores, key=lambda score:-score[1])
ss.reverse()
plt.figure(facecolor='white')
plt.bar(range(len(ss)), [ss[n][1] for n in range(len(ss))], align='center')
plt.xticks(range(len(ss)),["%s (%d)" % tuple(ss[n]) for n in range(len(ss))], rotation=80)
plt.axis([-1, len(ss), 0, 100])
plt.title("Number of PLoungers who've been active since Civvie's change, sorted by title")
plt.show()