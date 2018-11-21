#!/bin/bash
# Sample script:
# Change paths below to where you keep and run these scripts ('~' is shorthand for HOME-folder), 
# and change input arguments as needed.

# Run with "-h" for help on input arguments:
# /usr/local/bin/python3 ~/Bear-Markdown-Export/bear_export_sync.py -h

# To make this shell script executable, run following commands in Terminal (without the leading '# ' comment tag): 
# cd ~/Bear-Markdown-Export
# chmod 755 bear_export_sync.sh

# NOTE: Mulitiple tags in '-t=' or '-x=' aruments are entered as one CSV string (Comma Separated Values).
# NOTE: Enclose entire argument in "" if any spaces in path or tags. (See example below)
/usr/local/bin/python3 ~/Bear-Markdown-Export/bear_export_sync.py -o=OneDrive "-t=writings,travel info,.drafts,health issues"
/usr/local/bin/python3 ~/Bear-Markdown-Export/bear_export_sync.py --out_path=Box -x=private,secret,.shortcuts
# '-o' or '--out_path' defaults is 'Dropbox', and then no argument needed.

# Example with last run status written to a log-file:
# [ -d ~/BearProc ] || mkdir ~/BearProc
# /usr/local/bin/python3 ~/Bear-Markdown-Export/bear_export_sync.py -o=OneDrive -t=writings > ~/BearProc/LaunchD_log1.txt
# /usr/local/bin/python3 ~/Bear-Markdown-Export/bear_export_sync.py -o=Box -x=private >> ~/BearProc/LaunchD_log1.txt

# Run this script manually or add to cron job for automatic syncing (every 5 – 30 minutes, or whatever you prefer)  
# I recommend LaunchD Task Scheduler:
# https://itunes.apple.com/us/app/launchd-task-scheduler/id620249105?mt=12
# Is easy to configure and works very well for this.