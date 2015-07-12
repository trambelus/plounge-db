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

class PText(markovify.Text):
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
	try:
		f_txt = open('usermodels\%s.txt' % user, 'r')
		f_json = open('usermodels\%s.json' % user, 'r')
		text = ''.join(f_txt.readlines()).replace('~~','')
		json = f_json.readlines()[0]
		if text == '' or json == []:
			raise(FileNotFoundError)
		f_txt.close()
		f_json.close()
		model = PText(text, state_size=STATE_SIZE, chain=markovify.Chain.from_json(json))
	except FileNotFoundError:
		db = sqlite3.connect('plounge.db3')
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
	started = []
	req_pat = re.compile(r"\+/u/%s\s(/u/)?[\w\d\-_]{3,20}" % USER.lower())
	r = rlogin.get_auth_r(USER, APP)
	t0 = time.time()
	while True:
		try:
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
		except Exception as ex:
			print("Error: %s" % ex)

def manual(user):
	model = get_markov(user)
	print(unidecode(model.make_sentence()))

if __name__ == '__main__':
	if len(sys.argv) == 3 and sys.argv[1] == 'manual':
		manual(sys.argv[2])
	else:
		monitor()