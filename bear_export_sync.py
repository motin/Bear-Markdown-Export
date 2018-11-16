# encoding=utf-8
# python3.6
# bear_export_sync.py

version = '''
bear_export_sync.py - markdown export from Bear sqlite database 
Version 1.6.2, 2018-11-16 at 19:24 IST - github/rovest, rorves@twitter
** Please discard versions 1.5.x **
Developed on an MBP with Visual Studio Code with MS Python extension.
Tested with python 3.6 and Bear 1.6.3 on MacOS 10.14'''

help_text = '''
*** If no arguments, this help is displayed. (Use '-d' for internal defaults only)
    all arguments separated by one space! (No joining like: -rma allowed)
    -h  display this Help text.
    -v  Version info displayed.
    -d  run with Default settings (as in earlier versions), use no other arguments.
    -o  export Out path as next argument! Examples:
        -o MyExports (if no leading '/' it will be placed on HOME-folder)
        -o "/users/Guest" (make sure you have permission if not on HOME)
        -o ~  (tilde only = 'BearNotes' folder directly on HOME root)
        enclose in " " if spaces in path! (Default: '~/Dropbox/BearNotes')
        PS. 'BearNotes' will always be added to path for security reasons!  
    -t  Tags to be exported, as comma separated list of tags in next argument:
            -t mytag,travelinfo,memos,writings
            enclose list in " " if any spaces: 
            -t "My Essay/in edit,Travel Info,memos/my medical"
    -x  tags to be eXcluded as comma separated list in next argument:
            -x health,private,secret
            use either -e or -t, not both!
    -r  force Run - runs even if no changes in db since last run.
    -p  export as regular markdown files, but with links to images and files 
        that are copied to a rePository (not textbundles) in two folders: 
        'BearAssetsImages' and 'BearAssetsFiles' on the root of export_path.
    -R  export all notes in Raw format as Bear does, no changes to md formatting,
        use with -b to export as plain markdown without images or files.

*** The following functions are ON by default, use these swithces to turn them OFF:
    -s  do not Sync changes back to Bear - export only.
    -u  do not use _Untagged folder: put untagged notes flat on root.
    -f  do not make tag Folders: all notes flat on root.
    -m  do not export same note to Multiple tag folders: only use first tag in note.
    -c  do not hide tags in html Comments: `<!-- #mytag -->`, but just plain `#mytag`
    -a  do not include Archived notes (under '_Archived' sub folder)
    -i  do not Include file attachments.
    -b  du not export as textBundles: all notes as regular markdown, no images or files.
    -y  do not export as hYbrid: all notes will be exported as textbundles even if no images.
    -l  do not write to Log-file.
    -w  export Without tags: All tags are stripped from text.
'''

'''
=================================================================================================
Updated 2018-11-15
    - Cleaning up code
    - Bug fixes
    - Added argument: '-l' do not write to Log-file.
    - Added function and argument: '-w' export Without tags: All tags are stripped from text.

Updated 2018-11-14 
    - Added command line arguments: -R for 'RAW' markdown export, and -s for no Sync.
    - Included some other improvements from pull requests.

Updated 2018-11-13 
    - Added command line argument help and switches.

Updated 2018-11-12 
    - Added export of file attachments (when 'export_as_textbundles = True')
    - All untagged notes are now exported to '_Untagged' folder if 'make_tag_folders = True'
    - Added choice for exporting with or without archived notes, or only archived.
    - Fixed escaping of spaces for sync import back to Bear.
    - Fixed multiple copying if same tag is repeated in same note. Case sensitive though!

Updated 2018-10-30 
    - Uses newer rsync from Carbon Copy Cloner (if present) to preserve file-creation-time.  
    - Fixed escaping of spaces in image names from iPhone camera taken directly in Bear.

Updated 2018-10-17 with new Bear path: 'Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data'

See also: bear_import.py for auto import to bear script.

## Sync external updates:
First checks for changes in external Markdown files (previously exported from Bear)
* Replacing text in original note with callback-url `/add-text&mode=replace_all` command   
  (Keeping original creation date)
  Now using the new mode: `replace_all` to include title.
* New notes are added to Bear (with x-callback-url command)
* New notes get tags from sub folder names, or `#.inbox` if root
* Backing up original note as file to BearSyncBackup folder  
  (unless a sync conflict, then both notes will be there)

## Export:
Then exporting Markdown from Bear sqlite db.
* check_if_modified() on database.sqlite to see if export is needed
* Uses rsync for copying, so only markdown files of changed sheets will be updated  
  and synced by Dropbox (or other sync services)
* "Hides" tags with `period+space` on beginning of line: `. #tag` not appear as H1 in other apps.   
  (This is removed if sync-back above)
* Or instead hide tags in HTML comment blocks like: `<!-- #mytag -->` if `hide_tags_in_comment_block = True`
* Makes subfolders named with first tag in note if `make_tag_folders = True`
* Files can now be copied to multiple tag-folders if `multi_tags = True`
* Export can now be restricted to a list of spesific tags: `limit_export_to_tags = ['bear/github', 'writings']`  
or leave list empty for all notes: `limit_export_to_tags = []`
* Can export and link to images in common image repository
* Or export as textbundles with images included 
'''

make_tag_folders = True  # Exports to folders using first tag only, if `multi_tag_folders = False`
untagged_folder_name = '_Untagged'  # Only works if 'make_tag_folders = True'
                                    # If empty: untagged notes are exported to root-folder.
multi_tag_folders = True  # Copies notes to all 'tag-paths' found in note!
                          # Only active if `make_tag_folders = True`
