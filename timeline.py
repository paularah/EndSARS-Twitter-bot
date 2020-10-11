from tweepy.streaming import StreamListener
import json
import time


class Listener(StreamListener):

    def __init__(self, api):
        super(StreamListener)
        self.api = api

    def on_data(self, data):
        try:
            output = json.loads(data)
            if output['id']:
                self.api.retweet(output['id'])
                print('retweeted')
                time.sleep(5)
                self.api.update_status("#EndSarsNow, #EndSars, #EndSarsNow!", in_reply_to_status_id=output['id'],
                                       auto_populate_reply_metadata=True)
                print('updated status')
            return True
        except KeyError as e:
            print(e)
