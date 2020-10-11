from jsonschema import validate
import jsonschema
import json
import logging
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from tweepy import TweepError
from tweepy import Stream
from timeline import Listener
import time


class Endsars:
    def __init__(self):
        validated_config = validate_config()
        api_key, api_secret, access_token, access_token_secret, hashtags, blacklist = validated_config.values()
        api_key = api_key.strip()
        api_secret = api_secret.strip()
        access_token = access_token.strip()
        access_token_secret = access_token_secret.strip()
        api_instance = self.auth_user(api_key, api_secret, access_token, access_token_secret)
        # self.like_and_retweet_search(api_instance)
        # time.sleep(60)
        self.live_feed(api_instance, hashtags)

    @staticmethod
    def auth_user(api_key, api_secret, access_token, access_token_secret):
        try:
            auth = OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=4, retry_delay=30)
            print('API keys and tokens authenticated')
            return api
        except TweepError as e:
            logging.error(e.reason)

    def like_and_retweet_search(self, api):
        for tweet in Cursor(api.search, '#EndSARS').items(30):
            try:
                tweet.favorite()
                print("likekeddd")
                tweet.retweet()
                print("retweeted")
            except TweepError as e:
                logging.error(e.reason)

    def live_feed(self, api, hashtags):
        twitter_stream = Stream(api.auth, Listener(api))
        twitter_stream.filter(track=hashtags)


def validate_config():
    schema = {
        "type": "object",
        "properties": {
            "API KEY": {
                "type": "string"
            },
            "API SECRET KEY": {
                "type": "string"
            },
            "ACCESS TOKEN": {
                "type": "string"
            },
            "ACCESS TOKEN SECRET": {
                "type": "string"
            },
            "hashtags": {
                "type": "array"
            },
            "blacklist": {
                "type": "array"
            }
        },
        "required": [
            "API KEY",
            "API SECRET KEY",
            "ACCESS TOKEN",
            "ACCESS TOKEN SECRET",
            "hashtags",
            "blacklist"
        ]
    }
    try:
        with open('config.json', 'r') as config_input:
            config_data = config_input.read()
            config_json = json.loads(config_data)
            logging.info('Loaded config')
            validate(config_json, schema)
            logging.info('Valid config schema')
            return config_json
    except ValueError or jsonschema.exceptions.ValidationError as e:
        logging.error(e.reason)