hide_tags_in_comment_block = True  # Hide tags in HTML comments: `<!-- #mytag -->`
export_without_tags = False
do_not_log = False

# The following two lists are more or less mutually exclusive, so use only one of them.
# (You can use both if you have some nested tags where that makes sense)
# Also, they only work if `make_tag_folders = True`.
only_export_these_tags = []  # Leave this list empty for all notes! See below for sample
# only_export_these_tags = ['bear/github', 'writings'] 
no_export_tags = []  # If a tag in note matches one in this list, it will not be exported.
# no_export_tags = ['private', '.inbox', 'love letters', 'banking']

include_archived = True  # Archived included under '_Archived' sub folder (only works if 'only_archived = False')
only_archived = False  # Exports only archived notes

export_as_textbundles = True  # Exports as Textbundles with images included
export_as_hybrids = True  # Exports as .textbundle only if images included, otherwise as .md
                          # Only used if `export_as_textbundles = True`
export_raw = False        # export all notes in Raw format as Bear does, no changes to md formatting.
export_with_files = True  # Only used if `export_as_textbundles = True`
                          # Sync/Import back to Bear will loose any externally added file attachments,
                          # as they are not part of textbundle spec.
export_image_repository = False  # Export all notes as md but link images to 
                                 # a common repository exported to: `assets_images_path` 
                                 # Only used if `export_as_textbundles = False`
do_sync_back_to_bear = True  # Syncs any changes in exported files back to Bear
force_run = False
set_logging_on = True

my_sync_service = 'Dropbox'  # Change 'Dropbox' to 'Box', 'Onedrive' or whatever folder of sync service you want.

# NOTE! Do not change anything below here!!!

import sqlite3
import datetime
import re
import subprocess
import urllib.parse
import time
import shutil
import fnmatch
import json
import sys
import os

HOME = os.getenv('HOME', '')
# NOTE! if 'BearNotes' is left blank, all other files in my_sync_service will be deleted!! 
export_path = os.path.join(HOME, my_sync_service, 'BearNotes')
# NOTE! "export_path" is used for sync-back to Bear, so don't change this variable name!

bear_db = os.path.join(HOME, 'Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite')
temp_path = os.path.join(HOME, 'BearTemp', 'BearExportTemp')  # NOTE! Do not change the "BearExportTemp" folder name!!!
sync_backup = os.path.join(HOME, 'BearTemp', 'BearSyncBackup') # Backup of original note before sync to Bear.
log_file = os.path.join(sync_backup, 'bear_export_sync_log.txt')

# Paths used in image exports:
bear_image_path = os.path.join(HOME, 
         'Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/Local Files/Note Images')
bear_file_path = os.path.join(HOME, 
         'Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/Local Files/Note Files')
assets_images_path = '' 
assets_files_path = ''

sync_ts = '.sync-time.log'
export_ts = '.export-time.log'

sync_ts_file = os.path.join(export_path, sync_ts)
export_ts_file_exp = os.path.join(export_path, export_ts)
sync_ts_file_temp = os.path.join(temp_path, sync_ts)
export_ts_file = os.path.join(temp_path, export_ts)

gettag_sh = os.path.join(HOME, 'temp/gettag.sh')
gettag_txt = os.path.join(HOME, 'temp/gettag.txt')

# If present, use newer rsync v. 3.0.6 from Carbon Copy Cloner:
rsync_path = '/Library/Application Support/com.bombich.ccc/Frameworks/CloneKit.framework/Versions/A/rsync'
if os.path.exists(rsync_path):
    # with --crtimes to preserve file-creation-time
    crswitch = '--crtimes' 
else:
    rsync_path = 'rsync'
    crswitch = ''
    

def main():
    if not check_sysargs():
        return
    if export_image_repository:
        global assets_images_path, assets_files_path
        assets_images_path = os.path.join(export_path, 'BearAssetsImages')
        assets_files_path = os.path.join(export_path, 'BearAssetsFiles')
    init_gettag_script()
    if do_sync_back_to_bear:
        sync_md_updates()
    if check_db_modified() or force_run:
        delete_old_temp_files()
        note_count = export_markdown()
        write_time_stamp()
        rsync_files_from_temp(export_path, True)
        if export_image_repository and not export_as_textbundles:
            copy_bear_images_and_files()
        # notify('Export completed')
        write_log(str(note_count) + ' notes exported to: ' + export_path)
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
        print(time_stamp + ' - ' + str(note_count) + ' notes exported to: ' + export_path)        
    else:
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
        print(time_stamp, '*** No export needed: nothing modified in Bear since last export')


