import os
import subprocess
import tempfile

import requests as r

API_ROOT = 'https://api.twitter.com/'
TWITTER_KEY_VAR = 'TWITTER_CONSUMER_KEY'
TWITTER_SECRET_VAR = 'TWITTER_SECRET_KEY'

def get_twitter_creds_from_env():
    """
    Loads a Twitter key and secret from the environment.
    """
    consumer_key = os.environ[TWITTER_KEY_VAR]
    consumer_secret = os.environ[TWITTER_SECRET_VAR]

    return consumer_key, consumer_secret

def get_auth_token(consumer_key, consumer_secret):
    """
    Per the Twitter Docs:
    https://dev.twitter.com/oauth/application-only
    We need to:
    1. Hit the `oauth2/token` endpoint with a POST request
    2. With the Content-Type header set to 'application/x-www-form-urlencoded;charset=UTF-8'
    3. And the body set to 'grant_type=client_credentials'
    4. Using our key and secret as the user name and password for Basic Auth.
    """
    endpoint = 'oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    # Per the Twitter Docs:
    resp = r.post(
        API_ROOT + endpoint,
        auth=(consumer_key, consumer_secret),
        headers=headers,
        data='grant_type=client_credentials'
    )

    response_json = resp.json()

    # Twitter is awfully firm on this point: if the token_type is not 'bearer',
    # _do not use it_.
    if response_json['token_type'] != 'bearer':
        raise RuntimeError('Could not authorize!')

    return response_json['access_token']


def get_status_by_id(tweet_id, token):
    endpoint = '1.1/statuses/show.json'

    headers = {
        'Authorization': 'Bearer ' + token
    }

    params = {'id': tweet_id}
    resp = r.get(
        API_ROOT + endpoint,
        headers=headers,
        params=params
    )

    response_json = resp.json()
    return response_json

def get_video_url_from_status(status):
    media = status.get('extended_entities', {}).get('media', [])
    variants = media[0].get('video_info', {}).get('variants')

    if not variants:
        print('Could not find a video. （╯°□°）╯︵ ┻━┻')
        raise RuntimeError('ooo weeee')

    urls = [variant['url'] for variant in variants
            if variant['url'].endswith('mp4')]

    # This function could produce multiple urls, but at the time of writing, 
    # we really just kinda care about the first one

    return urls[0]

def download_mp4(url):
    """
    Download an mp4 from a given url.

    TO DO: Test and finish this function
    """
    resp = r.get(url)
    tmp = tempfile.mktemp()

    with open(tmp, 'wb') as handle:
        handle.write(resp.raw)

    return tmp

def convert_mp4_to_gif(mp4, gif_path):
    """
    Shell out mp4->gif conversion to FFMPeG
    """
    return subprocess.call('ffmpeg', ['-i', mp4, gif_path])


if __name__ == "__main__":
    key, secret = get_twitter_creds_from_env()
    token = get_auth_token(key, secret)
    status = get_status_by_id('854059190511423489',token)
    #url = get_video_url_from_status(status)
    print(get_video_url_from_status(status))
    #mp4 = download_mp4(url)
    #convert_mp4_to_gif()

# .py | jq '.'