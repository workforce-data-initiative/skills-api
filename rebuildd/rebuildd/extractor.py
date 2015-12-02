import os
import sys
import collections
import string
import numpy
import cPickle
import marshal
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import rake 
import operator
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from pyspark import SparkContext, SparkConf
import json
import numpy
import pandas

git_root = sys.path[0].split("/rebuildd", 1)[0]
sys.path.insert(1,git_root)
from rebuildd import settings
#from rebuildd import utill

# Test extractor
def test():
    print "Extractor script works!"

# For unstructured input text, return sorted scored dictionary of RAKE keyword phrases
def get_rake_keywords(text_, stoppath = None):
    if stoppath is None:
        stoppath = "./labor/res/stopwords/SmartStoplist.txt" #Issue 1:
    rake_object = rake.Rake(stoppath, 5, 3, 4)
    sentenceList = rake.split_sentences(text_)
    stopwordpattern = rake.build_stop_word_regex(stoppath)
    phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern)
    wordscores = rake.calculate_word_scores(phraseList)
    keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)
    sortedKeywords = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedKeywords


# For unstructured text return dictionary of sorted skill
def get_skills(text_, skillpath = None):
    skills = {}
    if skillpath is None:
        skillpath = './labor/res/skills/about_linkedin_skills.txt'
    utill.read_file_dict_keys(skillpath,skills)
    tokens = nltk.word_tokenize(text_)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)
    skills_final = []
    for t in tagged:
        if (len(t)>1):
            if (t[1] == 'NN' or t[1][0] == 'V'):
                if (skills.has_key(t[0])):
                    skills_final.append(t[0])

    #hist = Counter(skills_final)
    #return hist
    return skills_final

# For unstructured text return dictionary of sorted skill
# With preloaded skill set dictionary
# Do tokenization and Part of Speech tagging
def get_skills_pss_pos(text_, skills):
    tokens = nltk.word_tokenize(text_)
    tagged = nltk.pos_tag(tokens)
    #entities = nltk.chunk.ne_chunk(tagged)
    skills_final = []
    for t in tagged:
        if (len(t)>1):
            if (t[1] == 'NN' or t[1][0] == 'V'):
                if (skills.has_key(t[0])):
                    skills_final.append(t[0])

    return skills_final

# For unstructured text return dictionary of sorted skill
# With preloaded skill set dictionary
# Spark
def get_skills_pss_sp(data_pared, skills):
    return data_pared.map(lambda (jobdesc): (get_skills_pss(jobdesc, skills)))

def get_skills_pss2(jobdesc, skills, cat, jobid, ind, tit, otit, ctit, country, state, city, created):
    tokens = nltk.word_tokenize(jobdesc)
    tagged = nltk.pos_tag(tokens)
    skills_final = []
    for t in tagged:
        if (len(t)>1):
            if (t[1] == 'NN' or t[1][0] == 'V'):
                if (skills.has_key(t[0])):
                    skills_final.append(jobid, t[0], cat, ind, tit, otit, ctit, country, state, city, created)

    return skills_final

# 
def get_skills_vectorizer(jobdesc, vectorizer, D, jobid, cat, ind, tit, otit, ctit, country, state, city, created):
    mat = vectorizer.transform([jobdesc])
    indices = D.get_feature_names()
    for m in mat:
        indiarray = m.indices
        wordarray = []
        for indi in indiarray:
            wordarray.append((jobid, indices[indi], cat, ind, tit, otit, ctit, country, state, city, created))
    return wordarray

