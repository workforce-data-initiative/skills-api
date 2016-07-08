# ----------------------------------------------------------------------------
# clean - General purpose cleanup utility for removing development crud.
#
# Usage: ./clean.sh
# ----------------------------------------------------------------------------

SCRIPT_NAME=`basename "$0"`
HERE=`pwd`

if [ -f $SCRIPT_NAME ]; then 
    cd ..
fi

echo -ne "Cleaning Work Directories........."
find . -name "*.pyc" -exec rm -rf {} \;
cd $HERE
echo "Done"
