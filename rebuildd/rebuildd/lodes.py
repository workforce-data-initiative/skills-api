# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 07:36:12 2015
@author: Iwa
"""
from settings import * #DB AUTH SETTINGS

import os
import pandas as pd
import numpy as np
import json
import psycopg2
from sklearn.cluster import KMeans
from collections import Counter
from snap import *

# Dictionary of industries
lodesFieldDict = {
'CNS01': 'NAICS sector 11, (Agriculture, Forestry, Fishing and Hunting)',
'CNS02': 'NAICS sector 21, (Mining, Quarrying, and Oil and Gas Extraction)',
'CNS03': 'NAICS sector 22, (Utilities)',
'CNS04': 'NAICS sector 23, (Construction)',
'CNS05': 'NAICS sector 31-33, (Manufacturing)',
'CNS06': 'NAICS sector 42 (Wholesale Trade)',
'CNS07': 'NAICS sector 44-45 (Retail Trade)',
'CNS08': 'NAICS sector 48-49 (Transportation and Warehousing)',
'CNS09': 'NAICS sector 51 (Information)',
'CNS10': 'NAICS sector 52 (Finance and Insurance)',
'CNS11': 'NAICS sector 53 (Real Estate and Rental and Leasing)',
'CNS12': 'NAICS sector 54 (Professional, Scientific, and Technical Services)',
'CNS13': 'NAICS sector 55 (Management of Companies and Enterprises)',
'CNS14': 'NAICS sector 56 (Administrative and Support and Waste Management and Remediation Services)',
'CNS15': 'NAICS sector 61 (Educational Services)',
'CNS16': 'NAICS sector 62 (Health Care and Social Assistance)',
'CNS17': 'NAICS sector 71 (Arts, Entertainment, and Recreation)',
'CNS18': 'NAICS sector 72 (Accommodation and Food Services)',
'CNS19': 'NAICS sector 81 (Other Services [except Public Administration])',
'CNS20': 'NAICS sector 92 (Public Administration)'  }

# Get dictionary of industries. Key is SOC code, value is Industry name
def get_industries():
    dic = lodesFieldDict
    indCode = {}
    for d in dic:
       indCode[d] = dic[d].split('(')[1][:-1]
    return indCode

# Get list of industry names
def get_industries_names_list():
    dic = lodesFieldDict
    indNames = []
    for d in dic:
       indNames.append(dic[d].split('(')[1][:-1])
    out = {}
    out["names"] = indNames
    return out

# Get list of industry codes
def get_industries_codes_list():
    dic = lodesFieldDict
    indNames = []
    for d in dic:
       indNames.append(d)
    out = {}
    out["codes"] = indNames
    return out

# Get list of tracts
def get_tracts():
    conn = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
        password=DB_PWD, host=DB_HOST, port=DB_PORT);
        print "Connected"
    except:
        print "Failed to connect"
    
    df = pd.read_sql("select distinct cast(tract as varchar) from nowcast_predict order by tract", conn)
    tracts = df.ix[:,0].tolist()
    out = {}
    out["tracts"] = tracts
    return out

# Get transition graph statistics
def graph_stat(G):
    return 0

# Get transitions graph
def get_transitions(treshold):
    conn = None
     
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
        password=DB_PWD, host=DB_HOST, port=DB_PORT);
        print "Connected"
    except:
        print "Failed to connect"

    print "select * from job_trans where rate > "+str(treshold)
    df = pd.read_sql("select onetsoc1, onetsoc2, rate,\
(select title from onet_occupation_data where onetsoc_code = onetsoc1) as \"title1\",\
(select title from onet_occupation_data where onetsoc_code = onetsoc2) as \"title2\"\
 from job_trans where onetsoc1 <> onetsoc2 and rate >= "+str(treshold), conn)
    
    N1 = df.ix[:,0].tolist()
    N2 = df.ix[:,1].tolist()
    V = df.ix[:,2].tolist() 
    T1 = df.ix[:,3].tolist()
    T2 = df.ix[:,4].tolist()

    print len(N1)
    nodes = []
    links = []

    node_uniq = {}
    node_id = 0
    
    # snap graph
    G1 = TUNGraph.New()    

    # get uniq nodes from col1
    for i,n1 in enumerate(N1):
        if (node_uniq.has_key(n1) == False):
            node_uniq[n1] = node_id
            nodes.append({'name': T1[i], 'group': 1, 'id':node_id, 'soc':n1})
            G1.AddNode(node_id)
            node_id = node_id + 1

    # get uniq nodes from col2
    for i,n2 in enumerate(N2):
        if (node_uniq.has_key(n2) == False):
            node_uniq[n2] = node_id
            nodes.append({'name': T2[i], 'group': 1, 'id':node_id, 'soc':n2})
            G1.AddNode(node_id)
            node_id = node_id + 1
   
    for i,n1 in enumerate(N1):
        links.append({'source': node_uniq[N1[i]], 'target': node_uniq[N2[i]], 'value': round(V[i],2) })
        G1.AddEdge(node_uniq[N1[i]],node_uniq[N2[i]])
    
    CmtyV = TCnComV()
    modularity = CommunityCNM(G1, CmtyV)
    cmty_dict = {}
    for i,Cmty in enumerate(CmtyV):
        for NI in Cmty:
            cmty_dict[NI] = i    

    for n in nodes:
        nid = n['id']
        node = G1.GetNI(nid)
        deg = node.GetDeg()
        n['deg'] = deg
        n['group'] = cmty_dict[nid]

    out = {}
    out["nodes"] = nodes
    out["links"] = links

    return json.dumps(out)

# Get Nowcasted values for specified industry and tract
def industry_nowcasting(tract, industry):
    conn = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
        password=DB_PWD, host=DB_HOST, port=DB_PORT);
        print "Connected"
    except:
        print "Failed to connect"

    df = pd.read_sql_query("select index, to_char(date, 'YYYY-MM'), industry_lodes, tract, min_emp, predicted_emp, max_emp from nowcast_predict where tract = "+tract+" and industry_lodes = '"+industry+"' order by date",conn)
    timepoints = df.ix[:,1].tolist()
    min_emp = df.ix[:,4].tolist()
    pred_emp = df.ix[:,5].tolist()
    max_emp = df.ix[:,6].tolist()
    out = {}
    series = []
    series.append({"name": "Min employement", "data": min_emp})
    series.append({"name": "Predicted employement", "data": pred_emp})
    series.append({"name": "Max employement", "data": max_emp})

    out["xAxis"] = {"categories": timepoints}
    out["yAxis"] = {"title": {"text": "employement"}, 'min': 0.1}
    out["title"] = {"text": "Industry employement nowcasting"}
    out["subtitle"] = {"text": lodesFieldDict[industry]}
    out["series"] = series
    return json.dumps(out)

# Compute k-means industry composition clusters
def industry_kmeans_df(k):
    conn = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
        password=DB_PWD, host=DB_HOST, port=DB_PORT);
        print "Connected"
    except:
        print "Failed to connect"

    df = pd.read_sql("select * from IllinoisLodesTract", conn)
    indFields = df.keys().tolist()
    df.set_index('tract',inplace = True)
    
    ## Remove unneeded fields and prepare dataframe for K-Mean algorithm
    indFields.remove('tract')
    indFields.remove('year')
    indFields.remove('C000')
    indFields.remove('index')
    dfRecent = df[df['year'] == 2011] # Keep only most recent year
    
    dfRecent = dfRecent.div(dfRecent.C000, axis = 'index')
    dfRecent = dfRecent[indFields]
    n = dfRecent.shape[0]
    estimator =  KMeans(n_clusters=k)
    data_matrix = dfRecent.as_matrix()
    A = estimator.fit_predict(data_matrix)
    centers = estimator.cluster_centers_   
    return dfRecent,A,centers

# 
def industry_kmeans_from_db():

    conn = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
        password=DB_PWD, host=DB_HOST, port=DB_PORT);
        print "Connected"
    except:
        print "Failed to connect"

    df = pd.read_sql("select * from industry_clusters", conn)
    
    tracts = df.ix[:,0].tolist()
    clusters = df.ix[:,1].tolist()

    out = {}
    for i, t in enumerate(tracts):
        out[str(t)] = int(clusters[i])

    return json.dumps(out)

# Compute tract clusters based on industry composition and save to rebuildd database
def industry_kmeans_db(k):
    kmeans = industry_kmeans_df(k);
    dfRecent = kmeans[0]
    A = kmeans[1]
    centers = kmeans[2]

    conn = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
        password=DB_PWD, host=DB_HOST, port=DB_PORT);
        print "Connected"
    except:
        print "Failed to connect"

    out = []
    tracts = dfRecent.index
    dfRecent['cluster'] = A
    for i, t in enumerate(tracts):
        out.append((str(t),int(A[i])))
 
    cur = conn.cursor()
    
    cur.execute("truncate table industry_clusters")

    for o in out:
        cur.execute("INSERT INTO industry_clusters (tract, cluster_id) VALUES (%s, %s)", (o[0], o[1]))
        
    conn.commit()

#
def industry_kmeans(k):
    kmeans = industry_kmeans_df(k);
    dfRecent = kmeans[0]
    A = kmeans[1]
    centers = kmeans[2]
    
    out = {}
    tracts = dfRecent.index
    dfRecent['cluster'] = A
    for i, t in enumerate(tracts):
        out[str(t)] = int(A[i])
    
    return json.dumps(out)

# This function takes in filename of Illinois WAC lodes data and censustract
def genTractInd(tract,top,plot):
    lodesFile = "IllinoisTractInd.csv"
    print os.listdir(os.getcwd())
    df = pd.read_csv(lodesFile)
    
    '''
    conn = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
        password=DB_PWD, host=DB_HOST, port=DB_PORT);
        print "Connected"
    except:
        print "Failed to connect"


    df = pd.read_sql("select * from IllinoisLodesTract", conn)
    '''

    dfTract = df[df['tract']==tract]
    
    dfTract.set_index('year',inplace = True)
    indFields = dfTract.keys().tolist()
    indFields.remove('C000')
    indFields.remove('tract')
    dfITract = dfTract[indFields]  #dataframe that only has no total count
    erlyYr = min(dfTract.index)
    latestYr = max(dfTract.index)
    currIndBrkDwn = dfITract.loc[latestYr]
    indGrowth = dfITract.loc[latestYr]/(dfITract.loc[erlyYr]+0.000001)
    indGrowth.sort(ascending = False, inplace = True)
    currIndBrkDwn.sort(ascending = False, inplace = True)
    topCurrInd = currIndBrkDwn.index[:top]
    topGrowthInd = indGrowth.index[:top]
    
    if (plot):
        dfTract[topCurrInd].plot()
        dfTract[topGrowthInd].plot()
    topIndsM = dfTract[topCurrInd].as_matrix()
    #print dfTract[topCurrInd]
    #print dfTract[topGrowthInd]
    
    topCurrIndList = []
    for ind in topCurrInd:
        tempDict = {}
        tempDict['name'] = lodesFieldDict[ind]
        tempDict['data'] = [int(i) for i in dfTract[ind].tolist()]
        topCurrIndList.append(tempDict)
        
    topGrowthIndList = []
    for ind in topGrowthInd:
        tempDict = {}
        tempDict['name'] = lodesFieldDict[ind]
        tempDict['data'] = [int(i) for i in dfTract[ind].tolist()]
        topGrowthIndList.append(tempDict)
    
    outCurr = {}
    outCurr['series'] = topCurrIndList
    outCurr['title'] = {'text': "Top " + str(top) + " Current Industries by Employment"}
    outCurr['subtitle'] = {'text': "Census Tract Fipscode: " +  str(tract)}
    outCurr['xAxis'] = {'categories': [int(i) for i in dfTract.index.tolist()]}
    outCurr['yAxis'] = {'title':{'text': "Number of Employment"}}
    outGrowth = {}
    outGrowth['series'] = topGrowthIndList
    outGrowth['title'] = {'text': "Top " + str(top) + " Fastest Growing Industries By Employment in last Decade"}
    outGrowth['subtitle'] = {'text': "Census Tract Fipscode: " +  str(tract)}
    outCurr['xAxis'] = {'categories': [int(i) for i in dfTract.index.tolist()]}
    outCurr['yAxis'] = {'title':{'text': "Number of Employment"}}
    
    out = {}
    out["loads"] = [dict(outCurr), dict(outGrowth)]    
    return json.dumps(out)
