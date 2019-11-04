from DataCleaning import *

STATES = ['al', 'ak', 'as', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'dc', 'fm', 'fl', 'ga', 'gu', 'hi', 'id', 'il', 'in',
          'ia', 'ks', 'ky', 'la', 'me', 'mh', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm',
          'ny', 'nc', 'nd', 'mp', 'oh', 'ok', 'or', 'pw', 'pa', 'pr', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'vi',
          'va', 'wa', 'wv', 'wi', 'wy']

STATE_NAMES = ['alabama', 'alaska', 'american samoa', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut',
               'delaware', 'district of columbia', 'federated states of micronesia', 'florida', 'georgia', 'guam',
               'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine',
               'marshall islands', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri',
               'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york',
               'north carolina', 'north dakota', 'northern mariana islands', 'ohio', 'oklahoma', 'oregon', 'palau',
               'pennsylvania', 'puerto rico', 'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas',
               'utah', 'vermont', 'virgin island', 'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming']


class Tweet:

    def __init__(self, tweet_obj):
        self.status = tweet_obj.status
        self.text = self.get_tweet_text()
        self.url = self.get_tweet_url()
        self.hashtags = self.get_hashtags()
        self.symbols = self.get_symbols()
        self.place = self.get_place()
        self.createdAt = self.get_created_at()
        self.id = self.get_id()
        self.timestamp = self.get_timestamp()
        self.filterLevel = self.get_filter_level()
        self.lang = self.get_lang()

    def get_tweet_text(self):
        text = self.status.extended_tweet['full_text'] if self.status.truncated else self.status.text
        return clean_data_text(text)

    def get_tweet_url(self):
        if self.status.truncated:
            if self.status.extended_tweet['entities']['urls']:
                url = clean_data_other(self.status.extended_tweet['entities']['urls'][0]['expanded_url'])
            else:
                url = 'NULL'
        else:
            if self.status.entities['urls']:
                url = clean_data_other(self.status.entities['urls'][0]['expanded_url'])
            else:
                url = 'NULL'
        return url

    def get_hashtags(self):
        hashtags = self.status.extended_tweet['entities']['hashtags'] if self.status.truncated else \
            self.status.entities['hashtags']
        hashtags = ''.join(i['text'] + ' ' for i in hashtags)
        hashtags = 'NULL' if hashtags == '' else clean_data_other(hashtags)
        return hashtags

    def get_symbols(self):
        symbols = self.status.extended_tweet['entities']['symbols'] if self.status.truncated else self.status.entities[
            'symbols']
        symbols = ''.join(i['text'] + ' ' for i in symbols)
        symbols = 'NULL' if symbols == '' else clean_data_other(symbols)
        return symbols

    def get_place(self):
        return clean_data_loc(self.status.place.full_name, STATES, STATE_NAMES) if self.status.place else 'NULL'

    def get_created_at(self):
        return clean_data_other(self.status.created_at)

    def get_id(self):
        return clean_data_other(self.status.id_str)

    def get_timestamp(self):
        return clean_data_other(self.status.timestamp_ms)

    def get_filter_level(self):
        return clean_data_other(self.status.filter_level)

    def get_lang(self):
        return clean_data_other(self.status.lang)


class User:

    def __init__(self, tweet_obj):
        self.status = tweet_obj.status
        self.id = self.get_user_id()
        self.mentions = self.get_mentions()
        self.name = self.get_user_name()
        self.screenName = self.get_user_screen_name()
        self.verified = self.get_verified()
        self.location = self.get_location()
        self.followers = self.get_followers()
        self.friends = self.get_friends()
        self.statuses = self.get_statuses()
        self.createdAt = self.get_created_at()
        self.imageUrl = self.get_image_url()

    def get_user_id(self):
        return clean_data_other(self.status.user.id_str)

    def get_mentions(self):
        mentions = self.status.extended_tweet['entities']['user_mentions'] if self.status.truncated else \
            self.status.entities['user_mentions']
        mentions = list(i['id_str'] for i in mentions)
        return mentions

    def get_user_name(self):
        return clean_data_names(self.status.user.name)

    def get_user_screen_name(self):
        return clean_data_names(self.status.user.screen_name)

    def get_verified(self):
        return self.status.user.verified

    def get_location(self):
        return clean_data_loc(self.status.user.location, STATES, STATE_NAMES) if self.status.user.location else 'NULL'

    def get_followers(self):
        return self.status.user.followers_count

    def get_friends(self):
        return self.status.user.friends_count

    def get_statuses(self):
        return self.status.user.statuses_count

    def get_created_at(self):
        return clean_data_other(self.status.user.created_at)

    def get_image_url(self):
        return clean_data_other(self.status.user.profile_image_url_https)


class StatusJSON:

    def __init__(self, status_json):
        self.status = status_json
