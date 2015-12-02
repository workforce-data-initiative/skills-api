###########
# Imports #
###########

import sys
from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import distinct
import os
import settings
from collections import Counter
import string
import pandas as pd
import pandas_highcharts as pdhc
import itertools
import json
import joblib
from operator import itemgetter
from rebuildd import transitions
from rebuildd import lodes
from rebuildd import matcher_nsp

#################
# configuration #
#################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.PUBLIC_DATABASE_CONN
db = SQLAlchemy(app)

##########
# Routes #
##########

#Index redirects to about page
@app.route('/')
def index():
    return redirect(url_for('about'))

#About page
@app.route('/about')
def about():
    return render_template('about.html')

# API documentaion page
@app.route('/api')
def api():
    return render_template('api.html')

##########
#  API   #
##########

# Get list of industry names, codes and tracts
@app.route('/api/industries_and_tracts', methods=['GET'])
def industries_and_tracts():
    n = lodes.get_industries_names_list()
    c = lodes.get_industries_codes_list()
    t = lodes.get_tracts()
    out = {}
    out["indNames"] = n["names"]
    out["indCodes"] = c["codes"]
    out["tracts"] = t["tracts"]
    return json.dumps(out)

# Get job transitions graph based on given treshold
@app.route('/api/get_transitions/<treshold>', methods=['GET'])
def get_transitions(treshold):
    return lodes.get_transitions(treshold)

# Get posing label based on text
@app.route('/api/match/<text>', methods=['GET'])
def match(text):
    print("INPUT:")
    print(text)
    c = matcher_nsp.classify("SVM/", text)
    out = {}
    out["onet"] = c
    return json.dumps(out)

# Get top N industries for specified tract
@app.route('/api/census_tract/<tract>/<top>', methods=['GET'])
def tract_industry_plot(tract, top):
    out = {}
    j = lodes.genTractInd(int(tract), int(top), False)
    return j

# Get precalculated ids of clusters for each tract. Clustering is based on industry composition
@app.route('/api/industry_kmeans/<k>', methods=['GET'])
def industry_kmeans(k):
    print "INDUSTRY KMEANS"
    #j = lodes.industry_kmeans(int(k))
    j = lodes.industry_kmeans_from_db()
    return j

# Returns list of skills for occupation based on sufix 
@app.route('/api/auto_occupation/<word>', methods=['GET'])
def auto_complete_occupation(word):
    word = word.lower()
    word = word.capitalize()
    df = pd.read_sql_query("select onet_title from uniq_onettitle where onet_title like '"+word+"%'",db.engine.connect().connection)
    l = json.dumps(df.ix[:,0].tolist())
    return l

# Return nowcasted values for industries
@app.route('/api/industry_nowcasting/<tract>/<industry>', methods=['GET'])
def industry_nowcasting_raw(tract, industry):
    df = pd.read_sql_query("select index, to_char(date, 'YYYY-MM'), industry_lodes, tract, min_emp, predicted_emp, max_emp from nowcast_predict where tract = "+tract+" and industry_lodes = '"+industry+"' order by date",db.engine.connect().connection)
    out = {}
    out["tract"] = df.ix[0,3]
    out["timepoints"] = df.ix[:,1].tolist()
    out["min_emp"] = df.ix[:,4].tolist()
    out["pred_emp"] = df.ix[:,5].tolist()
    return json.dumps(out)

# Return nowcasted values for industries
@app.route('/api/industry_nowcasting_hc/<tract>/<industry>', methods=['GET'])
def industry_nowcasting_hc(tract, industry):
    out = lodes.industry_nowcasting(tract, industry) 
    return out

# Get exponential moving average from list. S in input list, n is number of previous timepoints
def ema(s, n):
    ema = []
    j = 1
    #get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)
    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)
    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    return ema

# Get skills timeseries for an occupation and saved it in the skills_precalculated table
@app.route('/api/skills_pre/<occupation>/<top>', methods=['GET'])
def skills_pre(occupation, top):
    skills = occupation_skills(occupation, top)
    series = skills["series"]
    for s in series:
        name = s["name"]
        ser = ""
        total = 0
        data = s["data"]
        for d in data:
            total += d
            ser = str(d)+','
        
# Get extracted skills timeseries. For given occupation it returnes N top skills
@app.route('/api/occupation_skills/<occupation>/<top>', methods=['GET'])
def occupation_skills(occupation, top):

    df_months = pd.read_sql_query("select * from uniq_months order by uniq_months",db.engine.connect().connection)
    months_list = df_months.ix[:,0].tolist()
    
    months_dict = {}
    for m in months_list:
        months_dict[m] = 0
   
    df = pd.read_sql_query("select count(*), to_char(created, 'YYYY-MM'),\
    keyword from skill_occurance_postings where onet_title = '"+occupation+"'\
    group by keyword, created\
    order by keyword, created",db.engine.connect().connection)   
    
    counts = df.ix[:,0].tolist()
    months = df.ix[:,1].tolist()
    skills = df.ix[:,2].tolist()
     
    skills_hist = Counter(skills)
    #skills_sorted = sorted(skills, key=lambda x: skills_hist.get(x,0),reverse=True)
    skills_sorted = skills_hist.most_common()
    print skills_sorted
    skills_sorted = [i[0] for i in skills_sorted]
    #skills_sorted = skills_sorted.keys()
    
    top = int(top)
    if (len(skills_sorted)>top):
        skills_sorted = skills_sorted[0:top]
   
    uniq_skills = list(set(skills))
    skills_dict = {} 
   
    for s in skills_sorted:
        skills_dict[s] = dict(months_dict)

    for i,s in enumerate(skills):
        skill_ = skills[i]
        if (skills_dict.has_key(skill_)):
            month_ = months[i]
            count_ = counts[i]
            skills_dict[skill_][month_] = count_
    
    # create json object
    out = {}
    
    # fill data
    series = []
    for s in skills_dict:
        obj = {}
        obj['name'] = s
        obj['data'] = ema(list(skills_dict[s].values()),10)
        #obj['data'] = skills_dict[s].values()
        #obj['data'] = list(skills_dict[s].values())
        series.append(obj) 
    out['series'] = series
    
    # y-axis
    xAxis = {}
    categories = {}
    categories["categories"] = months_list
    out["xAxis"] = categories
    
    # Title
    title = {}
    title["text"] = "Skill for Occupation"
    out["title"] = title 
    
    # Subtitle
    subtitle = {}
    subtitle["text"] = occupation
    out["subtitle"] = subtitle

    # yAxis
    title = {}
    title["text"] = "Demand"
    title0 = {}
    title0["title"] = title
    out["yAxis"] = title0
    
    return json.dumps(out)

# Main
if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0')
