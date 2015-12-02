import os
import sys
import collections

import string
import numpy
import cPickle
import marshal
import joblib
import timeit

from rebuildd import utill

import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import svm

from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils

# Test matcher
def test():
    print "Matcher script works!"
    
class Info(object):
    ngrams = 1
    stemming = 0
    weighting = "none"
    # The class "constructor" - It's actually an initializer 
    def __init__(self, ngrams, stemming, weighting):
        self.ngrams = ngrams
        self.stemming = stemming
        self.weighting = weighting

def make_info(ngrams, stemming, weighting):
    info = Info(ngrams, stemming, weighting)
    return info

def read_info(model_path, ngrams_, stemming_, weighting_):
    ngrams_ = 1
    stemming_ = 0
    weighting_ = 'none'
    with open(model_path+'info.txt', "r") as ins:
        for line in ins:
            try:
                line = line.strip('\n')
                line_array = line.split(':')
                if (len(line_array) >= 2):
                    if (line_array[0] == 'ngrams'):
                        ngrams_ = int(line_array[1])
                    if (line_array[0] == 'stemming'):
                        stemming_ = int(line_array[1])
                    if (line_array[0] == 'weighting'):
                        weighting_ = line_array[1]
            except:
                pass


def get_tokens(text):
    text = filter(lambda x: x in string.printable, text)
    lowers = text.lower().encode('utf-8')
    no_punctuation = lowers.translate(None, string.punctuation)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens

def stem_tokens(tokens, stemmer):
    stemmed = ""
    for item in tokens:
        stemmed += " " + stemmer.stem(item)
    return stemmed

def stem_corpus(corpus, stemmer):
    corpus_stemmed = [];
    for d in corpus:
        tokens = get_tokens(d)
        stems = stem_tokens(tokens, porter)
        corpus_stemmed.append(stems)
    return corpus_stemmed

def save_classifier(classifier, vectorizer, transformer, info,  name):
    if not os.path.exists(name+'/'):
        os.makedirs(name+'/')
    joblib.dump(classifier, name+'/matcher.save')
    joblib.dump(vectorizer, name+'/vectorizer.save')
    joblib.dump(transformer, name+'/transformer.save')
    text_file = open(name+"/info.txt", "w")
    text_file.write('ngrams:'+str(info.ngrams)+'\n')
    text_file.write('stemming:'+str(info.stemming)+'\n')
    text_file.write('weighting'+info.weighting+'\n')
    text_file.close()

def save_classifier_mllib(classifier,  name):
    if not os.path.exists(name+'/'):
        os.makedirs(name+'/')
    joblib.dump(classifier, name+'/matcher.save')
  
def map_classes(mapper_file, in_class):
    classes = []
    if (mapper_file != None):
        with open(mapper_file, "r") as ins:
            for line in ins:
                try:
                    line_array = line.split('\t')
                    if (len(line_array) >= 2):
                        ind = line_array[1].strip('\n').strip(' ').lower()
                        industry = in_class.strip(' ').lower()
                        if (ind == industry):
                            classes.append(line_array[0])
                except:
                    pass
    return classes

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Module-level global variables for the `tokenize` function below
PUNCTUATION = set(string.punctuation)
STOPWORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()

# Function to break text into "tokens", lowercase them, remove punctuation and stopwords, and stem them
def tokenize(text):
    tokens = word_tokenize(text)
    lowercased = [t.lower() for t in tokens]
    no_punctuation = []
    for word in lowercased:
        punct_removed = ''.join([letter for letter in word if not letter in PUNCTUATION])
        no_punctuation.append(punct_removed)
    no_stopwords = [w for w in no_punctuation if not w in STOPWORDS]
    stemmed = [STEMMER.stem(w) for w in no_stopwords]
    return [w for w in stemmed if w]

def binary_labels(dictionary, label):
    dictionary_binary = {}
    for d in dictionary:
        if (d == label):
            dictionary_binary[d] = 1
        else:
            dictionary_binary[d] = 0
    return dictionary_binary

