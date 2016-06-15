#!/bin/sh

# -----------------------------------------------------------------------------
# make_config.sh - Create a configuration file for application.
# -----------------------------------------------------------------------------

SCRIPT_NAME=`basename "$0"`
CURRENT_DIR=`pwd`

if [ -f $SCRIPT_NAME ]; then
    SOURCE_DIR=..
else
    SOURCE_DIR=.
fi

CONFIG_DIR=$SOURCE_DIR/config

if [ -d $CONFIG_DIR ]; then
    rm -Rf $CONFIG_DIR
fi

mkdir $CONFIG_DIR
cd $CONFIG_DIR
touch __init__.py

cd $CURRENT_DIR
