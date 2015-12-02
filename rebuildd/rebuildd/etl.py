__author__ = 'Ahuja'

from sqlalchemy import create_engine #Use this to connect to
import pandas as pd
from settings import * #imports constants for DB AUTH

def connect_to_db(database_string):
    try:
        database_engine = create_engine(database_string) #Creating a connection/engine to the database.
        return database_engine
    except:
        print "Failed to connect"


def get_uniq_onettitle(database_engine):

    CBOnetTitles = pd.read_sql("SELECT distinct onettitle from cb_jobdetails",database_engines)
    titles = CBOnetTitles.ix[:,0].tolist()
    title_dict = {}
    for i, t in enumerate(titles):
        title_dict[t] = i
    return title_dict


def skills_etl_insert(rows, skill_list): #Working on this - Ahuja
    rows = rows[2:]
    rows = rows[:-2]
    rows = string.replace(rows, "u\'","\'")
    rows = rows.split('), (')
    for row in rows:
        skill_list.append("insert into skill_occurance values(default,"+row+")") #Clean this up from sql insert statement to

def skills_etl(filename): #All slaves call the other function so that they can run sql stuff
    # Connect to db
    conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
    password=DB_PWD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    # Read the file
    sc = SparkContext(appName='skills_etl')
    rdd = sc.textFile(filename)
    # Do insert for each line
    rdd1 = rdd.map(lambda l: skills_etl_insert(l,conn,cursor))
    #skills_etl_insert(rdd.first())
    print rdd.first()

def skills_etl_nospark(filename): #not working
    # Read the file
    sc = SparkContext(appName='skills_etl', pyFiles=['/home/hadoop/labor/dist/rebuildd-0.1-py2.7.egg', '/home/hadoop/labor/rebuildd/extractor.py','/home/hadoop/labor/rebuildd/utill.py'])
    rdd = sc.textFile(filename)
    skill_list = []
    f = rdd.collect()
    for line in f:
        skills_etl_insert(line, skill_list)

    text_file = open("skill_occurance.sql", "w")
    for s in skill_list:
        text_file.write(s+";\n")
    text_file.close()