def check_sysargs():
    global force_run, make_tag_folders, multi_tag_folders, hide_tags_in_comment_block
    global include_archived, export_as_textbundles, export_as_hybrids, do_sync_back_to_bear
    global export_with_files, export_image_repository, export_without_tags
    global export_path, sync_ts_file, export_ts_file_exp, untagged_folder_name
    global only_export_these_tags, no_export_tags, export_raw, do_not_log
    arg_count = len(sys.argv) - 1
    if arg_count == 0:
        # No arguments supplied: display help:
        print(version)
        print(help_text)
        return False
    i = 0
    get_path = False
    path_ok = True
    include_tags = False
    exclude_tags = False
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
    print(time_stamp, sys.argv)
    for arg in sys.argv:
        if i == 0:
            i += 1
            continue
        if arg == '-d':
            if arg_count == 1:
                print('*** Running with default internal settings ...')
                return True
        elif arg == '-h':
            print(version)
            print(help_text)
            return False
        elif arg == '-v':
            print(version)
            return False
        elif get_path:
            if arg.startswith('/'):
                export_path = os.path.join(arg, 'BearNotes')
            elif arg.startswith('~/'):
                export_path = os.path.join(HOME, arg.replace('~/', ''), 'BearNotes')
            elif arg == '~':
                # 'BearNotes' folder directly on HOME root.
                export_path = os.path.join(HOME, 'BearNotes')
            elif arg.startswith('-') and len(arg) < 3:
                # If user accidentally supplied another CLI switch after '-o' instead of 'path name'
                print('\n*** Wrong argument:', arg, err_msg1)
                return False
            else:
                export_path = os.path.join(HOME, arg, 'BearNotes')
            if HOME + '/BearTemp/' in export_path:
                print('\n*** This is a reserved folder name, do not use! :', arg + '\n')
                return False
            # NOTE! if 'BearNotes' was not added, all other files in export_path would be deleted!! 
            # So very dangerous if you accidentally used an exsisting path with other files and subfolders!
            sync_ts_file = os.path.join(export_path, sync_ts)
            export_ts_file_exp = os.path.join(export_path, export_ts)
            get_path = False
            path_ok = True
        elif arg == '-r':
            force_run = True
        elif arg == '-s':
            do_sync_back_to_bear = False
        elif arg == '-u':
            untagged_folder_name = ''
        elif arg == '-f':
            make_tag_folders = False
        elif arg == '-m':
            multi_tag_folders = False
        elif arg == '-c':
            hide_tags_in_comment_block = False
        elif arg == '-a':
            include_archived = False
        elif arg == '-b':
            export_as_textbundles = False
        elif arg == '-y':
            export_as_hybrids = False
        elif arg == '-R':
            export_raw = True            
        elif arg == '-i':
            export_with_files = False
        elif arg == '-p':
            export_image_repository = True
            export_as_textbundles = False
        elif arg == '-o':
            get_path = True
        elif arg == '-t':
            include_tags = True
        elif arg == '-x':
            exclude_tags = True
        elif arg == '-w':
            export_without_tags = True       
        elif arg == '-l':
            do_not_log = True       
        elif include_tags:
            if arg[0] in '-~/':
                print(arg, err_msg2)
                return False
            only_export_these_tags = arg.split(',')
            include_tags = False
        elif exclude_tags:
            if arg[0] in '-~/':
                print(arg, err_msg2)
                return False
            no_export_tags = arg.split(',')
            exclude_tags = False
        else:
            print('\n*** Unknown argument! Use with -h for help!\n***')
            return False
        i += 1
    if get_path:
        print('\n*** Path name missing!', err_msg1)
        return False
    if include_tags or exclude_tags:
        print('\n*** Tag-list missing!', err_msg2)
        return False
    if path_ok:
        if not os.path.exists(export_path):
            os.makedirs(export_path)
    return True

err_msg1 = '''
*** Error in the path name following the '-o' argument!
        Use at least a 2 char string for path name and not starting with a '-'
        Examples: 

    -o OneDrive
    -o "/users/Guest/My Exports"
    -o ~ ('BearNotes' folder directly on HOME root)

        'BearNotes' will always be added to path for security reasons.
        Enclose in " " if spaces in path and without leading '/' if on Home-folder
'''

err_msg2 = '''
*** Error in tag list argument:
    -t or -e    
        Supply tab separated list of tags as next argument!
        Examples:
        "My Essay/in edit,Travel Info,memos/medical"
        health,private,secret
'''


def write_log(message):
    if do_not_log:
        return
    if set_logging_on == True:
        if not os.path.exists(sync_backup):
            os.makedirs(sync_backup)
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
        message = message.replace(export_path + '/', '')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(time_stamp + ': ' + message + '\n')


def check_db_modified():
    if not os.path.exists(sync_ts_file):
        return True
    db_ts = get_file_date(bear_db)
    last_export_ts = get_file_date(export_ts_file_exp)
    return db_ts > last_export_ts


def export_markdown():
    with sqlite3.connect(bear_db) as conn:
        conn.row_factory = sqlite3.Row
        if only_archived:
            query = "SELECT * FROM `ZSFNOTE` WHERE `ZTRASHED` LIKE '0' AND `ZARCHIVED` LIKE '1'"
        elif include_archived:
            # Both normal and archived notes
            query = "SELECT * FROM `ZSFNOTE` WHERE `ZTRASHED` LIKE '0'"
        else:
            query = "SELECT * FROM `ZSFNOTE` WHERE `ZTRASHED` LIKE '0' AND `ZARCHIVED` LIKE '0'"
        c = conn.execute(query)
    note_count = 0
    for row in c:
        title = row['ZTITLE']
        md_text = row['ZTEXT'].rstrip()
        creation_date = row['ZCREATIONDATE']
        modified = row['ZMODIFICATIONDATE']
        uuid = row['ZUNIQUEIDENTIFIER']
        archived = row['ZARCHIVED']
        filename = clean_title(title) + date_time_conv(creation_date)
        file_list = []
        if archived == 1:
            out_path = os.path.join(temp_path, '_Archived')
            # If you want a fixed local path for Archive export, un-comment line below:
            # out_path = os.path.join(HOME, 'BearArchive')  # NOTE! Notes deleted from archive will not be deleted here!
        else:
            out_path = temp_path
        if make_tag_folders:
            file_list = sub_path_from_tag(out_path, filename, md_text)
        else:
            file_list.append(os.path.join(out_path, filename))
        if file_list:
            cre_dt = dt_conv(creation_date)
            mod_dt = dt_conv(modified)
            if export_without_tags:
                md_text = strip_all_tags(md_text)
            if not export_raw:
                if not export_without_tags:
                    md_text = hide_tags(md_text)
                md_text += '\n\n<!-- {BearID:' + uuid + '} -->\n'
            for filepath in file_list:
                note_count += 1
                if export_as_textbundles:
                    if check_image_hybrid(md_text):
                        make_text_bundle(md_text, filepath, mod_dt, cre_dt)                        
                    else:
                        write_file(filepath + '.md', md_text, mod_dt, cre_dt)
                elif export_image_repository:
                    md_proc_text = process_image_and_file_links(md_text, filepath)
                    write_file(filepath + '.md', md_proc_text, mod_dt, cre_dt)
                else:
                    write_file(filepath + '.md', md_text, mod_dt, cre_dt)
    return note_count


