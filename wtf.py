# Francis Pimentel
# Vinicius Vieira

import pandas as pd
import numpy as np
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df1 = pd.read_csv('questions.csv')
# df2 = pd.read_csv('/content/S09_question_answer_pairs.txt', sep='\t')
# df3 = pd.read_csv('/content/S10_question_answer_pairs.txt', sep='\t', encoding = 'ISO-8859-1')

df1.head(20)

all_data = df1 #.append([df2, df3])
all_data.info()

# all_data['Question'] = all_data['ArticleTitle'].str.replace('_', ' ') + ' ' + all_data['Question']
all_data = all_data[['Question', 'Answer']]
all_data.shape

all_data.head(10)

all_data = all_data.drop_duplicates(subset='Question')
all_data.head(10)

all_data.shape

all_data = all_data.dropna()
all_data.shape

import nltk
nltk.download('omw-1.4')
nltk.download("stopwords")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

stopwords_list = stopwords.words('english')

lemmatizer = WordNetLemmatizer()

def my_tokenizer(doc):
    words = word_tokenize(doc)
    
    pos_tags = pos_tag(words)
    
    non_stopwords = [w for w in pos_tags if not w[0].lower() in stopwords_list]
    
    non_punctuation = [w for w in non_stopwords if not w[0] in string.punctuation]
    
    lemmas = []
    for w in non_punctuation:
        if w[1].startswith('J'):
            pos = wordnet.ADJ
        elif w[1].startswith('V'):
            pos = wordnet.VERB
        elif w[1].startswith('N'):
            pos = wordnet.NOUN
        elif w[1].startswith('R'):
            pos = wordnet.ADV
        else:
            pos = wordnet.NOUN
        
        lemmas.append(lemmatizer.lemmatize(w[0], pos))

    return lemmas

tfidf_vectorizer = TfidfVectorizer(tokenizer=my_tokenizer)
tfidf_matrix = tfidf_vectorizer.fit_transform(tuple(all_data['Question']))
print(tfidf_matrix.shape)

import pickle

matrix_path =  "tfidf_matrix.pickle"
vectorizer_path = "tfidf_vectorizer.pickle"


pickle.dump(tfidf_matrix, open(matrix_path, 'wb'))
pickle.dump(tfidf_vectorizer, open(vectorizer_path, "wb"))
pickle.dump(my_tokenizer, open("my_tokenizer.pickle", "wb"))

def predict(question):
    query_vect = tfidf_vectorizer.transform([question])
    similarity = cosine_similarity(query_vect, tfidf_matrix)
    max_similarity = np.argmax(similarity, axis=None)
    
    print('Your question:', question)
    print('Closest question found:', all_data.iloc[max_similarity]['Question'])
    print('Similarity: {:.2%}'.format(similarity[0, max_similarity]))
    print('Type:', all_data.iloc[max_similarity]['Answer'])
    return all_data.iloc[max_similarity]['Answer']