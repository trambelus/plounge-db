#!/usr/bin/env python

import markovify
import re
import sqlite3
import praw
from multiprocessing import Process
import time
import sys
import rlogin
from unidecode import unidecode
import nltk

USER = 'PloungerSimulator'
APP = 'Simulator'
STATE_SIZE = 2
DBNAME = 'plounge.db3'

class PText(markovify.Text):
	"""
	This subclass makes three changes: it modifies the sentence filter
	to allow emotes in comments, it uses the Natural Language Toolkit
	for slightly more coherent responses, and it guarantees a response
	every time with make_sentence.
	"""
	def test_sentence_input(self, sentence):
		"""
		A basic sentence filter. This one rejects sentences that contain
		the type of punctuation that would look strange on its own
		in a randomly-generated sentence. 
		"""
		emote_pat = re.compile(r"\[.*?\]\(\/.+?\)")
		reject_pat = re.compile(r"(^')|('$)|\s'|'\s|([\"(\(\)\[\])])")
		# Decode unicode, mainly to normalize fancy quotation marks
		decoded = unidecode(sentence)
		# Sentence shouldn't contain problematic characters
		filtered_str = re.sub(emote_pat, '', decoded).replace('  ',' ')
		# Filtered sentence will have neither emotes nor double spaces
		if re.search(reject_pat, filtered_str):
			# Not counting emotes, there are no awkward characters.
			return False
		return True
	if 'nltk' in globals():
		def word_split(self, sentence):
			words = re.split(self.word_split_pattern, sentence)
			words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
			return words
		def word_join(self, words):
			sentence = " ".join(word.split("::")[0] for word in words)
			return sentence
	def make_sentence(self, *args, **kwargs):
		while True:
			ret = super(PText, self).make_sentence(*args, **kwargs)
			if ret != None:
				return ret

def get_markov(user):
	"""
	Given a user, return a Markov state model for them,
	either from the cache or fresh from the database.
	"""
	try:
		# Stores two files: some-reddit-user.txt for the raw corpus,
		# and some-reddit-user.json for the structure holding the Markov state model.
		f_txt = open('usermodels\%s.txt' % user, 'r')
		f_json = open('usermodels\%s.json' % user, 'r')
		text = ''.join(f_txt.readlines()).replace('~~','')
		json = f_json.readlines()[0]
		if text == '' or json == []:
			raise(FileNotFoundError)
		f_txt.close()
		f_json.close()
		model = PText(text, state_size=STATE_SIZE, chain=markovify.Chain.from_json(json))
	# This is a horrible way to determine if something is in a cache,
	# but for some reason I was too lazy to google "python check if file exists".
	except FileNotFoundError:
		db = sqlite3.connect(DBNAME)
		res = db.execute("SELECT body FROM comments WHERE author LIKE '%s'" % user).fetchall()
		if len(res) < 20:
			return None
		res = ' '.join([r[0] for r in res])
		model = PText(res, state_size=STATE_SIZE)
		f = open('usermodels\%s.txt' % user, 'w')
		f.write(unidecode(res))
		f.close()
		f = open('usermodels\%s.json' % user, 'w')
		f.write(model.chain.to_json())
		f.close()
	# for i in range(10):
	# 	print(unidecode(model.make_sentence()))
	return model

def process(r, com, val):
	"""
	Multiprocessing target. Gets the Markov model, uses it to get a sentence, and posts that as a reply.
	"""
	target_user = val[val.find(' ')+1:]
	if target_user[:3] == '/u/':
		target_user = target_user[3:]
	model = get_markov(target_user)
	if model == None:
		com.reply("User not found: %s\n\n_Note: this bot can only detect users with at least 20 comments logged on the Plounge._" % target_user)
	else:
		reply = unidecode(model.make_sentence())
		print(reply)
		com.reply(reply)

def monitor():
	"""
	Main loop. Looks through username notifications, comment replies, and whatever else,
	and launches a single process for every new request it finds.
	"""
	started = []
	req_pat = re.compile(r"\+/u/%s\s(/u/)?[\w\d\-_]{3,20}" % USER.lower())
	r = rlogin.get_auth_r(USER, APP)
	t0 = time.time()
	while True:
		try:
			# Every 55 minutes, refresh the login.
			if (time.time() - t0 > 55*60):
				r = rlogin.get_auth_r(USER, APP)
				t0 = time.time()
			mentions = r.get_inbox()
			for com in mentions:
				res = re.search(req_pat, com.body.lower())
				if res == None:
					continue # We were mentioned but it's not a proper request, move on
				if USER in [rep.author.name for rep in com.replies if rep.author != None]:
					continue # We've already hit this one, move on
				if com.name in started:
					continue # We've already started on this one, move on
				started.append(com.name)
				Process(target=process, args=(r, com, res.group(0))).start()
			time.sleep(1)
		# General-purpose catch to make the script unbreakable.
		except Exception as ex:
			print("Error: %s" % ex)

def manual(user):
	"""
	This allows the script to be invoked like this:
	psim.py manual some-reddit-user
	This was useful for when the script failed to reply in some cases.
	I logged in as the script, got a manual response like this,
	and just pasted it in as a normal comment.
	They never knew.
	"""
	model = get_markov(user)
	print(unidecode(model.make_sentence()))

if __name__ == '__main__':
	if len(sys.argv) == 3 and sys.argv[1] == 'manual':
		manual(sys.argv[2])
	else:
		monitor()