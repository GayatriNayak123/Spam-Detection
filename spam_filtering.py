# -*- coding: utf-8 -*-
"""Spam_Filtering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DEHyD2THfY8N0qbBE4UH-knzirUSOkJZ

# Spam Filtering Using Machine Learning Techniques
"""

# 1. Data collection
# 2. Data cleaning
# 3. Text\Data Pre-Processing
# 4. Exploratory Data Analysis
# 5. Model Building
# 6. Evaluation

# importing libraries
import numpy as np
import pandas as pd

"""## 1. Data Collection"""

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/spam.csv',encoding='latin-1')

df.head()

df.shape

"""## 2. Data Cleaning"""

df.info()

# drop last 3 cols
df.drop(columns=['Unnamed: 2','Unnamed: 3','Unnamed: 4'],inplace=True)

df.head()

# renaming the columns
df.rename(columns={'v1':'target','v2':'text'},inplace=True)
df.head()

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

df['target'] = encoder.fit_transform(df['target'])
df.head()

# missing values
df.isnull().sum()

# check for duplicate values
df.duplicated().sum()

# remove duplicate values
df = df.drop_duplicates(keep='first')

df.duplicated().sum()

df.shape

"""## 3. EDA"""

df.head()

df['target'].value_counts()

import matplotlib.pyplot as plt
plt.pie(df['target'].value_counts(), labels=['ham','spam'],autopct="%0.2f")
plt.show()

# Data is imbalanced

import nltk

pip install nltk

nltk.download('punkt')

df['num_characters'] = df['text'].apply(len)

df.head()

# number of words
df['num_words'] = df['text'].apply(lambda x:len(nltk.word_tokenize(x)))

df.head()

df['num_sentences'] = df['text'].apply(lambda x:len(nltk.sent_tokenize(x)))

df.head()

df[['num_characters','num_words','num_sentences']].describe()

df[df['target'] == 0][['num_characters','num_words','num_sentences']].describe()

# ham
df[df['target'] == 0][['num_characters','num_words','num_sentences']].describe()

# spam
df[df['target'] == 1][['num_characters','num_words','num_sentences']].describe()

import seaborn as sns

sns.histplot(df[df['target'] == 0]['num_characters'])
sns.histplot(df[df['target'] == 1]['num_characters'],color='red')

sns.histplot(df[df['target'] == 0]['num_words'])
sns.histplot(df[df['target'] == 1]['num_words'],color='red')

#correlation
sns.pairplot(df,hue='target')

sns.heatmap(df.corr(),annot=True)

"""## 3. Data Preprocessing

*   Lower case
*   Tokenization
*   Removing special characters
*   Removing stop words and punctuation
*   stemming
"""

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)


    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords

import string
string.punctuation

df['text'][0]

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
ps.stem('dancing')

df['transformed_text'] = df['text'].apply(transform_text)

df.head()

pip install wordcloud

from wordcloud import WordCloud
wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')

spam_wc = wc.generate(df[df['target'] == 1]['transformed_text'].str.cat(sep=" "))

plt.imshow(spam_wc)

ham_wc = wc.generate(df[df['target'] == 0]['transformed_text'].str.cat(sep=" "))

plt.imshow(ham_wc)

spam_corpus = []
for msg in df[df['target'] == 1]['transformed_text'].tolist():
    for word in msg.split():
        spam_corpus.append(word)

len(spam_corpus)

ham_corpus = []
for msg in df[df['target'] == 0]['transformed_text'].tolist():
    for word in msg.split():
        ham_corpus.append(word)

len(ham_corpus)

df.head()

"""## 4. Model Building

(Naive Bayes Algorithm , Linear Regression, KNN, SVM)
"""

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
cv = CountVectorizer()
tfidf = TfidfVectorizer()

x = tfidf.fit_transform(df['transformed_text']).toarray()

from google.colab import drive
drive.mount('/content/drive')

x.shape

y = df['target'].values
y

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=2)

from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score

gnb = GaussianNB()
mnb = MultinomialNB()
bnb = BernoulliNB()

gnb.fit(x_train,y_train)
y_pred1 = gnb.predict(x_test)
print(accuracy_score(y_test,y_pred1))
print(confusion_matrix(y_test,y_pred1))
print(precision_score(y_test,y_pred1))

mnb.fit(x_train,y_train)
y_pred2 = mnb.predict(x_test)
print(accuracy_score(y_test,y_pred2))
print(confusion_matrix(y_test,y_pred2))
print(precision_score(y_test,y_pred2))

bnb.fit(x_train,y_train)
y_pred3 = bnb.predict(x_test)
print(accuracy_score(y_test,y_pred3))
print(confusion_matrix(y_test,y_pred3))
print(precision_score(y_test,y_pred3))

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier

svc = SVC(kernel='sigmoid', gamma=1.0)
knc = KNeighborsClassifier()
mnb = MultinomialNB()
lrc = LogisticRegression(solver='liblinear', penalty='l1')

clfs = {
    'SVC' : svc,
    'KN' : knc,
    'NB': mnb,
    'LR': lrc
}

def train_classifier(clf,X_train,y_train,X_test,y_test):
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test,y_pred)
    precision = precision_score(y_test,y_pred)

    return accuracy,precision

train_classifier(svc,x_train,y_train,x_test,y_test)

accuracy_scores = []
precision_scores = []

for name,clf in clfs.items():

    current_accuracy,current_precision = train_classifier(clf, x_train,y_train,x_test,y_test)

    print("For ",name)
    print("Accuracy - ",current_accuracy)
    print("Precision - ",current_precision)

    accuracy_scores.append(current_accuracy)
    precision_scores.append(current_precision)

performance_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy':accuracy_scores,'Precision':precision_scores}).sort_values('Precision',ascending=False)

performance_df

performance_df1 = pd.melt(performance_df, id_vars = "Algorithm")

performance_df1

sns.catplot(x = 'Algorithm', y='value',
               hue = 'variable',data=performance_df1, kind='bar',height=5)
plt.ylim(0.5,1.0)
plt.xticks(rotation='vertical')
plt.show()

