#!/bin/sh

# ---------------------------------------------------------------------------
# upgrade_pip - Utility for upgrading the Python pip package manager. 
#
# Usage: ./upgrade_pip.sh
# ---------------------------------------------------------------------------

pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
