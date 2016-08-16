"""Extract, Transform, Load Utility."""

import os
import sys
import uuid
import hashlib

JOBS_UNUSUAL_TITLES = 'jobs_unusual_titles.tsv'
JOBS_SKILLS = 'jobs_skills.tsv'
JOBS_MASTER = 'jobs_master.tsv'
JOBS_TITLES = 'jobs_titles.tsv'
SKILLS_IMPORTANCE = 'skills_importance.tsv'
SKILLS_MASTER = 'skills_master.tsv'
JOBS_SKILLS = 'jobs_skills.tsv'

def process_file(filepath):
    """Route a file to its appropriate processing subroutine.

    Each file that is produced by the machine learning pipeline must be
    preprocessed into a form that is appropriate for storage in a relation
    database. At present, the preprocessing steps must be handwritten by an
    engineer who is familiar with the dataset. 

    Args:
        filepath (str, required): The path and name of the file to process.

    """

    # TODO(agileronin): Ultimately, find a more streamlined way to process
    # files automatically.

    file_path = filepath.strip().split('/')
    filename = file_path[len(file_path) - 1]

    # Extract datasets
    if filename == 'interesting_job_titles.csv':
        interesting_job_titles(filepath)
    elif filename == 'job2skill_column_skill_index.tsv':
        job_to_skills(filepath)
    elif filename == 'job_titles_master_table.tsv':
        job_titles(filepath)
    elif filename == 'ksas_importances.csv':
        skills_importance(filepath)
    elif filename == 'skills_master.csv':
        pass
    elif filename == 'skills_master_table.tsv':
        skills(filepath)
    else:
        # TODO(agileronin): Provide a more graceful approach for handling files
        # without processing rules.
        print 'No rules on how to process file ' + filepath
        sys.exit(1)   


def get_md5(text):
    """Compute the MD5 checksum of a specified string of text.
    
    Args:
        text(str, required): Text to calculate MD5 sum.
    
    """

    return str(hashlib.md5(text).hexdigest())

def extract_data(filepath, extract_header=True):
    """ Extracts the contents of a text file into a Python list.

    A helper method for reading the contents of a text file into a list.

    Args:
        filepath(str, required): The path and name of the file to extract the 
            content from.
        extract_header(boolean, optional): Determine whether or not to dump the
            header (first line) of the content before it is returned. Default is
            True.
    Return:
        The file content as a Python list. 

    """
    with open(filepath, 'r') as f:
        content = f.readlines()
    
    # Strip the header if necessary
    if extract_header:
        content = content[1:]
    return content
    

def interesting_job_titles(filepath):
    """Process the interesting job titles text file.

    Args:
        filepath(str, required): The path and name of the file to process.

    """
    content = extract_data(filepath, False)
    fh = open(os.path.join(os.getcwd(), 'etl', 'stage_2', JOBS_UNUSUAL_TITLES), 'w')
    
    fh.write('onet_soc_code\ttitle\tdescription\n')
    for line in content:
        line = line.strip().split('\t')
        fh.write(line[2] + '\t' + line[0] + '\t' + line[1] + '\n')
    fh.close()

def job_to_skills(filepath):
    """Process job to skills mapping text file
    
    Args:
        filepath(str, required): The path and name of the file to process.

    """
    content = extract_data(filepath)
    fh = open(os.path.join(os.getcwd(), 'etl', 'stage_2', JOBS_SKILLS), 'w')

    fh.write('onet_soc_code\tskill_uuid\tskill_name\tcount\n')
    for line in content:
        line = line.strip().split('\t')
        fh.write(line[3] + '\t' + get_md5(line[5]) + '\t' + line[5] + '\t' + line[6] + '\n')
    fh.close()

def job_titles(filepath):
    """Process job titles mapping text file
    
    Args:
        filepath(str, required): The path and name of the file to process.

    """
    content = extract_data(filepath)
    parent_uuid = []
    fh = open(os.path.join(os.getcwd(), 'etl', 'stage_2', JOBS_MASTER), 'w')
    fh.write('onet_soc_code\tcategory_title\tdescription\tcategory_uuid\n')

    fh2 = open(os.path.join(os.getcwd(), 'etl', 'stage_2', JOBS_TITLES), 'w')
    fh2.write('onet_soc_code\tjob_title\tjob_uuid\tcategory_uuid\n')

    for line in content:
        line = line.strip().split('\t')
        if line[1] in parent_uuid:
            fh2.write(line[1] + '\t' + line[2] + '\t' + get_md5(line[2]) + '\t' + get_md5(line[3]) + '\n')
        else:
            parent_uuid.append(line[1])
            fh.write(line[1] + '\t' + line[2] + '\t' + line[4] + '\t' + get_md5(line[3]) + '\n')
    
    fh.close()
    fh2.close()

def skills_importance(filepath):
    """Consolidate the importance and level of each skill per job title.

    Args:
        filepath(str, required): The path and name of the file to process.

    Note:
        This subroutine assumes that importance and level for each skill are grouped consistently
        and that there are no missing rows in the dataset.

    """
    content = extract_data(filepath)
    fh = open(os.path.join(os.getcwd(), 'etl', 'stage_2', SKILLS_IMPORTANCE), 'w')
    fh.write('onet_soc_code\tskill_uuid\timportance_value\timportance_n' + \
                '\timportance_stderr\timportance_lower_ci\timportance_upper_ci\t' + \
                'level_value\tlevel_n\tlevel_stderr\tlevel_lower_ci\tlevel_upper_ci\n')
    
    stats = ''
    found_level = False
    for line in content:
        line = line.strip().split(',')
        if not found_level:
            stats += line[1] + '\t' + get_md5(line[3].lower()) + '\t' + line[5] + '\t' + line[6] + '\t' + line[7] + \
            '\t' + line[8] + '\t' + line[9] + '\t'    
            found_level = True
        else:
            stats += line[5] + '\t' + line[6] + '\t' + line[7] + '\t' + line[8] + '\t' + line[9] + '\n'
            fh.write(stats)
            found_level = False
            found_importance = True
            stats = ''
        
    fh.close()

def skills(filepath):
    """Consolidate the names and uuids for skills.

    Args:
        filepath(str, required): The path and name of the file to process.

    """
    content = extract_data(filepath)
    fh = open(os.path.join(os.getcwd(), 'etl', 'stage_2', SKILLS_MASTER), 'w')
    fh2 = open(os.path.join(os.getcwd(), 'etl', 'stage_2', JOBS_SKILLS), 'w')
    skill_uuids = []
    fh.write('uuid\tskill_name\tdescription\n')
    fh2.write('skill_uuid\tonet_soc_code\n')
    for line in content:
        line = line.strip().split('\t')
        uuid = get_md5(line[3])
        if uuid not in skill_uuids:
            fh.write(uuid + '\t' + line[3] + '\t' + line[4] + '\n')
            skill_uuids.append(uuid)
        
        fh2.write(uuid + '\t' + line[1] + '\n')
    fh.close()
    fh2.close()

def stage_3_processing(filepath):
    """ Perform further refinement on datasets.
    
    Args:
        filepath(str, required):The path to the stage 2 processing directory.

    """
    files = os.listdir(filepath)

    for file in files:
        print file

if __name__ == '__main__':
    if len(sys.argv) > 2:
        if sys.argv[1] == '--stage-2' and os.path.isfile(sys.argv[2]):
            process_file(sys.argv[2])
        elif sys.argv[1] == '--stage-3' and os.path.isdir(sys.argv[2]):
            stage_3_processing(sys.argv[2])
