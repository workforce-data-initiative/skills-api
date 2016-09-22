#!/bin/sh

# ----------------------------------------------------------------------------
# etl - Extract, Transform, Load handler for data produced by Machine Learning
#		pipeline.
#
# Usage: ./etl.sh
# ----------------------------------------------------------------------------

ETL_APP=`pwd`/etl.py
TMP_DIR=`pwd`/etl
STAGE_1=$TMP_DIR/stage_1
STAGE_2=$TMP_DIR/stage_2
STAGE_3=$TMP_DIR/stage_3
STAGE_4=$TMP_DIR/stage_4

S3_PATHS=(  "skills-public/machine_learning/table/job2skill_column_skill_index.tsv"
            "skills-public/machine_learning/table/job_titles_master_table.tsv"
            "skills-public/machine_learning/table/skills_master_table.tsv"
            "skills-public/tables/skills_master.csv"
            "skills-public/bucket/ksas_importances.csv"
            "skills-public/tables/interesting_job_titles.csv" )

# Ensure that the working directory is created
if [ ! -d $STAGE_1 ]; then
    mkdir -p $STAGE_1
fi


# Stage 1: Download Data Files from AWS S3 Buckets
echo -ne "Stage 1 - Downlading Data Files From AWS S3 Buckets................."
for path in ${S3_PATHS[@]}; do
    echo ""
    aws s3 cp s3://$path $STAGE_1/.
done
echo "Done"


# Stage 2: Consolidate Files from ML Pipeline
echo -ne "Stage 2 - Consolidating Files From ML Pipeline......................"
if [ ! -d $STAGE_2 ]; then
    mkdir -p $STAGE_2
fi

DATA_FILES=`ls -1 $STAGE_1`
for data_file in $DATA_FILES; do
    python $ETL_APP --stage-2 $STAGE_1/$data_file
done
echo "Done"

# Stage 3: Refine files from ML Pipeline
echo -ne "Stage 3 - Refining Stage 2 Products................................."
if [ ! -d $STAGE_3 ]; then
    mkdir -p $STAGE_3
fi

python $ETL_APP --stage-3 $STAGE_2 $STAGE_3
echo "Done"