def onet_classification_spark():
    # start time
    start = timeit.timeit()
    # initializing spark context
    sc = SparkContext(appName='Extractor', pyFiles=[\
    '/home/hadoop/labor/rebuildd/extractor.py','/home/hadoop/labor/rebuildd/utill.py'])
    # read textual file
    data_raw = sc.textFile('s3://dssg-labor/JobDetails1.txt')
    # data_raw = sc.textFile('s3://dssg-labor/*.txt')
    # parse lines as json
    data = data_raw.map(lambda line: json.loads(line))
    # filter out unlabeled rows
    data = data.filter(lambda line: line['onettitle'] != '')
    # create (label,text) tuples
    data_pared = data.map(lambda line: (line['onettitle'].encode('utf-8'), line['jobdesc'].encode('utf-8')))

    # initialize hasher
    htf = HashingTF(50000)

    # read uniq title labels
    title_dict = {}
    utill.read_file_dict_keys("/home/hadoop/labor/tests/onet_classification_spark/uniq_onettitles.txt",title_dict)
    for t in title_dict:
        print t
    
    # create labels dictionary
    dictionary = {}
    #lbl_dict = data_pared.reduceByKey(lambda x,y:x)
    lbl_dict = data_pared.map(lambda (x,y): x)
    lbl_dict = lbl_dict.distinct()
    lbls = lbl_dict.collect()
    br = 0
    for l in lbls:
        dictionary[l] = br
        br += 1
        print (l,br)
   
    # create list of label dictionaries
    dictionary_list = []
    for d in dictionary:
        dic = binary_labels(dictionary,d)
        dictionary_list.append(dic)
    
    # tokenize
    data_hashed = data_pared.map(lambda (label, text): (dictionary[label], tokenize(text)))
    
    # hashing words
    data_hashed = data_pared.map(lambda (label, text): (label, htf.transform(text)))
    
    # save data rdd
    #joblib.dump(data_hashed, 'data_hashed.save')

    # save dictionary
    joblib.dump(dictionary, 'dictionary.save')    
    
    # save hasher
    joblib.dump(htf, 'htf.save')
    br = 0
    for d in dictionary:
        # setting labelsi
        dic = dictionary_list[br]
        br += 1
        train_hashed = data_hashed.map(lambda (label, text): LabeledPoint(dic[label], text))
    
        # spliting dataset
        # train_hashed, test_hashed = data_hashed.randomSplit([0.7, 0.3])
 
        # create the model
        print("create SVM"+str(d))
    
        model = SVMWithSGD.train(train_hashed, iterations=100)
        save_classifier_mllib(model, "SVM_"+str(dictionary[d]))
        print "done "+str(br)
    
    end = timeit.timeit()
    print end - start

def onet_classification_spark_classify(text, fname):
    #htf = HashingTF(50000)
    htf = joblib.load('htf.save')
    tokens = tokenize(text)
    vec = htf.transform(text)
    dictionary = joblib.load('dictionary.save')
    dictionary_rev = {}
    for d in dictionary:
        dictionary_rev[dictionary[d]] = d

    max_prob = -1
    max_class = "none"
    for i in range(1,30):
        model = joblib.load(fname+"_"+str(i)+"/matcher.save")
        model.clearThreshold()
        p = model.predict(vec)
        if (p > max_prob):
            max_prob = p
            max_class = dictionary_rev[i]
        print p,dictionary_rev[i]
    print "CLASS",max_class,max_prob

def onet_classification_spark_scikit():
    # initializing spark context
    sc = SparkContext(appName='Extractor', pyFiles=[\
    '/home/hadoop/labor/rebuildd/extractor.py','/home/hadoop/labor/rebuildd/utill.py'])
    # read textual file
    data_raw = sc.textFile('s3://dssg-labor/JobDetails1.txt').sample(False, 0.1, 2)
    # parse lines as json
    data = data_raw.map(lambda line: json.loads(line))
    # filter out unlabeled rows
    data_pared = data.filter(lambda line: line['onettitle'] != '')
    # create (label,text) tuples
    data_pared = data_pared.map(lambda line: (line['onettitle'].encode('utf-8'), line['jobdesc'].encode('utf-8')))
    # create labels dictionary
    dictionary = {}
    lbl_dict = data_pared.map(lambda (x,y): x)
    lbl_dict = lbl_dict.distinct()
    lbls = lbl_dict.collect()
    br = 0
    for l in lbls:
        dictionary[l] = br
        br += 1
        print (l,br)

    descriptions = data_pared.map(lambda (label, text): tokenize(text)).collect()
    categories = data_pared.map(lambda (label, text): label).collect()
    vectorizer = CountVectorizer(lowercase=True, ngram_range=(1, 1), stop_words='english');
    print(categories)
