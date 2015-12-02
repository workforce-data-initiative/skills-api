import os
import pandas as pd
import numpy as np
import json
import psycopg2
from collections import Counter
from settings import *

def get_transitions(treshold):
    conn = None
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
        password=DB_PWD, host=DB_HOST, port=DB_PORT);
        print "Connected"
    except:
        print "Failed to connect"

    df = pd.read_sql("select * from jobtransition where rate > "+str(treshold), conn)

    N1 = df.ix[0,:].tolist()
    N2 = df.ix[1,:].tolist()
  
    nodes = []
    links = []
    
    node_uniq = {}

    # get uniq nodes from col1
    for i,n1 in enumerate(N1):
        if (node_uniq.has_key(n1) == False):
            node_uniq[n1] = i
    
    # get uniq nodes from col2
    for i,n2 in enumerate(N2):
        if (node_uniq.has_key(n2) == False):
            node_uniq[n2] = i
   
    # fill nodes dict
    for n in node_uniq:
        d = {}
        nodes.append({'id': node_uniq[n], 'reflexive': False })

    for i,n1 in enumerate(N1):
        links.append({'source': node_uniq[N1[i]], 'target': node_uniq[N2[i]], 'left': False, 'right': True })

    out = {}
    out["nodes"] = nodes
    out["links"] = links

    return json.dumps(out)
    
