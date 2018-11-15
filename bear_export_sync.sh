#!/bin/bash
/usr/local/bin/python3 ~/GitHub/Bear-Markdown-Export/bear_export_sync.py -o "Dropbox" -a -s -x private,secret,.shortcuts
/usr/local/bin/python3 ~/GitHub/Bear-Markdown-Export/bear_export_sync.py -o "OneDrive" -a -s -t writings,travel,.drafts

# Or with run status to log-file:
# /usr/local/bin/python3 ~/Scripts/python/Bear-Markdown-Export/bear_export_sync.py -o "Dropbox" -a -s > ~/BearTemp/LaunchD_log1.txt
