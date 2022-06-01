import nltk as nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
import psycopg2 as db
import pandas as pd
import pandas.io.sql as sqlio
import os

#Database Connection Postgres instance
connection = db.connect(database='quasar_prod_warehouse', user='scyrway', password=os.environ['SQLPASS'], host=os.environ['HOST'], port='5432')

df = sqlio.read_sql_query("Select posts.campaign_id, text from posts left outer join campaign_info on posts.campaign_id = cast(campaign_info.campaign_id as varchar) where created_at >= '2022-03-01' and text is not null group by posts.campaign_id, text",connection)

# Make lower case
df['text'] = df['text'].astype(str).str.lower()

# We use NLTK’s RegexpTokenizer to perform tokenization in combination with regular expressions.
regexp = RegexpTokenizer('\w+')

df['text_token'] = df['text'].apply(regexp.tokenize)

# Make a list of english stopwords
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words("english")

# Extend the list with your own custom stopwords
my_stopwords = ['https']
stopwords.extend(my_stopwords)

# Remove Stopwords
df['text_token'] = df['text_token'].apply(lambda x: [item for item in x if item not in stopwords])

print(df.info)

# Remove infrequent Words
df['text_string'] = df['text_token'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))

df[['text', 'text_token', 'text_string']].head()

all_words = ' '.join([word for word in df['text_string']])

#tokenize all words
tokenized_words = nltk.tokenize.word_tokenize(all_words)

# Create a frequency distribution for word occurence


# def lemmatize_sentence(tokens):
#     lemmatizer = WordNetLemmatizer()
#     lemmatized_sentence = []
#     for word, tag in pos_tag(tokens):
#         if tag.startswith('NN'):
#             pos = 'n'
#         elif tag.startswith('VB'):
#             pos = 'v'
#         else:
#             pos = 'a'
#         lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
#     return lemmatized_sentence
#
# print(lemmatize_sentence(tweet_tokens[0]))




