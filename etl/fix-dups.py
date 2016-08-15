# -*- coding: utf-8 -*-

import os
import sys
import hashlib
import uuid

COUNT    = 0
SOC_CODE = 1
ONET_CAT = 2
NAME     = 3
UUID     = 4
NLP_A    = 5

if __name__ == '__main__':
    infile = os.path.join('tmp', 'skills_master_table.tsv')
    outfile = os.path.join('tmp', 'skills_master_unique_table.tsv')
    content = None
    count = 0
    dups = 0
    add = 0
    dots = 0
    seen_sigs = []
    with open(infile, 'r') as in_file:
        if len(sys.argv) > 1:
            resume_point = int(sys.argv[1])
        else:
            resume_point = None

        if resume_point is not None:
            out_file = open(outfile, 'a+')
        else:
            out_file = open(outfile, 'w+')

        while content != '':
            content = in_file.readline()
            content_explore = content.strip().split('\t')
            count += 1
            
            if resume_point is not None:
                try:
                    current_line = int(content_explore[COUNT])
                except:
                    current_line = -1
                if current_line < resume_point:
                    print 'Skipping line ' +  content_explore[COUNT]
                    #sys.stdout.write( ' - ')
                    sys.stdout.flush()
                    signature = content_explore[SOC_CODE].strip() + content_explore[NAME].strip()
                    if signature not in seen_sigs:
                        seen_sigs.append(signature)
                    process_line = False
                else:
                    process_line = True
            else:
                process_line = True
            
            if process_line:
                # get md5 sum
                try:
                    signature = content_explore[SOC_CODE].strip() + content_explore[NAME].strip()
                except:
                    print content

                if signature not in seen_sigs:
                    add += 1
                    seen_sigs.append(signature)
                    out_file.write(content)
                else:
                    dups += 1

                # proof of life
                if dots == 1000:
                    sys.stdout.write(' . ')
                    sys.stdout.flush()
                    dots = 0
                else:
                    dots += 1

        outfile.close()
 
    print '\n-------\nsummary\n-------'
    print ' total records           ' + str(count)
    print ' total unique records    ' + str(add)
    print ' total duplicate records ' + str(dups)
    print ' duplicate + unique      ' + str(add + dups)
