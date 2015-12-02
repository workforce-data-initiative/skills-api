# This script builds a model to predict O*NET Title of a job posting based on its description
# Lable : O*NET title
# Features : Generated from Job Description [TFIDF and Bag of Words(BoW)]

###################
# Importing paths #
###################

import sys

git_root = sys.path[0].split("/app", 1)[0]
sys.path.insert(1, git_root)

#I don't know what is this for
from settings import *

#######################
# Importing libraries #
#######################

# -- Utilities --
import os
import string
import numpy
import cPickle
import marshal
import joblib
import collections

from multiprocessing import Process, Pool

# -- Database & Pandas --
import psycopg2
import sqlalchemy
import pandas as pd

# -- Sklearn --
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA

# -- NLTK --
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


# -- Defining configuration class --
class Config(object):
    # These are the default values they can be changed as required
    min_ngrams = 1
    max_ngrams = 3
    row_limit = -1  # The number of rows to fetch from database. setting the value to -1 fetches all rows
    # stemming = 0 #TODO implement stemming
    # weighting = "none" #TODO implement weighting
    tfidf = True
    save_model = False  # Todo do-something with stats
    model = []
    accuracy = {}
    data_source = 'psv'
    '''
    data_source takes one of two values. 'psv' if you are reading from a pipe separated file containing the job descriptions and onet title. It needs to have a header.
    Specify psv_file = /path/to/psv/file
    'db' if you are reading from the postgres database
    Specify databse = database_connection_string
    '''
    database = CONSERV_DATABASE_CONN
    psv_file = '/mnt/tmp/test.csv'

    multiprocessing = False

    # TODO Add classifiers RFC
    # TODO Add classifiers SVM
    # TODO Add classifiers Decision Trees
    # TODO Add classifiers NN
    # TODO Add classifiers Logit
    # TODO Add classifiers GB
    # TODO Add classifiers Boosting

    names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
             "Random Forest", "AdaBoost", "SGD"]
    #TODO Look at MLLib classifiers
    #TODO GraphLabCreate Spark classifiers
    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        AdaBoostClassifier(),
        SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)
    ]

    stemmer = PorterStemmer()


    # The class "constructor" - It's actually an initializer
    def __init__(self):
        1  # do nothing

def read_from_csv(config):
    #Read data from csv file
    import csv
    descriptions = []
    categories = []
    with open(config.psv_file, 'rb') as csvfile:
        jobreader = csv.reader(csvfile, delimiter='|')
        jobreader.next() #Skipping header
        for row in jobreader:
            #print(len(row))
            try:
                row_0 = row[0]
                row_1 = row[1]
                descriptions.append(row_0)
                categories.append(row_1)
            except IndexError:
                print(jobreader.line_num)
                print(row)

            if (jobreader.line_num == config.row_limit):
                print("breaking at %i" % jobreader.line_num)
                break

        print("Completed csv file read")
    return descriptions,categories

def read_from_db(config, sqlstring):
    #Read data from database
    ##Connect to database
    try:
        engine = sqlalchemy.create_engine(config.database)
        print "Connected"
    except:
        print "Failed to connect"
    # Get data
    #sqlstring = "SELECT jobdesc, onettitle FROM jobdetails WHERE NOT onettitle='' "
 
    jobs = None    

    try:
        if config.row_limit <= 0:
            jobs = pd.read_sql(sqlstring, engine)
        else:
            jobs = pd.read_sql(sqlstring + ' LIMIT ' + str(config.row_limit), engine)
    except:
        print "SQL Query Failed"

    #descriptions = jobs.ix[:, 0].tolist()
    #categories = jobs.ix[:, 1].tolist()

    #return descriptions,categories
    return jobs
 
# def make_info(ngrams, stemming, weighting):
#    info = Config(ngrams, stemming, weighting)
#   return info

def get_tokens(sentence):  # Not used either #Sentence input
    sentence = filter(lambda x: x in string.printable, sentence)
    lowers = sentence.lower().encode('utf-8')
    no_punctuation = lowers.translate(None, string.punctuation)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens


def stem_tokens(tokens, stemmer):  # Doesn't seem to be used at all
    stemmed = ""
    for item in tokens:
        stemmed += " " + stemmer.stem(item)
    return stemmed


