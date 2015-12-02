# This file contains functions form manipulating data, reading/writing from db/files, etc.builds a model to predict O*NET Title of a job posting based on its description

###################
# Importing paths #
###################

import sys
git_root = sys.path[0].split("/tests", 1)[0]
sys.path.insert(1, git_root)

# -- Rebuildd settings - DB connections and other --

#This is a configuration file used by the rest of the project
from settings import *

# -- Database & Pandas --
import psycopg2
import sqlalchemy
import pandas as pd
import string
import collections
import numpy as np
from pyspark import SparkContext

sys.path.insert(1,'/home/hadoop/labor')

# -- Test function --
def test():
    print "ReBUILDD works!"

# -- Configuration object class --
class Config(object):
    database = CONSERV_DATABASE_CONN
    row_limit = -1
    def __init__(self):
        1  # do nothing

# -- Reading from database --
def read_from_db(config, sqlstring):
    
    # connect to database
    try:
        engine = sqlalchemy.create_engine(config.database)
        print "Connected"
    except:
        print "Failed to connect"
    
    # initialization of result variable
    result = None

    # execute select query
    try:
        if config.row_limit <= 0:
            result = pd.read_sql(sqlstring, engine)
        else:
            result = pd.read_sql(sqlstring + ' LIMIT ' + str(config.row_limit), engine)
    except:
        print "SQL Query Failed"

    # return dataframe
    return result

def skills_etl_insert(rows, skill_list):
    rows = rows[2:]
    rows = rows[:-2]
    rows = string.replace(rows, "u\'", "\'")
    rows = rows.split('), (')
    for row in rows:
        skill_list.append("insert into skill_occurance values(default," + row + ")")


def skills_etl(filename):
    # Connect to db
    conn = psycopg2.connect(database=DB_NAME, user=DB_USERNAME, \
        password=DB_PWD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    # Read the file
    sc = SparkContext(appName='skills_etl')
    rdd = sc.textFile(filename)
    # Do insert for each line
    rdd1 = rdd.map(lambda l: skills_etl_insert(l, conn, cursor))
    # skills_etl_insert(rdd.first())
    print rdd.first()

def skills_etl_sparksql():
    sc = SparkContext(appName='skills_etl')
    rdd = sc.textFile(filename)
    df = sqlContext.load(source="jdbc", url=JDBC_URL, dbtable="rebuildd")

# Read skill files saved to s3 and save it as a new txt file
def skills_etl_nospark(filename):
    # Read the file
    sc = SparkContext(appName='skills_etl', \
                      pyFiles=['/home/hadoop/labor/dist/rebuildd-0.1-py2.7.egg',
                               '/home/hadoop/labor/rebuildd/extractor.py', '/home/hadoop/labor/rebuildd/utill.py'])
    rdd = sc.textFile(filename)
    skill_list = []
    f = rdd.collect()
    for line in f:
        skills_etl_insert(line, skill_list)

    text_file = open("skill_occurance.sql", "w")
    for s in skill_list:
        text_file.write(s + ";\n")
    text_file.close()


# Read textual file line by line and add elements to the dictionary.
# Lines of files are keys for dictionary. Value for each element is 1 (int)
def read_file_dict_keys(file_path, dictionary_):
    with open(file_path, "r") as ins:
        br = 1
        for line in ins:
            try:
                line = line.strip('\n').lower()
                dictionary_[line] = br
                br += 1
            except:
                pass


# Read line by line of a file into a list
def read_file_desc(file_path, descriptions_):
    br = 0
    with open(file_path, "r") as ins:
        for line in ins:
            br += 1
            try:
                desc = ""
                for l in line_array:
                    desc += " " + l
                descriptions_.append(desc.encode('utf-8'))
            except:
                pass


# Read file line by line into categories and descriptions lists.
# First \t caracter delimits the categories from descriptions
def read_file_cat_desc(file_path, categories_, descriptions_, delimiter):
    with open(file_path, "r") as ins:
        for line in ins:
            try:
                line_array = line.split(delimiter)
                desc = ""
                if (len(line_array) >= 2):
                    for l in line_array:
                        desc += " " + l
                    descriptions_.append(desc.encode('utf-8'))
                    categories_.append(line_array[0])
            except:
                pass


# Read file line by line into categories and descriptions lists.
# First \t caracter delimits the categories from descriptions
# Read only those line that exist in provided list of classes
def read_file_spec_cat_desc(file_path, categories_, descriptions_, classes_):
    br = 0
    with open(file_path, "r") as ins:
        for line in ins:
            br += 1
            try:
                line_array = line.split('\t')
                desc = ""
                if (len(line_array) >= 2):
                    if (line_array[0] in classes_):
                        for l in line_array:
                            desc += " " + l
                        descriptions_.append(desc.encode('utf-8'))
                        categories_.append(line_array[0])
                        # descriptions_.append(desc)
            except:
                pass


# Function to get arguments from command line
def get_arguments(arg_names):
    args_ = dict(zip(arg_names, sys.argv))
    Arg_list = collections.namedtuple('Arg_list', arg_names)
    args_ = Arg_list(*(args_.get(arg, None) for arg in arg_names))
    return args_
