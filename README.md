# Markdown export and sync of Bear notes

**Version 1.7.0, 2018-11-17 at 16:12 IST**

Update 2018-11-17:
- Refactored code: Now using the 'argparse' library instead of clunky, home-made CLI function.  
Thanks to @motin for that pull-request and code suggestion :)
- Updated shell script sample for easy run with various choices and multiple outputs.
- **Please see help text below for all input arguments:**
 
*Help text when run with "-h" in version 1.7.0:*
```
*** Run with "-h" to display help on all functions and argument switches.
*** If no arguments: script runs with internal defaults.
*** If switches are used alone, like: '-b', it will toggle default value.
*** Or use like this: '-b=false', '-b=0', '--text_bundle=false', '-b=true' to set explicit value.
*** Use either short form: '-b' or long form: '--text_bundle'
*** Also use '=' for input strings: '--out_path=OneDrive' or '-o=Box'
*** Multi values as CSV list: "--exclude_tags=private,banking,old stuff,stupid ideas"
*** NOTE: Enclose whole argument in " " if any spaces in tags or out_path

usage: bear_export_sync_test.py [-h] [-v [VERSION]] [-d [DEFAULT]]
                                [-r [FORCE_RUN]] [-f [TAG_FOLDERS]]
                                [-m [MULTI_FOLDERS]]
                                [-u [UNTAGGED_FOLDER_NAME]]
                                [-c [TAGS_COMMENTED]] [-w [WITHOUT_TAGS]]
                                [-t [INCLUDE_TAGS]] [-x [EXCLUDE_TAGS]]
                                [-b [AS_TEXTBUNDLES]] [-y [AS_HYBRIDS]]
                                [-i [INCLUDE_FILES]] [-p [REPOSITORIES]]
                                [-o [OUT_PATH]] [-l [LOGGING]] [-s [DO_SYNC]]
                                [-R [RAW_MD]] [-a [INCLUDE_ARCHIVED]]
                                [-n [ONLY_ARCHIVED]]

Markdown export from Bear sqlite database.

optional arguments:
  -h, --help            show this help message and exit
  -v [VERSION], --version [VERSION]
                        (Default: False) Displays version info.
  -d [DEFAULT], --default [DEFAULT]
                        (Default: True) Run only with internal defaults.
                        Depreciated (but there for backwards compatibility):
                        Running without any arguments will do the same.
  -r [FORCE_RUN], --force_run [FORCE_RUN]
                        (Default: False) Runs even if no changes in db since
                        last run.
  -f [TAG_FOLDERS], --tag_folders [TAG_FOLDERS]
                        (Default: True) Exports to folders using first tag
                        only, if `multi_folders = False`
  -m [MULTI_FOLDERS], --multi_folders [MULTI_FOLDERS]
                        (Default: True) Copies notes to all 'tag-paths' found
                        in note! Only active if `tag_folders = True`
  -u [UNTAGGED_FOLDER_NAME], --untagged_folder_name [UNTAGGED_FOLDER_NAME]
                        (Default: '_Untagged') If empty, untagged notes
                        exports to root-folder.
  -c [TAGS_COMMENTED], --tags_commented [TAGS_COMMENTED]
                        (Default: True) Hide tags in HTML comments: `<!--
                        #mytag -->`
  -w [WITHOUT_TAGS], --without_tags [WITHOUT_TAGS]
                        (Default: False) Remove all tags from exported notes.
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
  -b [AS_TEXTBUNDLES], --as_textbundles [AS_TEXTBUNDLES]
                        (Default: True) Exports all notes as Textbundles, also 
                        when no images in note.
  -y [AS_HYBRIDS], --as_hybrids [AS_HYBRIDS]
                        (Default: True) Exports as .textbundle only if images
                        included, otherwise as .md. Only used if
                        `as_textbundles = True`
  -i [INCLUDE_FILES], --include_files [INCLUDE_FILES]
                        (Default: True) Include file attachments. Only used if
                        'as_textbundles' or 'repositories' = True
  -p [REPOSITORIES], --repositories [REPOSITORIES]
                        (Default: True) Export all notes as md but link images
                        and files to common repositories. Only used if
                        `as_textbundles = False`
  -o [OUT_PATH], --out_path [OUT_PATH]
                        (Default: Dropbox) Examples: "-o=OneDrive",
                        "-o=/users/Guest" (/ is from HD root if permission!),
                        "-out_path=~" (~ means directly on HOME root).
                        "BearNotes" will be always be added to path for
                        security reasons.
  -l [LOGGING], --logging [LOGGING]
                        (Default: True)
  -s [DO_SYNC], --do_sync [DO_SYNC]
                        (Default: True) Sync external updates back into Bear
  -R [RAW_MD], --raw_md [RAW_MD]
                        (Default: False) Exports without any modification to
                        the note contents, just like Bear does. This implies
                        not hiding tags, not adding BearID. Note: This
                        disables later 'note to note' syncing of modified
                        contents: sync-back then as a new modified note.
  -a [INCLUDE_ARCHIVED], --include_archived [INCLUDE_ARCHIVED]
                        (Default: False) Include archived notes (in
                        '_Archived' sub folder)
  -n [ONLY_ARCHIVED], --only_archived [ONLY_ARCHIVED]
                        (Default: False) Only export archived notes
