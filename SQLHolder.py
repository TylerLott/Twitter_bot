
# SQL queries

USER_UPDATE = '''UPDATE users SET name = %s, screen_name = %s, verified = %s, location = %s, followers_count = %s,
                 friends_count = %s,statuses_count = %s,created_at = %s,profile_image_https = %s WHERE id = %s'''

USER_INSERT = '''INSERT INTO users(id, name, screen_name, verified, location, followers_count, friends_count, 
                 statuses_count, created_at, profile_image_https) SELECT %s,%s,%s,%s,%s,%s,%s,%s,%s,%s 
                 WHERE NOT EXISTS(SELECT 1 FROM users WHERE id = %s)'''

TWEET_INFO_UPDATE = '''UPDATE tweet_info SET hashtags = %s,url = %s,symbols = %s,created_at = %s,text = %s,place = %s,
                  filter_level = %s, lang = %s,timestamp = %s WHERE id = %s'''

TWEET_INFO_INSERT = '''INSERT INTO tweet_info(id, hashtags, url, symbols, created_at, text, place, filter_level, lang, 
                       timestamp) 
                       SELECT %s,%s,%s,%s,%s,%s,%s,%s,%s,%s WHERE NOT EXISTS(SELECT 1 FROM tweet_info WHERE id=%s)'''

USER_ASSOCIATIONS = '''INSERT INTO user_associations(id_1, id_2, tweet_id) SELECT %s, %s, %s
                       WHERE NOT EXISTS(SELECT 1 FROM user_associations WHERE id_1= %s AND id_2 = %s)'''

TWEETS_INSERT = '''INSERT INTO tweet (user_id, tweet_id, candidate_id) SELECT %s, %s, %s WHERE NOT EXISTS(SELECT 1 FROM tweet 
            WHERE user_id=%s AND tweet_id=%s AND candidate_id=%s)'''


class SQLHolder:

    def __init__(self):
        self.user_update = USER_UPDATE
        self.user_insert = USER_INSERT
        self.tweet_info_update = TWEET_INFO_UPDATE
        self.tweet_info_insert = TWEET_INFO_INSERT
        self.user_associations = USER_ASSOCIATIONS
        self.tweets_insert = TWEETS_INSERT

    def get_user_update(self):
        return self.user_update

    def get_user_insert(self):
        return self.user_insert

    def get_tweet_info_update(self):
        return self.tweet_info_update

    def get_tweet_info_insert(self):
        return self.tweet_info_insert

    def get_user_associations(self):
        return self.user_associations

    def get_tweets_insert(self):
        return self.tweets_insert
