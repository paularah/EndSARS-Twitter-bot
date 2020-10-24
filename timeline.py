from tweepy.streaming import StreamListener
import json
import time
from tweepy import TweepError


class Listener(StreamListener):

    def __init__(self, api, message):
        super(StreamListener)
        self.api = api
        self.message = message

    def on_data(self, data):
        try:
            output = json.loads(data)
            if output['id']:
                self.api.retweet(output['id'])
                print('retweeted')
                time.sleep(10)
                self.api.update_status(self.message, in_reply_to_status_id=output['id'],
                                       auto_populate_reply_metadata=True)
                print('updated status')
            return True
        except KeyError as e:
            print(e)
            return True

    def on_error(self, status_code):
        return True
