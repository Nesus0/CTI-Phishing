import requests
import tweepy
import os

# Twitter API keys
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Set up Tweepy API client
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Scrape Phishtank for current phishing campaigns
url = 'http://data.phishtank.com/data/online-valid.json'
response = requests.get(url)
data = response.json()

# Save Phishtank results to file
with open('phishtank_results.txt', 'w') as f:
    f.write('Phishing campaigns found on Phishtank:\n\n')
    for entry in data:
        f.write(f"URL: {entry['url']}\n")
        f.write(f"Phishing target: {entry['phish_detail_url']}\n")
        f.write(f"Submission time: {entry['submission_time']}\n\n")

# Scrape Twitter for current phishing campaigns
query = "#phishing"
tweets = api.search_all_tweets(query, max_results=10)

# Save Twitter results to file
with open('twitter_results.txt', 'w') as f:
    f.write('Phishing campaigns found on Twitter:\n\n')
    for tweet in tweets:
        f.write(f"Tweet: {tweet.text}\n")
        f.write(f"Author: {tweet.author.name}\n")
        f.write(f"Date: {tweet.created_at}\n\n")

print('Results saved to file.')
