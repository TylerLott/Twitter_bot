# Twitter_bot
This is a twitter bot built with the tweepy library 

It is currently set up to collect data from a twitter about all of the candidates in the 2020 presidential election
It is set up to clean the data as it comes in, in order to be stored into a postgreSQL database

TwitterStream:
  contains the search terms, and a dictionary with the candidate id's
  class MyStreamListener:
    starts the stream and contains on_status class to execute when a new status is retrieved
  main program:
    connects to the database
    connects to the twitter stream 
    executes the on_status while running
    if disconnected the stream trys to boot up at a delaying exponentially if the reconnect fails
    
Authentication:
  holds two classes:
    TwitterAuth:  all twitter authentication keys
    DBAuth: all postgreSQL database information
    
TweetAndUser:
  holds truncated state names and normal state names, these are used to get formatted locations
  holds two classes:
    Tweet:
      holds all information relevent to the tweet data table in my database
    User:
      holds all information relevent to the user data table in my database

DataCleaning:
  holds functions to clean and format various information from the tweet response, these are utilized in the Tweet and User classes
  
SQLHolder:
  class that holds all of the sql used in the database queries
    

