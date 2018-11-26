import json
import pprint
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient

client = MongoClient('mongodb2', 27017)
db = client.twitterDB


# This is a listener that inserts twwets to Mongo DB.
class StdOutListener(StreamListener):

  
  def on_data(self, data):
  
    data = json.loads(data)
    try:
      data['text']
      for keyword in keywords:
        if keyword in data['text']:
          twitterDoc = {'keyword': keyword,'Created_at':data['created_at'],'Id':data['id'],'Text':data['text'],'Source':data['source'],'Truncated':data['truncated'],'Geo':data['geo']}
          # print(" Debug: ", twitterDoc)
          result = db.twitterdata.insert_one(twitterDoc)
          print('Info: Created a record for keyword {:14s} in Mongo DB: {}'.format(keyword, result.inserted_id))
      return True
    except Exception as e:
      print("Error - Mongo DB error:")
      pprint(e) 
      return False

  def on_error(self, status):
    print(status)

# These are the keywords we are searching
keywords = ['Israel', 'Tel Aviv', 'Jeruslaem', 'Jaffa', 'Haifa']
# -----------------------------------------------------------------

if __name__ == '__main__':
# ----------------------------------
# load my Twitter API credentials
# ----------------------------------
    try:
      with open('/tmp/.config', "r") as cred_file:
        config = json.loads(cred_file.read())
    except Exception as e:
      print("Error: cound not open config file. {}".format(e))
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_key'], config['access_secret'])
    
    stream = Stream(auth, l)
    # This line filter Twitter Streams to capture data by the keywords: 'money', 'laundering', 'security', 'iot'
    stream.filter(track=keywords)
    
