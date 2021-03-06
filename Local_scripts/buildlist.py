#!/usr/bin/env python
# Queries the RedditAnalytics API and builds a list of 
#  submission ids to check out later.
# Note: RedditAnalytics is giving 500s. This might not work for a while.
# Or ever again.

import requests
import time

def main():
	after=""
	params = {"subreddit":"ploungeafterdark", "fields":"name","limit":"500"}
	while True:
		j = requests.get("http://api.redditanalytics.com/getPosts", params=params).json()
		print(j)
		with open("ids-pad.txt","a") as f:
			f.write('\n'.join([j['data'][i]['name'][3:] for i in range(len(j['data']))]) + '\n')
		after = j['metadata']['oldest_id']
		params["after"] = after
		print(after)
		time.sleep(1)
if __name__ == '__main__':
	main()