import json
import os

import requests	

def get_twitter_creds_frome_env():
	consumer_key = os.environ['TWITTER_CONSUMER_KEY']
	consumer_secret = os.environ['TWITTER_SECRET_KEY']

	return consumer_key, consumer_secret

def get_auth_token(consumer_key, consumer_secret):
	#url = 'https://api.twitter.com/1.1'
	endpoint = '/oauth2/token'
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	}

	resp = r.post(
		API_ROOT + 
	)

	if response_json['token_type'] != 'bearer':
		raise RuntimeError('Could not authorize!')

	return response_json['access_token']

def get_status_by_id(tweet_id, token):
	endpoint = '1.1/statuses/show.json'
	headers = {
		'Authorization': 'Bearer' + token
	}

	params = {'id': tweet_id}
	resp = r.get(
		API_ROOT + endpoint,
		headers=headers,
		params=params
	)

	response_json = resp.text
	return response_json

def get_video_url_from_status(status):
	media = status.get('extended_entities', {}).get('media', [])
	variants = media[0].get('video_info', {}).get('variants')

	if not variants:
		print('Could not find a video. （╯°□°）╯︵ ┻━┻')
		raise RuntimeError('ooo weeee')

	urls = [variant['url'] for variant in variants if variant['url'].endswith('mp4')]

	# This function could produce multiple urls, but at the time of writing, 
	# we really just kinda care about the first one

	return url[0]


if __name__ == "__main__":
	key, secret = get_twitter_creds_frome_env()
	token = get_auth_token(key,secret)
	print(get_status_by_id('853513515029585920',token))

# .py | jq '.'