def get_skills_vectorizer_sql(jobdesc, vectorizer, D, jobid, cat, ind, tit, otit, ctit, country, state, city, created):
    mat = vectorizer.transform([jobdesc])
    indices = D.get_feature_names()
    for m in mat:
        indiarray = m.indices
        wordarray = []
        for indi in indiarray:
            '''
            wordarray.append("insert into skill_occurance_postings values(\
'default','"+str(jobid).encode('utf8')+"','"+str(indices[indi]).encode('utf8').replace('\'','\\\'')+"',\
   
            '''  
            try:      
                wordarray.append("insert into skill_occurance_postings values(\
default,'"+str(jobid).encode('utf8')+"','"+str(indices[indi]).encode('utf8').replace('\'','\\\'')+"',\
'"+str(cat).encode('utf8').replace('\'','\\\'')+"','"+str(ind).encode('utf8').replace('\'','\\\'')+"',\
'"+str(tit).encode('utf8').replace('\'','\\\'')+"','"+str(otit).encode('utf8').replace('\'','\\\'')+"',\
'"+str(ctit).replace('\'','\\\'')+"','"+str(country).encode('utf8').replace('\'','\\\'')+"',\
'"+str(state).encode('utf8')+"','"+str(city).encode('utf8')+"','"+str(created).encode('utf8')+"');\n")
            except:
                pass
    return wordarray

# Extract all skills and save in text file
# Use spark
# Simple unigram comparing with dictionary
def skill_extract_all(outname):
    # Test extractor
    test()
    sconf = SparkConf()
    conf = (SparkConf().setMaster("local[12]").setAppName("CountingSheep").set("spark.executor.memory", "2G").set("spark.storage.memoryFraction", "0.4"))
    #sc = SparkContext(conf=conf)
    #sc = SparkContext(conf=conf, pyFiles=['/home/hadoop/labor/dist/rebuildd-0.1-py2.7.egg', '/home/hadoop/labor/rebuildd/extractor.py','/home/hadoop/labor/rebuildd/utill.py'])    
    # Create Spark Context
    sc = SparkContext(appName='Extractor', pyFiles=['/home/hadoop/labor/dist/rebuildd-0.1-py2.7.egg', '/home/hadoop/labor/rebuildd/extractor.py','/home/hadoop/labor/rebuildd/utill.py'])
    # Load jobdetails files from S3
    #data_raw = sc.textFile('s3://dssg-labor/JobDetails1.txt')
    data_raw = sc.textFile('s3://dssg-labor/*.txt')    
    # Parse jobpostings as jsons
    data = data_raw.map(lambda line: json.loads(line))
    # Create job tuples from each line 
    data_pared = data.map(lambda line: (line['hashdid'], line['firstcategory'], line['firstindustry'], line['jobtitle'],\
    line['created'], line['onettitle'], line['carotenetitle'], line['countryname'], line['statename'], line['cityname'], line['jobdesc']))
    # Load skills dictionary
    skills = {}
    skills_rdd = sc.textFile('s3://dssg-labor/about_linkedin_skills')
    skills_list = skills_rdd.collect()
    # Load skills dictionary from public database 
    '''
    config_pub = utill.Config()
    config_pub.database = settings.PUBLIC_DATABASE_CONN
    dictionary = utill.read_from_db(config_pub, "SELECT * FROM skill_dictionary")
    dictionary = dictionary.ix[:,0].tolist()
    skills_list = dictionary
    '''
    # Load skills vectorizer 
    transformer = CountVectorizer(lowercase=True, ngram_range=(1, 4), stop_words='english')
    D = transformer.fit(skills_list)
    # Creating skills dictionary
    skills = {}
    for s in skills_list:
        skills[s.lower()] = 1

    # Run stuff - first pass version
    '''
    res = data_pared.map(lambda (jobid, cat, ind, tit, created, otit, ctit, country, state, city, jobdesc):\
    (get_skills_pss2(jobdesc, skills, jobid, cat, ind, tit, otit, ctit, country, state, city, created)))
    '''
    # Run stuff - second pass version
    res = data_pared.map(lambda (jobid, cat, ind, tit, created, otit, ctit, country, state, city, jobdesc):\
    (get_skills_vectorizer_sql(jobdesc, transformer, D, jobid, cat, ind, tit, otit, ctit, country, state, city, created)))
    #save output to s3
    rdd = res.flatMap(lambda l: l)    
    rdd.saveAsTextFile('s3://dssg-labor//'+outname)
    print len(l)
