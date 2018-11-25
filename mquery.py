from pymongo import MongoClient
from flask import Flask

app = Flask(__name__)

# Connect to the MongoDB, change the connection string per your MongoDB environment
client = MongoClient('mongodb2',27017)
# Set the db object to point to the business database
db=client.twitterDB

version = 'Version 1.3'
print("Debug: Connected to Mongo DB.")

def get_hit_count():
    str = "<!DOCTYPE html><head><title>Twitter Counter</title></head>"
    str += "<body><h1> Twitter keyword analytics: </h1><p>" + version + "</p>"
    keygroup=db.twitterdata.aggregate( [ { '$group': { '_id' : "$keyword", "count" : { '$sum' :1 } } }, {"$sort":  { "_id":1} } ] )
    for group in keygroup:
        str += "<p> %s: %d </P>" % (group['_id'],group['count'])
    str += "</body>"
    return str

    
@app.route('/')


def hello():
    vector = get_hit_count()
    print(" Debug: vector ", vector)
    return vector 

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

