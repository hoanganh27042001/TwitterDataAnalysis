import re
import string
import nltk
import pandas as pd
from prettytable import PrettyTable
from sklearn.feature_extraction.text import CountVectorizer

# Removing punctuation
def remove_punct(text):
  text = ''.join([char for char in text if char not in string.punctuation])
  text = re.sub('[0-9]+', '', text)
  return text

# Applying tokenization
def tokenization(text):
  text = re.split('\W+', text)
  return text

# Removing stopwords
stopword = nltk.corpus.stopwords.words('english')
def remove_stopwords(text):
  text = [word for word in text if word not in stopword]
  return text

# Applying stemmer
ps = nltk.PorterStemmer()

def stemming(text):
  text = [ps.stem(word) for word in text]
  return text

# Cleaning Text
def clean_text(text):
  text_lc = ''.join([word.lower() for word in text if word not in string.punctuation]) # remove punctuation
  text_rc = re.sub('[0-9]+', '', text_lc)
  tokens = re.split('\W+', text_rc) # tokenization
  text = [ps.stem(word) for word in tokens if word not in stopword]
  # remove stopword and stemming
  return text

def countVectorizer(tw_list):
  # Apply Countvectorizer
  countVectorizer = CountVectorizer(analyzer=clean_text)
  countVector = countVectorizer.fit_transform(tw_list['Tweet'])
  print('{} Number of reviews has {} words'.format(countVector.shape[0], countVector.shape[1]))
  # print(countVectorizer.get_feature_names())

  count_vect_df = pd.DataFrame(countVector.toarray(),
                               columns=countVectorizer.get_feature_names())
  return count_vect_df

def get_top_n_gram(corpus, ngram_range, n=None):
  vec = CountVectorizer(ngram_range=ngram_range, stop_words='english').fit(corpus)
  bag_of_words = vec.transform(corpus)
  sum_words = bag_of_words.sum(axis=0)
  words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
  words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
  pt = PrettyTable(field_names=[f"{ngram_range[0]}_gram", "Count"])
  [pt.add_row(kv) for kv in words_freq[:n]]
  pt.align[f"{ngram_range[0]}_gram"], pt.align["Count"] = 'l', 'r'  # Set column alignment
  print(pt)
  return words_freq[:n]