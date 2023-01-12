'''
top-tweets.py
Computes summary statistics about top users, hashtags for a given keyword
@p_barbera
Usage:
## find 10 most active users for this event
python top_tweets.py -v users -f data/tweets.json -k 10
## find 10 most used hashtags for this event
python top_tweets.py -v hashtags -f data/tweets.json -k 10
'''
import argparse
import json

import pandas as pd
from prettytable import PrettyTable
from collections import Counter

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True,
    help = 'name of file with tweets in json format')
parser.add_argument('-v', '--variable', default='text',
    help = 'element of tweet to summarize',
    choices=['hashtags', 'users'])
parser.add_argument('-k', '--count', default=10, type=int,
    help = 'number of results to display in console')

args = parser.parse_args()
output = args.variable
tweetfile = args.file
k = args.count
def top_hashtags(tweetfile, count):
    # Opening JSON file
    f = open(tweetfile)

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # print(data[0]['entities']['hashtags'])
    hashtags = [hashtag['text'] for tweet in data for hashtag in tweet['entities']['hashtags']]

    # for label, data in (("Hashtag", hashtags)):
    pt = PrettyTable(field_names=["Hashtag", "No of tweets"])
    c = Counter(hashtags)
    [pt.add_row(kv) for kv in c.most_common()[:count]]
    pt.align["Hashtag"], pt.align["Count"] = 'l', 'r'  # Set column alignment
    print(pt)

def top_users(tweetfile, count):
    # Opening JSON file
    f = open(tweetfile)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # print(data[0]['entities']['hashtags'])
    users = [tweet['user']['screen_name'] for tweet in data]

    # for label, data in (("Hashtag", hashtags)):
    pt = PrettyTable(field_names=["Users", "No of tweets"])
    c = Counter(users)
    [pt.add_row(kv) for kv in c.most_common()[:count]]
    pt.align["Users"], pt.align["No of tweets"] = 'l', 'r'  # Set column alignment
    print(pt)
if output == 'hashtags':
    top_hashtags(tweetfile, k)

if output == 'users':
    top_users(tweetfile, k)