```

## Warning!
**Please discard versions 1.5.x !**

> It introduced CLI argument '-o' for export path, where it is possible to enter any user path. 
> 
> So if one accidentally entered root of an existing folder, all other files and folders there, would be deleted (by rsync) when running 1.5.x !
> 
> This is now corrected from version 1.6.0, by always adding 'BearNotes' to whatever path users supply with the '-o' argument. It's now (once again) hardcoded for your safety.
> 
> As always: please take a full backup of Bear and a full backup of your Mac before running new versions or when changing CLI arguments. 
> 
> Apologies and hope nobody ran into this problem/SNAFU :)

*Updated 2018-11-16:*

- *Fixed: tags getting HTML comment in code-blocks*
- *Fixed: tags or tag-like code, in codeblocks no longer exported in folders*
- *Simplified code in function: 'sub_path_from_tag()' used above*

*Updated 2018-11-15:*

- *Cleaning up code*
- *Bug fixes*
- *Added argument: '-l' do not write to Log-file.*
- *Added function and argument: '-w' export Without tags: All tags are stripped from text.*

*Updated 2018-11-14:*

- *Added command line arguments: -R for 'RAW' markdown export, and -s for no Sync.*
- *Included some other improvements from pull requests.*

*Updated 2018-11-13:*

- *Added command line argument help and switches.*

*Updated 2018-11-12:*

- *Now with export of file attachments (only to .textbundle)*
- *All untagged notes are now exported to '_Untagged' folder if 'make_tag_folders = True'*
- *Added choice for exporting with or without archived notes, or only archived.* 
- *Removes escaping of spaces in sync/import back to Bear.*
- *Fixed multiple copying if same tag is repeated in same note. Case sensitive though!*

*Updaded 2018-10-30:*

- *Use newer rsync from Carbon Copy Cloner to preserve file-creation-time.*
- *Fixed escaping of spaces in image names from iPhone camera taken directly in Bear.*

*Updaded 2018-10-17:*

- *new Bear path: 'Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data'*

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

### Syncs external edits back into Bear
Script first checks for external edits in Markdown files or textbundles (previously exported from Bear as described below):

* It replaces text in original note with `bear://x-callback-url/add-text?mode=replace` command   
(That way keeping original note ID and creation date)  
If any changes to title, new title will be added just below original title.  
(`mode=replace` does not replace title)
* Original note in `sqlite` database and external edit are both backed up as markdown-files to BearSyncBackup folder before import to bear.
* If a sync conflict, both original and new version will be in Bear (the new one with a sync conflict message and link to original).
* New notes created online, are just added to Bear  
(with the `bear://x-callback-url/create` command)
* If a textbundle gets new images from an external app, it will be opened and imported as a new note in Bear, with message and link to original note.  
(The `subprocess.call(['open', '-a', '/applications/bear.app', bundle])` command is used for this)

### Markdown export to Dropbox, OneDrive, or other:
Then exports all notes from Bear's database.sqlite as plain markdown files:

* Checks modified timestamp on database.sqlite, so exports only when needed.
* Sets Bear note's modification date on exported markdown files.
* Appends Bear note's creation date to filename to avoid “title-filename-collisions”
* Note IDs are included at bottom of markdown files to match original note on sync back:  
	{BearID:730A5BD2-0245-4EF7-BE16-A5217468DF0E-33519-0000429ADFD9221A}  
(these ID's are striped off again when synced back into Bear)
* Uses rsync for copying (from a temp folder), so only changed notes will be synced to Dropbox (or other sync services)
* rsync also takes care of deleting trashed notes
* "Hides” tags from being displayed as H1 in other markdown apps by adding `period+space` in front of first tag on a line:   
`. #bear #idea #python`   
* Or hide tags in HTML comment blocks like: `<!-- #mytag -->` if `hide_tags_in_comment_block = True`   
(these are striped off again when synced back into Bear)
* Makes subfolders named with first tag in note if `make_tag_folders = True`
* Files can now be copied to multiple tag-folders if `multi_tags = True`
* Export can now be restricted to a list of spesific tags: `limit_export_to_tags = ['bear/github', 'writings']`  
or leave list empty for all notes: `limit_export_to_tags = []`
* Can export and link to images in common image repository
* Or export as textbundles with images included 

You have Bear on Mac but also want your notes on your Android phone, on Linux or Windows machine at your office. Or you want them available online in a browser from any desktop computer. Here is a solution (or call it workaround) for now, until Bear comes with an online, Windows, or Android solution ;)

Happy syncing! ;)
