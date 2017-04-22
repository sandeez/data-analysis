import json

from os import path

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

from sqlalchemy.orm.exc import NoResultFound

from database import session, Tweet, Hashtag, User


consumer_key = 'Qq9Ot3m3RO3S3SY4hU0P94BNh'
consumer_secret = 'GDz1e7AG9BPKMOA2T6iCXXA2Noqex9yLnVI9gM1spJdLMrwjIk'
access_token = '2477251579-T4ThNRlyOzA5aeeBeWHeWYi54AqvDRSeHsbkc8U'
access_token_secret = 'us7IskAzWL8YhmJqa2nWqw5UYPverrCVlfzp32KfHm1dm'

auth = OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)


def save_tweets():
    directory = _get_dir_absolute_path()
    filepath = path.join(directory, 'tweets.json')
    listener = DatabaseListener(number_tweets_to_save=200, filepath=filepath)
    stream = Stream(auth, listener)
    languages = ('en',)
    try:
        stream.sample(languages=languages)
    except KeyboardInterrupt:
        listener.file.close()


class DatabaseListener(StreamListener):

    def __init__(self, number_tweets_to_save, filepath=None):
        self._final_count = number_tweets_to_save
        self._current_count = 0
        if filepath is None:
            filepath = 'tweets.txt'
        self.file = open(filepath, 'w')

    def __del__(self):
        self.file.close()

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        json.dump(raw_data, self.file)
        self.file.write('\n')
        if 'in_reply_to_status_id' in data:
            return self.on_status(data)

    def on_status(self, data):
        save_to_database(data)
        self._current_count += 1
        print('Status count: {}'.format(self._current_count))
        if self._current_count >= self._final_count:
            return False


def create_user_helper(user_data):
    u = user_data
    return User(uid=u['id_str'],
                name=u['name'],
                screen_name=u['screen_name'],
                created_at=u['created_at'],
                description=u['description'],
                followers_count=u['followers_count'],
                statuses_count=u['statuses_count'],
                favorites_count=u['favourites_count'],
                listed_count=u['listed_count'],
                geo_enabled=u['geo_enabled'],
                lang=u.get('lang'))


def create_tweet_helper(tweet_data, user):
    t = tweet_data
    retweet = True if t['text'][:3] == 'RT ' else False
    coordinates = json.dumps(t['coordinates'])
    return Tweet(tid=t['id_str'],
                 tweet=t['text'],
                 user=user,
                 coordinates=coordinates,
                 created_at=t['created_at'],
                 favorite_count=t['favorite_count'],
                 is_retweet=retweet)


def save_to_database(data):
    try:
        user = session.query(User).filter_by(id=str(data['user']['id'])).one()
    except NoResultFound:
        user = create_user_helper(data['user'])
        session.add(user)

    hashtag_results = []
    hashtags = data['entities']['hashtags']
    for hashtag in hashtags:
        hashtag = hashtag['text'].lower()
        try:
            hashtag_obj = session.query(Hashtag).filter_by(text=hashtag).one()
        except NoResultFound:
            hashtag_obj = Hashtag(text=hashtag)
            session.add(hashtag_obj)
        hashtag_results.append(hashtag_obj)
    tweet = create_tweet_helper(data, user)
    for hashtag in hashtag_results:
        tweet.hashtags.append(hashtag)
    session.add(tweet)
    session.commit()


def _get_dir_absolute_path():
    return path.abspath(path.dirname(__file__))


if __name__ == '__main__':
    save_tweets()
