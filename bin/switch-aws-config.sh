#!/bin/sh

# ---------------------------------------------------------------------------
# switch-aws-config - Because sometimes you just get tired of changing your 
# AWS configs manually...
#
# Usage: ./switch-aws-config.sh [ --development | --testing | --production ] 
# ---------------------------------------------------------------------------

AWS_CONFIG_HOME=$HOME/.aws/

if [ -d $AWS_CONFIG_HOME ]; then
    HERE=`pwd`
    if [ ! -z $1 ]; then
        if [ $1 == "--development" ]; then
            echo "Switched to Development AWS Credentials"
            CONFIG_TYPE="development"
        elif [ $1 == "--testing" ]; then
            echo "Switched to Testing AWS Credentials"
            CONFIG_TYPE="testing"
        elif [ $1 == "--production" ]; then
            echo "Switched to Production AWS Credentials"
            CONFIG_TYPE="production"
        else
            echo "Invalid Configuration ${1}"
            exit 1
        fi
    else
        echo "No Configuration Specified"
        exit 1
    fi
    cd $AWS_CONFIG_HOME
    cp credentials.$CONFIG_TYPE credentials
    cp config.$CONFIG_TYPE config
fi