def check_image_hybrid(md_text):
    # Hybrid export: textbundle if note contains images or files, otherwise regular markdown file. 
    if export_as_hybrids:
        if re.search(r'\[image:(.+?)\]', md_text):
            return True
        elif export_with_files and re.search(r'\[file:(.+?)\]', md_text):
            return True
        else:
            return False
    else:
        return True


def make_text_bundle(md_text, filepath, mod_dt, cre_dt):
    '''
    Exports as Textbundles with images included 
    '''
    bundle_path = filepath + '.textbundle'
    assets = os.path.join(bundle_path, 'assets')    
    if not os.path.exists(bundle_path):
        os.makedirs(bundle_path)
        os.makedirs(assets)
        
    info = '''{
    "transient" : true,
    "type" : "net.daringfireball.markdown",
    "creatorIdentifier" : "net.shinyfrog.bear",
    "version" : 2
    }'''

    matches = re.findall(r'\[image:(.+?)\]', md_text)
    for image in matches:
        new_name = image.replace('/', '_')
        source = os.path.join(bear_image_path, image)
        target = os.path.join(assets, new_name)
        try:
            shutil.copy2(source, target)
            # Escape spaces in dates on images (taken with iPhone camera direct in Bear):
            if ' ' in image:
                md_text = md_text.replace('[image:' + image, '[image:' + image.replace(' ', '%20'))
        except:
            print("File missing:", source)
    if matches:
        md_text = re.sub(r'\[image:(.+?)/(.+?)\]', r'![](assets/\1_\2)', md_text)

    if export_with_files:
        md_text = include_files(md_text, assets)
    write_file(bundle_path + '/text.md', md_text, mod_dt, cre_dt)
    write_file(bundle_path + '/info.json', info, mod_dt, cre_dt)
    os.utime(bundle_path, (-1, cre_dt))
    os.utime(bundle_path, (-1, mod_dt))


def include_files(md_text, assets):
    matches = re.findall(r'\[file:(.+?)\]', md_text)
    for file in matches:
        new_name = file.replace('/', '_')
        source = os.path.join(bear_file_path, file)
        target = os.path.join(assets, new_name)
        try:
            shutil.copy2(source, target)
        except:
            print("File missing:", source)
    if matches:
        md_text = re.sub(r'\[file:(.+?)/(.+?)\]', r'[File: \2](assets/\1_\2)', md_text)
        # Escape spaces in filename link:
        matches = re.findall(r'\[File: .+?\]\(assets/(.*?)\)', md_text)
        for file in matches:
            if ' ' in file:
                md_text = md_text.replace('(assets/' + file, '(assets/' + file.replace(' ', '%20'))
    return md_text


def strip_all_tags(md_text):
    # Removes all tags in note:
    pattern1 = r'(?<!\S)\#([^ \d][\w\/\-]+)[ \n]?(?!([\/ \w\-]+\w[#]))'
    pattern2 = r'(?<![\S])\#([^ \d][.\w\/ \-]+?)\#([ ]|$)'
    code_block = False
    new_lines = []
    for line in md_text.splitlines():
        if line[:2] in ['# ', '##']:
            new_lines.append(line)
            continue
        if line.startswith('```'):
            # Toggle code_block flag:
            code_block = code_block == False            
            new_lines.append(line)
        elif not code_block and '#' in line:
            stripped_line = re.sub(pattern1, '', line)
            stripped_line = re.sub(pattern2, '', stripped_line)
            if stripped_line.strip() != '':
                new_lines.append(stripped_line)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)


