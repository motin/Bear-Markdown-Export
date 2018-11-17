#!/bin/bash
# Sample script:
# Change paths below to where you want to keep and run these scripts ('~' is shorthand for HOME-folder), 
# and change input arguments as needed.

# Run with "-h" for help on input arguments:
# /usr/local/bin/python3 ~/Bear-Markdown-Export/bear_export_sync.py -h

# To make this shell script executable, run following commands in Terminal (without the leading '# '): 
# cd ~/Bear-Markdown-Export
# chmod 755 bear_export_sync.sh

/usr/local/bin/python3 ~/Bear-Markdown-Export/bear_export_sync.py --out_path=Box -a -s -x=private,secret,.shortcuts
/usr/local/bin/python3 ~/Bear-Markdown-Export/bear_export_sync.py -o=OneDrive -a -s -t=writings,travel,.drafts
# '-o' or '--out_path' defaults is 'Dropbox' and then argument not needed.

# Or with run status to log-file. Exaple:
# /usr/local/bin/python3 ~/Bear-Markdown-Export/bear_export_sync.py -o "Dropbox" -a -s > ~/BearTemp/LaunchD_log1.txt
