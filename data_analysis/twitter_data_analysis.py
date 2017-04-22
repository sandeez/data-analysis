import json

from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener

consumer_key = 'Qq9Ot3m3RO3S3SY4hU0P94BNh'
consumer_secret = 'GDz1e7AG9BPKMOA2T6iCXXA2Noqex9yLnVI9gM1spJdLMrwjIk'
access_token = '2477251579-T4ThNRlyOzA5aeeBeWHeWYi54AqvDRSeHsbkc8U'
access_token_secret = 'us7IskAzWL8YhmJqa2nWqw5UYPverrCVlfzp32KfHm1dm'

auth = OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)


class PrintListener(StreamListener):

    def on_status(self, status):
        if not status.text[:3] == 'RT ':
            print(status.text)
            print(status.author.screen_name,
                  status.created_at,
                  status.source,
                  '\n')

    def on_error(self, status_code):
        print('Error code: {}'.format(status_code))
        return True     # keep stream live

    def on_timeout(self):
        print('Listener timeout')
        return True     # keep stream live


def pull_down_tweets(screen_name):
    api = API(auth)
    tweets = api.user_timeline(screen_name=screen_name, count=200)
    dumps = json.dumps
    for tweet in tweets:
        print(dumps(tweet._json, indent=4))


def print_to_terminal():
    listener = PrintListener()
    stream = Stream(auth, listener)
    languages = ('en',)
    stream.sample(languages=languages)


if __name__ == '__main__':
    # print_to_terminal()
    pull_down_tweets(auth.username)