def sub_path_from_tag(temp_path, filename, md_text):
    # Get tags in note:
    pattern1 = r'(?<!\S)\#([^ \d][\w\/\-]+)[ \n]?(?!([\/ \w\-]+\w[#]))'
    pattern2 = r'(?<![\S])\#([^ \d][.\w\/ \-]+?)\#([ \n]|$)'
    if multi_tag_folders:
        # Files copied to all tag-folders found in note
        tags = []
        for matches in re.findall(pattern1, md_text):
            tag = matches[0]
            if tag not in tags:
                tags.append(tag)
        for matches2 in re.findall(pattern2, md_text):
            tag2 = matches2[0]
            if tag2 not in tags:
                tags.append(tag2)
        if len(tags) == 0:
            # No tags found
            if only_export_these_tags:
                return []
            if untagged_folder_name == '':
                # copy to root level only
                return [os.path.join(temp_path, filename)]
            else:
                tag = untagged_folder_name
                tags = [tag]
    else:
        # Only folder for first tag
        match1 =  re.search(pattern1, md_text)
        match2 =  re.search(pattern2, md_text)
        if match1 and match2:
            if match1.start(1) < match2.start(1):
                tag = match1.group(1)
            else:
                tag = match2.group(1)
        elif match1:
            tag = match1.group(1)
        elif match2:
            tag = match2.group(1)
        elif only_export_these_tags:
            return []
        else:
            # No tags found
            if untagged_folder_name == '':
                # copy to root level only
                return [os.path.join(temp_path, filename)]
            else:
                tag = untagged_folder_name
        tags = [tag]
 
    paths = []
    for tag in tags:
        if tag == '/':
            continue
        if only_export_these_tags:
            export = False
            for export_tag in only_export_these_tags:
                if tag.lower().startswith(export_tag.lower()):
                    export = True
                    break
            if not export:
                continue
        for no_tag in no_export_tags:
            if tag.lower().startswith(no_tag.lower()):
                return []
        if tag.startswith('.'):
            # Avoid hidden path if it starts with a '.'
            sub_path = '_' + tag[1:]     
        else:
            sub_path = tag    
        tag_path = os.path.join(temp_path, sub_path)
        if not os.path.exists(tag_path):
            os.makedirs(tag_path)
        paths.append(os.path.join(tag_path, filename))      
    return paths


def process_image_and_file_links(md_text, filepath):
    '''
    Bear image links converted to MD image links and files to MD url links
    For image and file repositories only
    '''
    root = filepath.replace(temp_path, '')
    level = len(root.split('/')) - 2
    parent = '../' * level

    md_text = re.sub(r'\[image:(.+?)\]', r'![](' + parent + r'BearAssetsImages/\1)', md_text)
    matches = re.findall(r'!\[\]\((\.\./)*BearAssetsImages/(.*?)\)', md_text)
    for groups in matches:
        file = groups[1]
        if ' ' in file:
            md_text = md_text.replace('BearAssetsImages/' + file + ')', 'BearAssetsImages/' + file.replace(' ', '%20') + ')')

    if export_with_files:
        md_text = re.sub(r'\[file:(.+?)/(.+?)\]', r'[File: \2](' + parent + r'BearAssetsFiles/\1/\2)', md_text)
        matches = re.findall(r'\[File: .+?\]\((\.\./)*BearAssetsFiles/(.*?)\)', md_text)
        for groups in matches:
            file = groups[1]
            if ' ' in file:
                md_text = md_text.replace('BearAssetsFiles/' + file + ')', 'BearAssetsFiles/' + file.replace(' ', '%20') + ')')
    return md_text


def restore_image_links(md_text):
    '''
    MD image links restored back to Bear links
    '''
    restored = False
    if export_as_textbundles and re.search(r'!\[.*?\]\(assets/.+?\)', md_text):
        md_text = re.sub(r'!\[(.*?)\]\(assets/(.+?)_(.+?)( ".+?")?\) ?', r'[image:\2/\3]\4 \1', md_text)
        restored = True
    elif export_image_repository and re.search(r'!\[.*?\]\((\.\./)*BearAssetsImages/.+?\)', md_text):
        md_text = re.sub(r'!\[\]\((\.\./)*BearAssetsImages/(.+?)\)', r'[image:\2]', md_text)
        restored = True
    if restored:
        # Unescape %20 back to spaces in filenames:
        matches = re.findall(r'\[image:(.+?)\]', md_text)
        for file in matches:
            if '%20' in file:
                md_text = md_text.replace('[image:' + file, '[image:' + file.replace('%20', ' '))       
    return md_text


def restore_file_links(md_text):
    '''
    MD file links restored back to Bear links.
    '''
    restored = False
    if export_as_textbundles and re.search(r'\[File: .*?\]\(assets/.+?\)', md_text):
        md_text = re.sub(r'\[File: (.*?)\]\(assets/(.+?)_(.+?)( ".+?")?\) ?', r'[file:\2/\3]', md_text)
        restored = True
    elif export_image_repository and re.search(r'\[File: .*?\]\((\.\./)*BearAssetsFiles/.+?\)', md_text):
        md_text = re.sub(r'\[File: .*?\]\((\.\./)*BearAssetsFiles/(.+?)\)', r'[file:\2]', md_text)
        restored = True
    if restored:
        # Unescape %20 back to spaces in filenames:
        matches = re.findall(r'\[file:(.+?)\]', md_text)
        for file in matches:
            if '%20' in file:
                md_text = md_text.replace('[file:' + file, '[file:' + file.replace('%20', ' '))    
    return md_text


def copy_bear_images_and_files():
    # Images and files copied to common repositories
    # This copies every image or file, regardless of how many notes are exported
    # Only used if export_image_repository = True.
    subprocess.call(['rsync', '-r', '-t', '--delete', 
                    bear_image_path + "/", assets_images_path])
    if export_with_files:
        subprocess.call(['rsync', '-r', '-t', '--delete', 
                        bear_file_path + "/", assets_files_path])


