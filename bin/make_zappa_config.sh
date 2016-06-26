#!/bin/sh

# -----------------------------------------------------------------------------
# make_zappa_config.sh - Create a Zappa configuration file for the application.
#
# Usage: ./make_zappa_config.sh [--development | --testing | --production]
# -----------------------------------------------------------------------------

SCRIPT_NAME=`basename "$0"`
CURRENT_DIR=`pwd`

if [ -f $SCRIPT_NAME ]; then
    SOURCE_DIR=..
else
    SOURCE_DIR=.
fi

CONFIG_DIR=$SOURCE_DIR
CONFIG_MODE=$1
ZAPPA_FILE=$CONFIG_DIR/zappa_settings.json

# Default Zappa configs
ZAPPA_AWS_REGION=1
ZAPPA_CACHE_CLUSTER_ENABLED=2
ZAPPA_CACHE_CLUSTER_SIZE=3
ZAPPA_DEBUG=4
ZAPPA_DELETE_ZIP=5
ZAPPA_DOMAIN=6
ZAPPA_EVENTS=7
ZAPPA_EXCLUDE=8
ZAPPA_HTTP_METHODS=9
ZAPPA_INTEGRATION_RESPONSE_CODES=10
ZAPPA_KEEP_WARM=11
ZAPPA_LOG_LEVEL=12
ZAPPA_MEMORY_SIZE=13
ZAPPA_METHOD_RESPONSE_CODES=14
ZAPPA_PARAMETER_DEPTH=15
ZAPPA_PREBUILD_SCRIPT=16
ZAPPA_PROFILE_NAME=17
ZAPPA_PROJECT_NAME=18
ZAPPA_ROLE_NAME=19
ZAPPA_S3_BUCKET=20
ZAPPA_SETTINGS_FILE=21
ZAPPA_TIMEOUT_SECONDS=22
ZAPPA_TOUCH=23
ZAPPA_USE_PRECOMPILED_PACKAGES=24
ZAPPA_VPC_CONFIG=25

function read_param {
    read -p "${1} [${2}] => " new_value
    if [ -z $new_value ]; then
        echo $2
    else
        echo $new_value
    fi
}


function get_config_params {
    ZAPPA_AWS_REGION=`read_param "aws_region" $ZAPPA_AWS_REGION`
    ZAPPA_CACHE_CLUSTER_ENABLED=`read_param "cache_cluster_enabled" $ZAPPA_CACHE_CLUSTER_ENABLED`
    ZAPPA_CACHE_CLUSTER_SIZE=`read_param "cache_cluster_size" $ZAPPA_CACHE_CLUSTER_SIZE`
    ZAPPA_DEBUG=`read_param "debug" $ZAPPA_DEBUG`
    ZAPPA_DELETE_ZIP=`read_param "delete_zip" $ZAPPA_DELETE_ZIP`
    ZAPPA_DOMAIN=`read_param "domain" $ZAPPA_DOMAIN`
    ZAPPA_EVENTS=`read_param "events" $ZAPPA_EVENTS`
    ZAPPA_EXCLUDE=`read_param "exclude" $ZAPPA_EXCLUDE`
    ZAPPA_HTTP_METHODS=`read_param "http_methofs" $ZAPPA_HTTP_METHODS`
    ZAPPA_INTEGRATION_RESPONSE_CODES=`read_param "integration_response_codes" $ZAPPA_INTEGRATION_RESPONSE_CODES`
    ZAPPA_KEEP_WARM=`read_param "keep_warm" $ZAPPA_KEEP_WARM`
    ZAPPA_LOG_LEVEL=`read_param "log_level" $ZAPPA_LOG_LEVEL`
    ZAPPA_MEMORY_SIZE=`read_param "memory_size" $ZAPPA_MEMORY_SIZE`
    ZAPPA_METHOD_RESPONSE_CODES=`read_param "method_response_codes" $ZAPPA_METHOD_RESPONSE_CODES`
    ZAPPA_PARAMETER_DEPTH=`read_param "parameter_depth" $ZAPPA_PARAMETER_DEPTH`
    ZAPPA_PREBUILD_SCRIPT=`read_param "prebuild_script" $ZAPPA_PREBUILD_SCRIPT`
    ZAPPA_PROFILE_NAME=`read_param "profile_name" $ZAPPA_PROFILE_NAME`
    ZAPPA_PROJECT_NAME=`read_param "project_name" $ZAPPA_PROJECT_NAME`
    ZAPPA_ROLE_NAME=`read_param "role_name" $ZAPPA_ROLE_NAME`
    ZAPPA_S3_BUCKET=`read_param "s3_bucket" $ZAPPA_S3_BUCKET`
    ZAPPA_SETTINGS_FILE=`read_param "settings_file" $ZAPPA_SETTINGS_FILE`
    ZAPPA_TIMEOUT_SECONDS=`read_param "timeout_seconds" $ZAPPA_TIMEOUT_SECONDS`
    ZAPPA_TOUCH=`read_param "touch" $ZAPPA_TOUCH`
    ZAPPA_USE_PRECOMPILED_PACKAGES=`read_param "use_precompiled_packages" $ZAPPA_USE_PRECOMPILED_PACKAGES`
    ZAPPA_VPC_CONFIG=`read_param "vpc_config" $ZAPPA_VPC_CONFIG`    
}

