'''
fetch_data.py
Fetch data from Twitter utilizing the twitter API
Usage:
## Collect tweets of your favourite event e.g.	#WorldCup
python fetch_data.py --keyword "World Cup" --limit 500
## Get the followers of	a given	twitter	user
python fetch_data.py -v followers --userid "12345" --username "fifa" --limit 100
## Obtain the tweets of a user
python fetch_data.py -v timeline --userid "12345" --username "fifa" --limit 100
'''
import argparse
import json
import tweepy
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--variable', default='text',
    help = 'type of requirement',
    choices=['followers', 'timeline'])
parser.add_argument('--keyword', type=str,
                    help = 'name of your favourite event')
parser.add_argument('--userid', type=int)
parser.add_argument('--username', type=str)
parser.add_argument('--limit', default=100, type=int,
    help = 'number of returned results')

args = parser.parse_args()

# keys and tokens from the Twitter Dev Console
consumer_key = "###################################"
consumer_secret = "###################################"
access_token = "###################################"
access_token_secret = "###################################"

# attempt authentication
try:
    # create OAuthHandler object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # set access token and secret
    auth.set_access_token(access_token, access_token_secret)
    # create tweepy API object to fetch tweets
    api = tweepy.API(auth)
except:
    print("Error: Authentication Failed")

def get_tweets(query, count=10):
    '''
    Main function to fetch tweets and parse them.
    '''
    # empty list to store parsed tweets
    tweets = []

    # call twitter api to fetch tweets
    fetched_tweets = tweepy.Cursor(api.search_tweets , q = query, lang = 'en').items(count)

    # print(type(fetched_tweets))
    # Serializing json
    # fetched_tweets = self.api.search_tweets(q=query, count = count)
    # json_object = json.dumps(fetched_tweets._json, indent=4)
    # print("fetch: ", fetched_tweets[0]._json)

    # Writing to sample.json
    # with open("sample.json", "w") as outfile:
    #     outfile.write(json_object)
    columns = ['Created Time', 'User', 'Tweet', 'Hashtag']
    data = []
    # parsing tweets one by one
    for tweet in fetched_tweets:
        tweets.append(tweet._json)
        hashtag = [x['text'] for x in tweet.entities['hashtags']]
        data.append([tweet.created_at, tweet.user.screen_name, tweet.text, hashtag])

        # empty dictionary to store required params of a tweet

    df = pd.DataFrame(data, columns = columns)
    df.to_csv('data/dataset.csv', index=False, encoding='utf-8')

    data = json.dumps(tweets, indent=4)
    # Writing to sample.json
    with open("data/tweets.json", "w") as outfile:
        outfile.write(data)

    print(f'Tweets about {query} is collected successfully. Check result at output file dataset.csv and tweets.json')
    print(df)

def get_followers(**kwargs):
    followers = tweepy.Cursor(api.get_followers , user_id = kwargs['userid'],screen_name = kwargs['username']).items(kwargs['limit'])
    # print(len(followers))
    columns = ['Id', 'Name', 'Screen_name', 'Location', 'Description', 'url']
    data = []
    results = []
    for follower in followers:
        data.append([follower.id, follower.name, follower.screen_name, follower.location, follower.description,
                     follower.url])
        results.append(follower._json)

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(f"data/{kwargs['userid']}_{kwargs['username']}_followers.csv")

    results = json.dumps(results, indent=4)
    # Writing to sample.json
    with open(f"data/{kwargs['userid']}_{kwargs['username']}_followers.json", "w") as outfile:
        outfile.write(results)

    print(f"Get followers of given user successfully. \
    Check result at data/{kwargs['userid']}_{kwargs['username']}_followers.csv and \
    data/{kwargs['userid']}_{kwargs['username']}_followers.json")

    print(df)

def get_user_tweets(**kwargs):
    tweets = tweepy.Cursor(api.user_timeline, user_id=kwargs['userid'], screen_name=kwargs['username']).items(kwargs['limit'])
    data = []
    results = []
    columns = ['Created at', 'Tweet']
    print(f"Homeline of user: {kwargs['userid']}_{kwargs['username']}")
    for tweet in tweets:
        print("***Create at: ", tweet.created_at)
        print(tweet.text)
        data.append([tweet.created_at, tweet.text])
        results.append(tweet._json)
    df = pd.DataFrame(data, columns = columns)
    df.to_csv(f"data/{kwargs['userid']}_{kwargs['username']}_tweets.csv", index=False, encoding='utf-8')

    results = json.dumps(results, indent=4)
    # Writing to sample.json
    with open(f"data/{kwargs['userid']}_{kwargs['username']}_followers.json", "w") as outfile:
        outfile.write(results)

    print(f"Get tweets timeline of given user successfully. \
        Check result at data/{kwargs['userid']}_{kwargs['username']}_tweets.csv and \
        data/{kwargs['userid']}_{kwargs['username']}_tweets.json")

if args.keyword is not None:
    get_tweets(args.keyword, args.limit)
if args.variable == 'followers':
    get_followers(userid=args.userid, username=args.username, limit=args.limit)
if args.variable == 'timeline':
    get_user_tweets(userid=args.userid, username=args.username, limit=args.limit)