def write_time_stamp():
    # write to time-stamp.txt file (used during sync)
    write_file(export_ts_file, "Markdown from Bear written at: " +
               datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S"), 0, 0)
    write_file(sync_ts_file_temp, "Markdown from Bear written at: " +
               datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S"), 0, 0)


def hide_tags(md_text):
    if hide_tags_in_comment_block:
        # hide tags in HTML comment blocks:
        pattern = r'^[ \t]*(\#[\w.].+)'
        pattern2 = r'<!-- \1 -->'
    else:
        # Hide tags from being seen as H1 (in some Markdown Editors),
        # by placing `period+space` at start of line:
        pattern = r'^[ \t]*(\#[\w.]+)'
        pattern2 = r'. \1'
    code_block = False
    new_lines = []
    for line in md_text.splitlines():
        if line[:2] in ['# ', '##']:
            # Headings don't accept tags
            new_lines.append(line)
            continue
        if line.startswith('```'):
            # Toggle code_block flag:
            code_block = code_block == False            
            new_lines.append(line)
        elif not code_block and '#' in line:
            # pre check: only run regex if line contain '#'
            changed_line = re.sub(pattern, pattern2, line)
            if changed_line.strip() != '':
                new_lines.append(changed_line)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)


def restore_tags(md_text):
    # Tags back to normal Bear tags:
    # stripping off html comment:
    md_text =  re.sub(r'(\n)<!--[ \t]*(\#[\w.].+?) -->', r'\1\2', md_text)
    # stripping off the `period+space` at start of line:
    md_text =  re.sub(r'(\n)\.[ \t]*(\#[\w.]+)', r'\1\2', md_text)
    return md_text


def clean_title(title):
    title = title[:56].strip()
    if title == "":
        title = "Untitled"
    title = re.sub(r'[/\\*?$@!^&\|~:]', r'-', title)
    title = re.sub(r'-$', r'', title)    
    return title.strip()


def write_file(filename, file_content, modified, created):
    with open(filename, "w", encoding='utf-8') as f:
        f.write(file_content)
    if created > 0 and modified > 0:
        os.utime(filename, (-1, created))
        os.utime(filename, (-1, modified))
        # This way of first setting cre_time and then mod_time with os.utime()
        # works in current directory (in this case: temp_path).
        # Older rsync does not preserve file-creation-time,
        # so use newer rsync v. 3.0.6 from Carbon Copy Cloner with --crtimes switch to preserve cre-time
    elif modified > 0:
        os.utime(filename, (-1, modified))


def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        file_content = f.read()
    return file_content


def get_file_date(filename):
    try:
        t = os.path.getmtime(filename)
        return t
    except:
        return 0


def dt_conv(dtnum):
    # Formula for date offset based on trial and error:
    hour = 3600 # seconds
    year = 365.25 * 24 * hour
    offset = year * 31 + hour * 6
    return dtnum + offset


def date_time_conv(dtnum):
    newnum = dt_conv(dtnum) 
    dtdate = datetime.datetime.fromtimestamp(newnum)
    #print(newnum, dtdate)
    return dtdate.strftime(' - %Y-%m-%d_%H%M')


def time_stamp_ts(ts):
    dtdate = datetime.datetime.fromtimestamp(ts)
    return dtdate.strftime('%Y-%m-%d at %H:%M') 


def date_conv(dtnum):
    dtdate = datetime.datetime.fromtimestamp(dtnum)
    return dtdate.strftime('%Y-%m-%d')


def delete_old_temp_files():
    # Deletes all files in temp folder before new export using "shutil.rmtree()":
    # NOTE! CAUTION! Do not change this function unless you really know shutil.rmtree() well!
    if os.path.exists(temp_path) and "BearExportTemp" in temp_path:
        # *** NOTE! Double checking that temp_path folder actually contains "BearExportTemp"
        # *** Because if temp_path is accidentally empty or root,
        # *** shutil.rmtree() will delete all files on your complete Hard Drive ;(
        shutil.rmtree(temp_path)
        # *** NOTE: USE rmtree() WITH EXTREME CAUTION!
    os.makedirs(temp_path)


def rsync_files_from_temp(dest_path, delete):
    # Moves markdown files to new folder using rsync:
    # This is a very important step! 
    # By first exporting all Bear notes to an emptied temp folder,
    # rsync will only update destination if modified or size have changed.
    # So only changed notes will be synced by Dropbox or OneDrive destinations.
    # Rsync will also delete notes on destination if deleted in Bear.
    # So doing it this way saves a lot of otherwise very complex programing.
    # Thank you very much, Rsync! ;)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    if delete:
        if export_with_files and export_image_repository:
            exclude_assets_files = 'BearAssetsFiles/'
        else:
            exclude_assets_files = ''
        if export_image_repository:
            exclude_assets_images = 'BearAssetsImages/'
        else:
            exclude_assets_images = ''
        
        # subprocess.call(['rsync',
        # Use newer rsync v. 3.0.6 from Carbon Copy Cloner with --crtimes to preserve cre-time
        subprocess.call([rsync_path, crswitch,
                            '-r', '-t', '--delete', '-q',
                            '--exclude', exclude_assets_images,
                            '--exclude', exclude_assets_files,
                            '--exclude', '.Ulysses*',
                            '--exclude', '*.Ulysses_Public_Filter',
                            temp_path + "/", dest_path])
    else:
        subprocess.call(['rsync', '-r', '-t', '-q',
                        temp_path + "/", dest_path])


def sync_md_updates():
    updates_found = False
    if not os.path.exists(sync_ts_file) or not os.path.exists(export_ts_file):
        return False
    ts_last_sync = os.path.getmtime(sync_ts_file)
    ts_last_export = os.path.getmtime(export_ts_file)
    # Update synced timestamp file:
    update_sync_time_file(0)
    file_types = ('*.md', '*.txt', '*.markdown')
    for (root, dirnames, filenames) in os.walk(export_path):
        '''
        This step walks down into all sub folders, if any.
        '''
        for pattern in file_types:
            for filename in fnmatch.filter(filenames, pattern):
                md_file = os.path.join(root, filename)
                ts = os.path.getmtime(md_file)
                if ts > ts_last_sync:
                    if not updates_found:  # Yet
                        # Wait 5 sec at first for external files to finish downloading from dropbox.
                        # Otherwise images in textbundles might be missing in import:
                        time.sleep(5)
                    updates_found = True
                    md_text = read_file(md_file)
                    backup_ext_note(md_file)
                    if check_if_image_added(md_text, md_file):
                        textbundle_to_bear(md_text, md_file, ts)
                        write_log('Imported to Bear: ' + md_file)
                    else:
                        update_bear_note(md_text, md_file, ts, ts_last_export)
                        write_log('Bear Note Updated: ' + md_file)
    if updates_found:
        # Give Bear time to process updates:
        time.sleep(3)
        # Check again, just in case new updates synced from remote (OneDrive/Dropbox) 
        # during this process!
        # The logic is not 100% fool proof, but should be close to 99.99%
        sync_md_updates() # Recursive call
    return updates_found


def check_if_image_added(md_text, md_file):
    if not '.textbundle/' in md_file:
        return False
    matches = re.findall(r'!\[.*?\]\(assets/(.+?_).+?\)', md_text)
    for image_match in matches:
        'F89CDA3D-3FCC-4E92-88C1-CC4AF46FA733-10097-00002BBE9F7FF804_IMG_2280.JPG'
        if not re.match(r'[0-9A-F]{8}-([0-9A-F]{4}-){3}[0-9A-F]{12}-[0-9A-F]{3,5}-[0-9A-F]{16}_', image_match):
            return True
    return False        


def textbundle_to_bear(md_text, md_file, mod_dt):
    md_text = restore_tags(md_text)
    bundle = os.path.split(md_file)[0]
    match = re.search(r'\{BearID:(.+?)\}', md_text)
    if match:
        uuid = match.group(1)
        # Remove old BearID: from new note
        md_text = re.sub(r'\<\!-- ?\{BearID\:' + uuid + r'\} ?--\>', '', md_text).rstrip() + '\n'
        md_text = insert_link_top_note(md_text, 'Images added! Link to original note: ', uuid)
    else:
        # New textbundle (with images), add path as tag: 
        md_text = get_tag_from_path(md_text, bundle, export_path)
    write_file(md_file, md_text, mod_dt, 0)
    os.utime(bundle, (-1, mod_dt))
    subprocess.call(['open', '-a', '/applications/bear.app', bundle])
    time.sleep(0.5)


def backup_ext_note(md_file):
    if '.textbundle' in md_file:
        bundle_path = os.path.split(md_file)[0]
        bundle_name = os.path.split(bundle_path)[1]
        target = os.path.join(sync_backup, bundle_name)
        bundle_raw = os.path.splitext(target)[0]
        count = 2
        while os.path.exists(target):
            # Adding sequence number to identical filenames, preventing overwrite:
            target = bundle_raw + " - " + str(count).zfill(2) + ".textbundle"
            count += 1
        shutil.copytree(bundle_path, target)
    else:
        # Overwrite former bacups of incoming changes, only keeps last one:
        shutil.copy2(md_file, sync_backup + '/')


def update_sync_time_file(ts):
    write_file(sync_ts_file,
        "Checked for Markdown updates to sync at: " +
        datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S"), ts, 0)


def update_bear_note(md_text, md_file, ts, ts_last_export):
    md_text = restore_tags(md_text)
    md_text = restore_image_links(md_text)
    md_text = restore_file_links(md_text)
    uuid = ''
    match = re.search(r'\{BearID:(.+?)\}', md_text)
    sync_conflict = False
    if match:
        uuid = match.group(1)
        # Remove old BearID: from new note
        md_text = re.sub(r'\<\!-- ?\{BearID\:' + uuid + r'\} ?--\>', '', md_text).rstrip() + '\n'

        sync_conflict = check_sync_conflict(uuid, ts_last_export)
        if sync_conflict:
            link_original = 'bear://x-callback-url/open-note?id=' + uuid
            message = '::Sync conflict! External update: ' + time_stamp_ts(ts) + '::'
            message += '\n[Click here to see original Bear note](' + link_original + ')'
            x_create = 'bear://x-callback-url/create?show_window=no' 
            bear_x_callback(x_create, md_text, message, '')   
        else:
            # Regular external update
            orig_title = backup_bear_note(uuid)
            # message = '::External update: ' + time_stamp_ts(ts) + '::'   
            x_replace = 'bear://x-callback-url/add-text?show_window=no&mode=replace_all&id=' + uuid
            bear_x_callback(x_replace, md_text, '', orig_title)
            # # Trash old original note:
            # x_trash = 'bear://x-callback-url/trash?show_window=no&id=' + uuid
            # subprocess.call(["open", x_trash])
            # time.sleep(.2)
    else:
        # New external md Note, since no Bear uuid found in text: 
        # message = '::New external Note - ' + time_stamp_ts(ts) + '::' 
        md_text = get_tag_from_path(md_text, md_file, export_path)
        x_create = 'bear://x-callback-url/create?show_window=no' 
        bear_x_callback(x_create, md_text, '', '')
    return


def get_tag_from_path(md_text, md_file, root_path, inbox_for_root=True, extra_tag=''):
    # extra_tag should be passed as '#tag' or '#space tag#'
    path = md_file.replace(root_path, '')[1:]
    sub_path = os.path.split(path)[0]
    tags = []
    if '.textbundle' in sub_path:
        sub_path = os.path.split(sub_path)[0]
    if sub_path == '': 
        if inbox_for_root:
            tag = '#.inbox'
        else:
            tag = ''
    elif sub_path.startswith('_'):
        tag = '#.' + sub_path[1:].strip()
    else:
        tag = '#' + sub_path.strip()
    if ' ' in tag: 
        tag += "#"               
    if tag != '': 
        tags.append(tag)
    if extra_tag != '':
        tags.append(extra_tag)
    for tag in get_file_tags(md_file):
        tag = '#' + tag.strip()
        if ' ' in tag: tag += "#"                   
        tags.append(tag)
    return md_text.strip() + '\n\n' + ' '.join(tags) + '\n'


def get_file_tags(md_file):
    try:
        subprocess.call([gettag_sh, md_file, gettag_txt])
        text = re.sub(r'\\n\d{1,2}', r'', read_file(gettag_txt))
        tag_list = json.loads(text)
        return tag_list
    except:
        return []


def bear_x_callback(x_command, md_text, message, orig_title):
    if message != '':
        lines = md_text.splitlines()
        lines.insert(1, message)
        md_text = '\n'.join(lines)
    ## 2018-02-23 at 22:41: 
    ## Using new `/add-text` mode: `replace_all` including changes to title.
    # if orig_title != '':
    #     lines = md_text.splitlines()
    #     title = re.sub(r'^#+ ', r'', lines[0])
    #     if title != orig_title:
    #         md_text = '\n'.join(lines)
    #     else:
    #         md_text = '\n'.join(lines[1:])        
    x_command_text = x_command + '&text=' + urllib.parse.quote(md_text)
    subprocess.call(["open", x_command_text])
    time.sleep(.2)


def check_sync_conflict(uuid, ts_last_export):
    conflict = False
    # Check modified date of original note in Bear sqlite db!
    with sqlite3.connect(bear_db) as conn:
        conn.row_factory = sqlite3.Row
        query = "SELECT * FROM `ZSFNOTE` WHERE `ZTRASHED` LIKE '0' AND `ZUNIQUEIDENTIFIER` LIKE '" + uuid + "'"
        c = conn.execute(query)
    for row in c:
        modified = row['ZMODIFICATIONDATE']
        uuid = row['ZUNIQUEIDENTIFIER']
        mod_dt = dt_conv(modified)
        conflict = mod_dt > ts_last_export
    return conflict


def backup_bear_note(uuid):
    # Get single note from Bear sqlite db!
    with sqlite3.connect(bear_db) as conn:
        conn.row_factory = sqlite3.Row
        query = "SELECT * FROM `ZSFNOTE` WHERE `ZUNIQUEIDENTIFIER` LIKE '" + uuid + "'"
        c = conn.execute(query)
    title = ''
    for row in c:  # Will only get one row if uuid is found!
        title = row['ZTITLE']
        md_text = row['ZTEXT'].rstrip()
        modified = row['ZMODIFICATIONDATE']
        mod_dt = dt_conv(modified)
        created = row['ZCREATIONDATE']
        cre_dt = dt_conv(created)
        md_text = insert_link_top_note(md_text, 'Link to updated note: ', uuid)
        dtdate = datetime.datetime.fromtimestamp(cre_dt)
        filename = clean_title(title) + dtdate.strftime(' - %Y-%m-%d_%H%M')
        if not os.path.exists(sync_backup):
            os.makedirs(sync_backup)
        file_part = os.path.join(sync_backup, filename) 
        # This is a Bear text file, not exactly markdown.
        backup_file = file_part + ".txt"
        count = 2
        while os.path.exists(backup_file):
            # Adding sequence number to identical filenames, preventing overwrite:
            backup_file = file_part + " - " + str(count).zfill(2) + ".txt"
            count += 1
        write_file(backup_file, md_text, mod_dt, 0)
        filename2 = os.path.split(backup_file)[1]
        write_log('Original to sync_backup: ' + filename2)
    return title


def insert_link_top_note(md_text, message, uuid):
    lines = md_text.split('\n')
    title = re.sub(r'^#{1,6} ', r'', lines[0])
    link = '::' + message + '[' + title + '](bear://x-callback-url/open-note?id=' + uuid + ')::'        
    lines.insert(1, link) 
    return '\n'.join(lines)


def init_gettag_script():
    gettag_script = \
    '''#!/bin/bash
    if [[ ! -e $1 ]] ; then
    echo 'file missing or not specified'
    exit 0
    fi
    JSON="$(xattr -p com.apple.metadata:_kMDItemUserTags "$1" | xxd -r -p | plutil -convert json - -o -)"
    echo $JSON > "$2"
    '''
    temp = os.path.join(HOME, 'temp')
    if not os.path.exists(temp):
        os.makedirs(temp)
    write_file(gettag_sh, gettag_script, 0, 0)
    subprocess.call(['chmod', '777', gettag_sh])
    

def notify(message):
    title = "ul_sync_md.py"
    try:
        # Uses "terminal-notifier", download at:
        # https://github.com/julienXX/terminal-notifier/releases/download/2.0.0/terminal-notifier-2.0.0.zip
        # Only works with MacOS 10.11+
        subprocess.call(['/Applications/terminal-notifier.app/Contents/MacOS/terminal-notifier',
                         '-message', message, "-title", title, '-sound', 'default'])
    except:
        write_log('"terminal-notifier.app" is missing!')        
    return


if __name__ == '__main__':
    main()