if [ -z $CONFIG_MODE ]; then
    echo "Error. Please specify a configuration mode (--development, --testing, --production)"
    
exit 1
fi

# Purge the old Zappa settings file
if [ -f $ZAPPA_FILE ]; then
    rm -f $ZAPPA_FILE
fi

case $CONFIG_MODE in
    --development )
        ZAPPA_MODE="development"
        get_config_params
        ;;
    --testing )
        ZAPPA_MODE="testing"
        get_config_params
        ;;
    --production ) 
        ZAPPA_MODE="production"
        get_config_params
        ;;
    * ) echo "Invalid configuration mode (${CONFIG_MODE}), select one of: --development, --testing, --production"
        exit 1
        ;;
esac

# Build the config module
cat <<EOF >> $ZAPPA_FILE
{
    "${ZAPPA_MODE}": {
            "aws_region": "${ZAPPA_AWS_REGION}",
            "cache_cluster_enabled": ${ZAPPA_CACHE_CLUSTER_ENABLED},
            "cache_cluster_size": ${ZAPPA_CACHE_CLUSTER_SIZE},
            "debug": ${ZAPPA_DEBUG},
            "delete_zip": ${ZAPPA_DELETE_ZIP},
            "domain": "${ZAPPA_DOMAIN}",
            "events": [${ZAPPA_EVENTS}],
            "exclude": ["${ZAPPA_EXCLUDE}"],
            "http_methods": [${ZAPPA_HTTP_METHODS}],
            "integration_response_codes": [${ZAPPA_INTEGRATION_RESPONSE_CODES}],
            "keep_warm": ${ZAPPA_KEEP_WARM},
            "log_level": "${ZAPPA_LOG_LEVEL}",
            "memory_size": $ZAPPA_MEMORY_SIZE,
            "method_response_codes": [$ZAPPA_METHOD_RESPONSE_CODES],
            "parameter_depth": $ZAPPA_PARAMETER_DEPTH,
            "prebuild_script": "$ZAPPA_PREBUILD_SCRIPT",
            "profile_name": "$ZAPPA_PROFILE_NAME",
            "project_name": "$ZAPPA_PROJECT_NAME",
            "role_name": "$ZAPPA_ROLE_NAME",
            "s3_bucket": "$ZAPPA_S3_BUCKET",
            "settings_file": "$ZAPPA_SETTINGS_FILE",
            "timeout_seconds": $ZAPPA_TIMEOUT_SECONDS,
            "touch": $ZAPPA_TOUCH,
            "use_precompiled_packages": $ZAPPA_USE_PRECOMPILED_PACKAGES,
            "vpc_config": {
                $ZAPPA_VPC_CONFIG
            }
    }
}
EOF

# All done, return to the home directory.
cd $CURRENT_DIR
echo "Application configuration completed. WARNING: Please DO NOT add the Zappa settings file to the code repo as it may expose credentials!"
exit 0
