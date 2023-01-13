# Twitter-Data-Analysis

This repository contains a series of scripts used to analyze Twitter data.

## Set up
**Authentication**: In order to fetch tweets through Twitter API, one needs create a developer account on the [Twitter apps site](https://apps.twitter.com/). Then follow these steps for the same:

* Open [Twitter apps site](https://apps.twitter.com/) and click the button: ‘Create New App’
* Fill the application details. You can leave the callback url field empty.
* Once the app is created, you will be redirected to the app page.
* Open the ‘Keys and Access Tokens’ tab.
* Copy ‘Consumer Key’, ‘Consumer Secret’, ‘Access token’ and ‘Access Token Secret’.

## Usage
To run this project: 
- first clone it to your computer.
- open file fetch_data.py and insert your ‘Consumer Key’, ‘Consumer Secret’, ‘Access token’ and ‘Access Token Secret’
- create new folder ./data and ./image under project directory
- cd to the project directory
- intall requirements: pip install -r requirements.txt

The project structure:

    .
    ├── data                            # folder contains fetched_data, analyzed data in form of .csv and .json file
    ├── image                           # folder contains ouput image (e.g. pie chart, word cloud) 
    ├── fetch_data.py                   # module to obtain data from twitter api
    ├── text_processing.py              # module to perform text processing for each tweet
    ├── top_tweets.py                   # module to get top hashtags and users
    ├── TwitterSentimentAnalysis.py     # module to derive the sentiment of each tweet
    ├── TwitterAnalysis.ipynb           # notebook show the code and the result for each step.
    └── README.md

### 1. Fetch data from Twitter utilizing the twitter API
*Note: Your fetched data will be stored in folder ./data in form of json and csv file for each command*

Collect tweets of your favourite event e.g.	#WorldCup 
```
python fetch_data.py --keyword "World Cup" --limit 500
```
Get the followers of a given	twitter	user
```
python fetch_data.py -v followers --userid "12345" --username "fifa" --limit 100
```
Given	a	twitter	user,	obtain	the	tweets	and	profiles	of	all	followers	of	the	user	and	show	it.
```
python fetch_data.py -v timeline --userid "12345" --username "fifa" --limit 100
```

### 2. Twitter sentiment analysis
```
python TwitterSentimentAnalysis.py
```
Derive the sentiment of each tweet using Python module. This module will show some sentiment about the tweets and return a result file ./data/sentiment_analysis.csv

### 3. Top	10 hash	tags	and	users	based	on	their	number	of	tweets	in	your	data	set.
Find 10 most active users for a event
```
python top_tweets.py -v users -f data/tweets.json -k 10
```
Find 10 most used hashtags for a event
```
python top_tweets.py -v hashtags -f data/tweets.json -k 10
```