import requests
from bs4 import BeautifulSoup
import re
import csv
import tweepy

# Twitter API keys
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Authenticate Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Scrape phishing news
url = 'https://www.phishing.org/news'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# Extract news articles and their links
articles = []
for item in soup.select('.newsItem'):
    article = item.select_one('.title a').text.strip()
    link = item.select_one('.title a')['href']
    articles.append((article, link))

# Scrape Twitter for #phishing tweets
tweets = []
for tweet in tweepy.Cursor(api.search_tweets, q='#phishing').items(10):
    urls = re.findall("(?P<url>https?://[^\s]+)", tweet.text)
    if urls:
        tweets.append((tweet.text, urls))

# Write results to a CSV file
with open('phishing_news.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Article', 'Link'])
    for article, link in articles:
        writer.writerow([article, link])
    for tweet, urls in tweets:
        writer.writerow([tweet, urls])
