
class TwitterAuth:

    def __init__(self):
        self.consumer_key = '*************************************'
        self.consumer_secret = '*************************************'
        self.auth_token = '*************************************'
        self.auth_secret = '*************************************'

    def get_consumer_key(self):
        return self.consumer_key

    def get_consumer_secret(self):
        return self.consumer_secret

    def get_auth_token(self):
        return self.auth_token

    def get_auth_secret(self):
        return self.auth_secret


class DBAuth:

    def __init__(self):
        self.db_username = '*************************************'
        self.db_password = '*************************************'
        self.db_hostname = '*************************************'
        self.db_port = '*************************************'
        self.db_database = '*************************************'

    def get_db_username(self):
        return self.db_username

    def get_db_password(self):
        return self.db_password

    def get_db_hostname(self):
        return self.db_hostname

    def get_db_port(self):
        return self.db_port

    def get_db_database(self):
        return self.db_database