def stem_corpus(corpus, stemmer):  # Doesn't seem to be used at all
    corpus_stemmed = [];
    for sentence in corpus:
        tokens = get_tokens(sentence)
        stems = stem_tokens(tokens, stemmer)
        corpus_stemmed.append(stems)
    return corpus_stemmed


def save_classifier(classifier, vectorizer, transformer, config,
                    name):  # TODO Change the input parameters to save_classifier @avinashahuja
    if not os.path.exists(name + '/'):
        os.makedirs(name + '/')
    joblib.dump(classifier, name + '/matcher.save')
    joblib.dump(vectorizer, name + '/vectorizer.save')
    joblib.dump(transformer, name + '/transformer.save')
    text_file = open(name + "/info.txt", "w")
    text_file.write('ngrams:' + str(config.ngrams) + '\n')
    text_file.write('stemming:' + str(config.stemming) + '\n')
    text_file.write('weighting' + config.weighting + '\n')
    text_file.close()


def multi_fit(clf):
    #Trying to multiprocess fitting. Does not work
    print clf
    print "multi working"
    #clf.fit(vectorized_corpus_train,categories_train)


def classify(path, text):
    # TODO use classifier somewhere
    # TODO move this to test_module?
    print ("loading clf")
    clf = joblib.load(path + 'matcher.save')
    print ("loading vec")
    vectorizer = joblib.load(path + 'vectorizer.save')
    print ("vectorizing")
    bow = vectorizer.transform([text])
    print ("predict")
    prediction = clf.predict(bow)
    print prediction[0]
    return prediction[0]

def classify_loaded(clf, vectorizer, text):
    # TODO modify this maybe?
    bow = vectorizer.transform([text])
    prediction = clf.predict(bow)
    print prediction[0]
    return prediction[0]

def build_classifier(config):

    # Reading input file - categories '\t' descriptions
    # print('Reading input file')
    if config.data_source == 'psv':
        descriptions,categories = read_from_csv(config)
    elif config.data_source == 'db':
        descriptions,categories = read_from_db(config)

    # Text preprocessing - stemming

    # corpus = stem_corpus(descriptions, stemmer)
    corpus = descriptions

    {
        '''
    if (args.stemming != None):
        print(args.stemming)
        if (int(args.stemming) == 1):
            print('Stemming corpus')
            corpus = stem_corpus(descriptions, porter)
    '''
    }
    # Text Processing
    print('vectorizing')

    # Check for ngrams
    '''
    if (args.ngrams != None):
        ngrams = (int)(args.ngrams)
    '''
    #print('ngrams = ' + str(config.ngrams))

    # vectorizers = []
    bows = []
    tfidfs = []
    sgds = []

    length = len(corpus)


    # TODO Add SciKit-Learn function to split train and test data based on various parameters
    # TODO: Add stemming and lemmatization
    corpus_train = corpus[0:int(length / 2)]
    corpus_test = corpus[int((length / 2) + 1):(length - 1)]
    categories_train = categories[0:int(length / 2)]
    categories_test = categories[int((length / 2) + 1):(length - 1)]

    # Note Some tips and tricks:
    # If documents are pre-tokenized by an external package, then store them in files (or strings) with the tokens
    # separated by whitespace and pass analyzer=str.split . Fancy token-level analysis such as stemming, lemmatizing,
    # compound splitting, filtering based on part-of-speech, etc. are not included in the scikit-learn codebase,
    # but can be added by customizing either the tokenizer or the analyzer.

    #TODO figure out the difference between transform and fit_transform
    if config.tfidf:
        transformer = TfidfTransformer()  # Used for Part 2, but needed here to save classifier
    else:
        transformer = CountVectorizer(lowercase=True, ngram_range=(config.min_ngrams, config.max_ngrams), stop_words='english')
    # CountVectorizer : Read more here http://scikit-learn.org/stable/modules/feature_extraction.html#common-vectorizer-usage

    vectorized_corpus_train = transformer.fit_transform(corpus_train)
    vectorized_corpus_test = transformer.transform(corpus_test)

    for name, clf in zip(config.names, config.classifiers):
        if config.multiprocessing == True:
            pool = Pool(processes=5)
            results = pool.map(multi_fit, clf)

        else:
            print('Using ' + name)
            clf.fit(vectorized_corpus_train, categories_train)
            score = clf.score(vectorized_corpus_test, categories_test)
            print('score = ', score)


    # print test_classifier(sgd, vectorized_corpus_test, categories_test)

    # End 1


    #deleted test_classifier() as score is already a function
