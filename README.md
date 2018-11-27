# Markdown export and sync of Bear notes

#### Version 1.7.7 - 2018-11-27 at 14:45 IST - Updates:
- Fix: Did not create `sync_backup` folder for textbundle sync/import. (Thanks to @dmd) 
    This is now created early on in line 280, and creation removed from two other places.
- Change: CLI argument: `-s` or `--do_sync` is now a toggle (to be in line with other arguments)  
    Default is still False.
- Added: `exist_ok=True` to: `os.makedirs(path, exist_ok=True)` most places 
    and no need for `if os.path.exists(path):`


## Related

- See: [change_log.md](change_log.md) for previous changes.
- See: [bear_export_sync.sh](bear_export_sync.sh) a sample script on how to use with params and multiple export paths.
- Download: [Python 3.7.1 for macOS](https://www.python.org/ftp/python/3.7.1/python-3.7.1-macosx10.9.pkg)

## Help text when run with "-h" in version 1.7.2

```txt
2018-11-18 at 17:07:56 ['/Users/roarvestre/Scripts/python/Bear-Markdown-Export/bear_export_sync.py', '-h']
usage: bear_export_sync.py [-h] [-v [VERSION]] [-d [DEFAULT]] [-o [OUT_PATH]]
                           [-s [DO_SYNC]] [-r [FORCE_RUN]] [-f [TAG_FOLDERS]]
                           [-m [MULTI_FOLDERS]] [-u [UNTAGGED_FOLDER_NAME]]
                           [-t [INCLUDE_TAGS]] [-x [EXCLUDE_TAGS]]
                           [-c [TAGS_COMMENTED]] [-w [WITHOUT_TAGS]]
                           [-b [AS_TEXTBUNDLE]] [-y [AS_HYBRIDS]]
                           [-i [INCLUDE_FILES]] [-p [REPOSITORIES]]
                           [-l [LOGGING]] [-R [RAW_MD]]
                           [-a [INCLUDE_ARCHIVED]] [-n [ONLY_ARCHIVED]]

Markdown export from Bear sqlite database.

optional arguments:
  -h, --help            show this help message and exit
  -v [VERSION], --version [VERSION]
                        (Default: False) Displays version info.
  -d [DEFAULT], --default [DEFAULT]
                        (Default: True) Run only with internal defaults.
                        Depreciated (but there for backwards compatibility to
                        1.6.x): Running without any arguments will do the
                        same.
  -o [OUT_PATH], --out_path [OUT_PATH]
                        (Default: Dropbox) Examples: "-o=OneDrive",
                        "-o=/users/Guest" Leading "/" means from HD root, if
                        permission!), "-out_path=~" (~ means directly on HOME
                        root). "BearNotes" will be always be added to path for
                        security reasons.
  -s [DO_SYNC], --do_sync [DO_SYNC]
                        (Default: False) Sync external updates back into Bear.
                        NOTE: This is not a toggle, turn on explicitly with:
                        "-s=1" or "--do_sync=true"
  -r [FORCE_RUN], --force_run [FORCE_RUN]
                        (Default: False) Runs even if no changes in Bear-db
                        since last run.
  -f [TAG_FOLDERS], --tag_folders [TAG_FOLDERS]
                        (Default: True) Exports to folders using first tag
                        only, if `multi_folders = False`
  -m [MULTI_FOLDERS], --multi_folders [MULTI_FOLDERS]
                        (Default: True) Copies notes to all 'tag-paths' found
                        in note! Only active if `tag_folders = True`
  -u [UNTAGGED_FOLDER_NAME], --untagged_folder_name [UNTAGGED_FOLDER_NAME]
                        (Default: "-u=_Untagged") If empty: "-u", untagged
                        notes exports to root-folder.
  -t [INCLUDE_TAGS], --include_tags [INCLUDE_TAGS]
                        (Default: '' all notes included) Example: "--
                        include_tags=bear,writings'", '-t=b' (all tags
                        beginning with 'b'). Comma separated list of tags in
                        notes, only matching notes will be exported. Works
                        only if `tag_folders = True`.
  -x [EXCLUDE_TAGS], --exclude_tags [EXCLUDE_TAGS]
                        (Default: '' no notes excluded) Example: "--
                        exclude_tags=private,.inbox,love letters,banking'",
                        '-x=.' (exclude all tags with leading '.') If a tag in
                        note matches one in this list, it will not be
                        exported.
  -c [TAGS_COMMENTED], --tags_commented [TAGS_COMMENTED]
                        (Default: True) Hide tags in HTML comments: `<!--
                        #mytag -->`
  -w [WITHOUT_TAGS], --without_tags [WITHOUT_TAGS]
                        (Default: False) Remove all tags from exported notes.
                        NOTE! Don't use with sync: original note will loose
                        all tags if changed externally and sync-back!
  -b [AS_TEXTBUNDLE], --as_textbundle [AS_TEXTBUNDLE]
                        (Default: True) Exports all notes as Textbundles, also
                        when no images in note
  -y [AS_HYBRIDS], --as_hybrids [AS_HYBRIDS]
                        (Default: True) Exports as .textbundle only if images
                        included, otherwise as .md. Only used if '--
                        as_textbundle=True'
  -i [INCLUDE_FILES], --include_files [INCLUDE_FILES]
                        (Default: True) Include file attachments. Only used if
                        'as_textbundle' or 'repositories' = True
  -p [REPOSITORIES], --repositories [REPOSITORIES]
                        (Default: True) Export all notes as md but link images
                        and files to common repositories. Will set
                        'as_textbundle' to False
  -l [LOGGING], --logging [LOGGING]
                        (Default: True)
  -R [RAW_MD], --raw_md [RAW_MD]
                        (Default: False) Exports without any modification to
                        the note contents, just like Bear does. This implies
                        not hiding tags, not adding BearID. Note: This
                        disables later 'note to note' syncing of modified
                        contents, but it's then synced back as a new modified
                        'duplicate' note.
  -a [INCLUDE_ARCHIVED], --include_archived [INCLUDE_ARCHIVED]
                        (Default: False) Include archived notes (in
                        '_Archived' sub folder)
  -n [ONLY_ARCHIVED], --only_archived [ONLY_ARCHIVED]
                        (Default: False) Use to only export archived notes
```

## Description

Python script for export and roundtrip sync of Bear's notes to OneDrive, Dropbox, etc. and edit online with [StackEdit](https://stackedit.io/app), or use a markdown editor like *Typora* on Windows or a suitable app on Android. Remote edits and new notes get synced back into Bear with this script.

Set up seamless syncing with Ulysses’ external folders on Mac, with images included!  
Write and add photos in Bear, then reorder, glue, and publish, export, or print with styles in Ulysses—  
bears and butterflies are best friends ;)  
(PS. The manual order you set for notes in Ulysses' external folder, is maintained during syncs, unless title is changed.) 

**Please use as is or make a new branch for updates!  
Thank you all for any input, and sorry that I don't have time to review and test pull requests.**

BEAR IN MIND! This version is free to use as is, and please improve or modify your own version as needed. But do be careful! both `rsync` and `shutil.rmtree` used here, are powerful commands that can wipe clean a whole folder tree or even your complete HD if paths are set incorrectly! Also, be safe, take a fresh backup of both Bear and your Mac before first run.

*See also: [Bear Power Pack](https://github.com/rovest/Bear-Power-Pack/blob/master/README.md)*

## Features

- Bear notes exported as plain Markdown or Textbundles with images.
- Syncs external edits back to Bear with original image links intact. 
- New external `.md` files or `.textbundles` are added. (Tags created from sub folder name)
- Export option: Make nested folders from tags. For first tag only, or all tags (duplicates notes)
- Export option: Include or exclude export of notes with specific tags.
- Export option: Export as `.textbundles` with images included. 
- Or as: `.md` with links to common image repository 
- Export option: Hide tags in HTML comments like: `<!-- #mytag -->` if `hide_tags_in_comment_block = True`
- **NEW** Hybrid export: `.textbundles` of notes with images, otherwise regular `.md` (Makes it easier to browse and edit on other platforms.)
- **NEW** Writes log to `bear_export_sync_log.txt` in `BearSyncBackup` folder.

Edit your Bear notes online in browser on [OneDrive.com](https://onedrive.live.com). It has a ok editor for plain text/markdown. Or with [StackEdit](https://stackedit.io/app), an amazing online markdown editor that can sync with *Dropbox* or *Google Drive*

Read and edit your Bear notes on *Windows* or *Android* with any markdown editor of choice. Remote edits or new notes will be synced back into Bear again. *Typora* works great on Windows, and displays images of text bundles as well.

NOTE! If syncing with Ulysses’ external folders on Mac, remember to edit that folder settings to `.textbundle` and `Inline Links`!

Run script manually or add it to a cron job for automatic syncing (every 5 – 15 minutes, or whatever you prefer).  
([LaunchD Task Scheduler](https://itunes.apple.com/us/app/launchd-task-scheduler/id620249105?mt=12) Is easy to configure and works very well for this)

See: [bear_export_sync.sh](bear_export_sync.sh) script for how to use.

### Syncs external edits back into Bear

Script first checks for external edits in Markdown files or textbundles (previously exported from Bear as described below):

- It replaces text in original note with `bear://x-callback-url/add-text?mode=replace` command   
  (That way keeping original note ID and creation date)  
  If any changes to title, new title will be added just below original title.  
  (`mode=replace` does not replace title)
- Original note in `sqlite` database and external edit are both backed up as markdown-files to BearSyncBackup folder before import to bear.
- If a sync conflict, both original and new version will be in Bear (the new one with a sync conflict message and link to original).
- New notes created online, are just added to Bear (with the `bear://x-callback-url/create` command)
- If a textbundle gets new images from an external app, it will be opened and imported as a new note in Bear, with message and link to original note.
  (The `subprocess.call(['open', '-a', '/applications/bear.app', bundle])` command is used for this)

### Markdown export to Dropbox, OneDrive, or other:

Then exports all notes from Bear's database.sqlite as plain markdown files:

- Checks modified timestamp on database.sqlite, so exports only when needed.
- Sets Bear note's modification date on exported markdown files.
- Appends Bear note's creation date to filename to avoid “title-filename-collisions”
- Note IDs are included at bottom of markdown files to match original note on sync back:  
  {BearID:730A5BD2-0245-4EF7-BE16-A5217468DF0E-33519-0000429ADFD9221A}  
  (these ID's are striped off again when synced back into Bear)
- Uses rsync for copying (from a temp folder), so only changed notes will be synced to Dropbox (or other sync services)
- rsync also takes care of deleting trashed notes
- "Hides” tags from being displayed as H1 in other markdown apps by adding `period+space` in front of first tag on a line:
  `. #bear #idea #python`   
- Or hide tags in HTML comment blocks like: `<!-- #mytag -->` if `hide_tags_in_comment_block = True`   
  (these are striped off again when synced back into Bear)
- Makes subfolders named with first tag in note if `make_tag_folders = True`
- Files can now be copied to multiple tag-folders if `multi_tags = True`
- Export can now be restricted to a list of spesific tags: `limit_export_to_tags = ['bear/github', 'writings']`  
  or leave list empty for all notes: `limit_export_to_tags = []`
- Can export and link to images in common image repository
- Or export as textbundles with images included 

You have Bear on Mac but also want your notes on your Android phone, on Linux or Windows machine at your office. Or you want them available online in a browser from any desktop computer. Here is a solution (or call it workaround) for now, until Bear comes with an online, Windows, or Android solution ;)

Happy syncing! ;)
