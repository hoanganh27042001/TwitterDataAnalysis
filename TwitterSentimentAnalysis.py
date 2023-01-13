# -*- coding: utf-8 -*-
import re
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS

from text_processing import *


def drop_duplicate(df: pd.DataFrame) -> pd.DataFrame:
    """
    drop duplicated rows
    """
    return df.drop_duplicates()
def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    # Cleaning Text (RT, Punctuation etc)
    # Creating new dataframe and new features
    df['cleaned_text'] = df['Tweet']

    # Removing RT, Punctuation etc
    remove_rt = lambda x: re.sub('RT @\w+: ', " ", x)
    rt = lambda x: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", x)
    df["cleaned_text"] = df["cleaned_text"].map(remove_rt).map(rt)
    df["cleaned_text"] = df["cleaned_text"].str.lower()
    return df

def sentiment_analysis(tw_list: pd.DataFrame) -> pd.DataFrame:
    # Calculating Negative, Positive, Neutral and Compound values
    tw_list[['polarity', 'subjectivity']] = tw_list['cleaned_text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
    for index, row in tw_list['cleaned_text'].iteritems():
        score = SentimentIntensityAnalyzer().polarity_scores(row)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        if neg > pos:
            tw_list.loc[index, 'sentiment'] = 'negative'
        elif pos > neg:
            tw_list.loc[index, 'sentiment'] = 'positive'
        else:
            tw_list.loc[index, 'sentiment'] = 'neutral'
        tw_list.loc[index, 'neg'] = neg
        tw_list.loc[index, 'neu'] = neu
        tw_list.loc[index, 'pos'] = pos
        tw_list.loc[index, 'compound'] = comp

    # Creating new data frames for all sentiments (positive, negative and neutral)
    tw_list_negative = tw_list[tw_list["sentiment"] == 'negative']
    tw_list_postive = tw_list[tw_list['sentiment'] == 'positive']
    tw_list_neutral = tw_list[tw_list["sentiment"] == 'neutral']
    return tw_list, tw_list_postive, tw_list_negative, tw_list_neutral
def show_tweets_sentiment(tw_list):
    tw_list_negative = tw_list[tw_list["sentiment"] == 'negative']
    tw_list_postive = tw_list[tw_list['sentiment'] == 'positive']
    tw_list_neutral = tw_list[tw_list["sentiment"] == 'neutral']

    positive = format(len(tw_list_postive) / len(tw_list) * 100, '.2f')
    negative = format(len(tw_list_negative) / len(tw_list) * 100, '.2f')
    neutral = format(len(tw_list_neutral) / len(tw_list) * 100, '.2f')

    print('Total number of non_duplicated tweets:', len(tw_list))
    print(f'Number of positive tweets: {len(tw_list_postive)} ({positive} %)')
    print(f'Number of negative tweets: {len(tw_list_negative)} ({negative} %)')
    print(f'Number of neutral tweets: {len(tw_list_neutral)} ({neutral} %)')
    print('------------------------------------------------------------------------------')
    print('Positive tweets: ')
    for text in tw_list_postive['Tweet'][:5]:
        print(text.encode('utf-8'))

    print('------------------------------------------------------------------------------')
    print('Negative tweets: ')
    for text in tw_list_negative['Tweet'][:5]:
        print(text.encode('utf-8'))

    print('------------------------------------------------------------------------------')
    print('Neutral tweets: ')
    for text in tw_list_neutral['Tweet'][:5]:
        print(text.encode('utf-8'))
    create_pie_chart(positive, negative, neutral)

def create_pie_chart(positive, negative, neutral):
    # Creating PieCart
    labels = ['Positive[' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'blue', 'red']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.style.use('default')
    plt.legend(labels)
    plt.title("Sentiment Analysis Result")
    plt.axis('equal')
    plt.show()

# Function to Create Wordcloud
def create_wordcloud(text, name=''):
  # mask = np.array(Image.open("cloud.png"))
  stopwords = set(STOPWORDS)
  wc = WordCloud(background_color="white",
                 max_words = 3000,
                 stopwords=stopwords,
                 repeat=True)
  wc.generate(str(text))
  wc.to_file("image/wc_{}.png".format(name))
  print(f"Word Cloud for {name} tweets saved successfully")
  path="image/wc_{}.png".format(name)
  (Image.open(path)).show()

def main():
    # api = TwitterClient()
    # tweets = api.get_tweets(query='World Cup', count=500)
    tweets = pd.read_csv('data/dataset.csv')

    print('Number of tweets fetched: ', len(tweets))
    tweet_list = tweets['Tweet']
    tweet_list = pd.DataFrame(tweet_list)

    tweet_list = drop_duplicate(tweet_list)
    tweet_list = clean_text(tweet_list)
    tweet_list, tw_list_positive, tw_list_negative, tw_neutral = sentiment_analysis(tweet_list)
    show_tweets_sentiment(tweet_list)
    create_wordcloud(tweet_list["Tweet"].values)
    create_wordcloud(tw_list_positive["Tweet"].values, "positive")
    create_wordcloud(tw_list_negative["Tweet"].values, "negative")

    columns = tweet_list.columns[1:]
    # Calculating tweet's length and word count
    tweet_list['text_len'] = tweet_list['Tweet'].astype(str).apply(len)
    tweet_list['text_word_count'] = tweet_list['Tweet'].apply(lambda x: len(str(x).split()))

    print('\nAverage length of tweet for each sentiment:')
    print(round(pd.DataFrame(tweet_list.groupby('sentiment').text_len.mean()), 2))

    print('\nAverage number of word per sentiment:')
    print(round(pd.DataFrame(tweet_list.groupby('sentiment').text_word_count.mean()), 2))

    tw_list_copy = tweet_list.copy()
    tw_list_copy['punct'] = tw_list_copy['Tweet'].apply(lambda x: remove_punct(x))
    tw_list_copy['tokenized'] = tw_list_copy['punct'].apply(lambda x: tokenization(x.lower()))
    tw_list_copy['nonstop'] = tw_list_copy['tokenized'].apply(lambda x: remove_stopwords(x))
    tweet_list['stemmed'] = tw_list_copy['nonstop'].apply(lambda x: stemming(x))

    count_vector_df = countVectorizer(tweet_list)
    # get the most used word
    # get the most 2-gram words
    get_top_n_gram(tweet_list['Tweet'], (2, 2), 10)
    # get the most 3-gram words
    get_top_n_gram(tweet_list['Tweet'], (3, 3), 10)

    df = pd.DataFrame(tweet_list)
    df.to_csv(f'data/sentiment_analysis.csv')
    print('Sentiment analysis results saved in data/sentiment_analysis.csv')

if __name__ == "__main__":
    # calling main function
    main()