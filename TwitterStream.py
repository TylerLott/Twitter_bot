import tweepy
import psycopg2
import math
import time
from TweetAndUser import Tweet, User, StatusJSON
from SQLHolder import SQLHolder
from Authentication import TwitterAuth, DBAuth

''' 
----- Constants for Stream----- 
'''
CANDIDATES = ['Trump', 'Weld', 'Walsh', 'Biden', 'Buttigieg', 'Booker', 'Warren', 'Klobuchar',
              'Yang', 'Sanders']

CANDIDATES_ID = {'Trump': 1, 'Weld': 2, 'Walsh': 3, 'Biden': 4, 'Buttigieg': 5,
                 'Booker': 6, 'Warren': 7, 'Klobuchar': 8, 'Yang': 9, 'Sanders': 10}

TRACKING = 'Trump, Donald Trump, ' \
           'Weld, Bill Weld, ' \
           'Walsh, Joe Walsh, ' \
           'Biden, Joe Biden, ' \
           'Buttigieg, Pete Buttigieg, ' \
           'Booker, Cory Booker, ' \
           'Warren, Elizabeth Warren, ' \
           'Klobuchar, Amy Klobuchar, ' \
           'Yang, Andrew Yang, ' \
           'Sanders, Bernie Sanders'


class MyStreamListener(tweepy.StreamListener):

    sql = SQLHolder()

    def on_status(self, status):
        if 'RT ' not in status.text and any(i in status.text for i in CANDIDATES):
            child = StatusJSON(status)
            tweet = Tweet(child)
            user = User(child)
            # actual database organizational logic

            cursor.execute((sql.get_user_update() % (user.name, user.screenName, user.verified, user.location,
                                                     user.followers, user.friends, user.statuses, user.createdAt,
                                                     user.imageUrl, user.id)))

            cursor.execute((sql.get_user_insert() % (user.id, user.name, user.screenName, user.verified, user.location,
                                                     user.followers, user.friends, user.statuses, user.createdAt,
                                                     user.imageUrl, user.id)))

            cursor.execute(sql.get_tweet_info_update() % (tweet.hashtags, tweet.url, tweet.symbols, tweet.createdAt,
                                                          tweet.text, tweet.place, tweet.filterLevel, tweet.lang,
                                                          tweet.timestamp, tweet.id))
            cursor.execute(sql.get_tweet_info_insert() % (tweet.id, tweet.hashtags, tweet.url, tweet.symbols,
                                                          tweet.createdAt, tweet.text, tweet.place, tweet.filterLevel,
                                                          tweet.lang, tweet.timestamp, tweet.id))

            if user.mentions:
                for mentioned in user.mentions:
                    cursor.execute(sql.user_associations % (user.id, '\''+mentioned+'\'', tweet.id,
                                                            user.id, '\''+mentioned+'\''))

            for candidate in CANDIDATES:
                if candidate.lower() in tweet.text:
                    cursor.execute(sql.tweets_insert % (user.id, tweet.id, CANDIDATES_ID[candidate],
                                                        user.id, tweet.id, CANDIDATES_ID[candidate]))

            connection.commit()


if __name__ == '__main__':

    twitter_auth = TwitterAuth()
    db_auth = DBAuth()
    sql = SQLHolder()

    # connect to postgres database
    try:
        connection = psycopg2.connect(user=db_auth.get_db_username(),
                                      password=db_auth.get_db_password(),
                                      host=db_auth.get_db_hostname(),
                                      port=db_auth.get_db_port(),
                                      database=db_auth.get_db_database())
        cursor = connection.cursor()
        print('Connection Successful \n', connection.get_dsn_parameters())
    except (Exception, psycopg2.Error) as error:
        print('An error occurred while connecting to the database \n', error)

    # twitter stream authentication

    auth = tweepy.OAuthHandler(twitter_auth.get_consumer_key(), twitter_auth.get_consumer_secret())
    auth.set_access_token(twitter_auth.get_auth_token(), twitter_auth.get_auth_secret())

    api = tweepy.API(auth)

    # loop to start stream and handle disconnections

    error_counter = 0
    while True:
        try:
            cSL = MyStreamListener()
            myStream = tweepy.Stream(auth=api.auth, listener=cSL)
            myStream.filter(track=[TRACKING],
                            is_async=True)
            error_counter = 0
        except tweepy.TweepError as e:
            print('Error while streaming... Restarting Connection in %s seconds' % math.pow(2, error_counter))
            print('Error: ', e.__doc__)
            print(e.args[0][0]['code'])
            time.sleep(math.pow(2, error_counter))
            error_counter += 1
        except OSError as e:
            print(e)
            time.sleep(math.pow(2, error_counter))
            error_counter += 1
        except Exception as e:
            print('Error while streaming... Restarting Connection in %s seconds' % math.pow(2, error_counter))
            print(e)
            time.sleep(math.pow(2, error_counter))
            error_counter += 1
