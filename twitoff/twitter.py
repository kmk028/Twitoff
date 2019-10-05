import tweepy
import basilica
import decouple import config
from .model import DB, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_user(username):
  # gets the user data from Tweepy API
  twitter_user = TWITTER.get_user(username) 
  
  #add user info to user table in database
  db_user = User(id=twitter_user.id,name=twitter_user.screen_name)

  DB.session.add(db_user)

   # Store first 200 tweets which are not retweets or replies to pther tweets
  tweets = twitter_user.timeline(count=200,exclude_replies = True,include_rts = False,tweet_mode='extended')

  for tweet in tweets:
        embedding = BASILICA.embed_sentence(tweet.full_text,
                                            model='twitter')
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300],
                        embedding=embedding)
        db_user.tweets.append(db_tweet)
        DB.session.add(db_tweet)
    
  DB.session.commit()
   return db_user
