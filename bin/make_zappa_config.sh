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
ZAPPA_AWS_REGION=us-east-1
ZAPPA_CACHE_CLUSTER_ENABLED=false
ZAPPA_CACHE_CLUSTER_SIZE=.5
ZAPPA_DEBUG=true
ZAPPA_DELETE_ZIP=true
ZAPPA_DOMAIN=
ZAPPA_EVENTS=
ZAPPA_EXCLUDE=(\"*.pem\", \"*.gz\", \"*.csv\", \"*.tsv\")
ZAPPA_HTTP_METHODS=(\"GET\", \"POST\", \"PUT\", \"DELETE\")
ZAPPA_INTEGRATION_RESPONSE_CODES=(200, 301, 404, 500)
ZAPPA_KEEP_WARM=true
ZAPPA_LOG_LEVEL=DEBUG
ZAPPA_MEMORY_SIZE=512
ZAPPA_METHOD_RESPONSE_CODES=(200, 301, 404, 500)
ZAPPA_PARAMETER_DEPTH=8
ZAPPA_PREBUILD_SCRIPT=
ZAPPA_PROFILE_NAME="default"
ZAPPA_PROJECT_NAME=
ZAPPA_ROLE_NAME=
ZAPPA_S3_BUCKET=
ZAPPA_SETTINGS_FILE=
ZAPPA_TIMEOUT_SECONDS=30
ZAPPA_TOUCH=true
ZAPPA_USE_PRECOMPILED_PACKAGES=true
ZAPPA_VPC_CONFIG=

# Purge the old Zappa settings file
if [ -f $ZAPPA_FILE ]; then
    rm -f $ZAPPA_FILE
fi

# Build the config module
cat <<EOF >> $ZAPPA_FILE
{
    "development": {
            "aws_region": "${ZAPPA_AWS_REGION}",
            "cache_cluster_enabled": ${ZAPPA_CACHE_CLUSTER_ENABLED},
            "cache_cluster_size": ${ZAPPA_CACHE_CLUSTER_SIZE},
            "debug": ${ZAPPA_DEBUG},
            "delete_zip": ${ZAPPA_DELETE_ZIP},
            "domain": "${ZAPPA_DOMAIN}",
            "events": [{
                ${ZAPPA_EVENTS}
            }],
            "exclude": [${ZAPPA_EXCLUDE[*]}],
            "http_methods": [${ZAPPA_HTTP_METHODS[*]}],
            "integration_response_codes": [${ZAPPA_INTEGRATION_RESPONSE_CODES[*]}],
            "keep_warm": ${ZAPPA_KEEP_WARM},
            "log_level": "${ZAPPA_LOG_LEVEL}",
            "memory_size": $ZAPPA_MEMORY_SIZE,
            "method_response_codes": [${ZAPPA_METHOD_RESPONSE_CODES[*]}],
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
                "SubnetIds": [],
                "SecurityGroupIds": []
            }
    },
    "testing": {
            "aws_region": "${ZAPPA_AWS_REGION}",
            "cache_cluster_enabled": ${ZAPPA_CACHE_CLUSTER_ENABLED},
            "cache_cluster_size": ${ZAPPA_CACHE_CLUSTER_SIZE},
            "debug": ${ZAPPA_DEBUG},
            "delete_zip": ${ZAPPA_DELETE_ZIP},
            "domain": "${ZAPPA_DOMAIN}",
            "events": [{
                ${ZAPPA_EVENTS}
            }],
            "exclude": [${ZAPPA_EXCLUDE[*]}],
            "http_methods": [${ZAPPA_HTTP_METHODS[*]}],
            "integration_response_codes": [${ZAPPA_INTEGRATION_RESPONSE_CODES[*]}],
            "keep_warm": ${ZAPPA_KEEP_WARM},
            "log_level": "${ZAPPA_LOG_LEVEL}",
            "memory_size": $ZAPPA_MEMORY_SIZE,
            "method_response_codes": [${ZAPPA_METHOD_RESPONSE_CODES[*]}],
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
                "SubnetIds": [],
                "SecurityGroupIds": []
            }
    },
    "production": {
            "aws_region": "${ZAPPA_AWS_REGION}",
            "cache_cluster_enabled": ${ZAPPA_CACHE_CLUSTER_ENABLED},
            "cache_cluster_size": ${ZAPPA_CACHE_CLUSTER_SIZE},
            "debug": ${ZAPPA_DEBUG},
            "delete_zip": ${ZAPPA_DELETE_ZIP},
            "domain": "${ZAPPA_DOMAIN}",
            "events": [{
                ${ZAPPA_EVENTS}
            }],
            "exclude": [${ZAPPA_EXCLUDE[*]}],
            "http_methods": [${ZAPPA_HTTP_METHODS[*]}],
            "integration_response_codes": [${ZAPPA_INTEGRATION_RESPONSE_CODES[*]}],
            "keep_warm": ${ZAPPA_KEEP_WARM},
            "log_level": "${ZAPPA_LOG_LEVEL}",
            "memory_size": $ZAPPA_MEMORY_SIZE,
            "method_response_codes": [${ZAPPA_METHOD_RESPONSE_CODES[*]}],
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
                "SubnetIds": [],
                "SecurityGroupIds": []
            }
    }
}
EOF

# All done, return to the home directory.
cd $CURRENT_DIR
echo "Application configuration completed. WARNING: Please DO NOT add the Zappa settings file to the code repo as it may expose credentials!"
exit 0
