import tweepy

# Twitter API keys and tokens
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Harvest Twitter data
def harvest_tweets(query, num_tweets=10):
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=query, lang="en").items(num_tweets):
        tweets.append({
            "text": tweet.text,
            "created_at": tweet.created_at,
            "user": tweet.user.screen_name
        })
    return tweets
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_data"]
collection = db["tweets"]

# Store harvested data in MongoDB
def store_tweets(tweets):
    for tweet in tweets:
        collection.insert_one(tweet)
import streamlit as st

st.title("Twitter Data Dashboard")

# Function to retrieve data from MongoDB
def get_tweets_from_db(query):
    return list(collection.find({"text": {"$regex": query, "$options": "i"}}))

# Sidebar with query input
query = st.sidebar.text_input("Search for Tweets:", "")
num_tweets = st.sidebar.slider("Number of Tweets to Display:", 1, 100, 10)

if st.sidebar.button("Search"):
    tweets = get_tweets_from_db(query)
    st.subheader(f"Showing {min(len(tweets), num_tweets)} Tweets")
    for tweet in tweets[:num_tweets]:
        st.write(f"**{tweet['user']}** ({tweet['created_at']}):")
        st.write(tweet['text'])
