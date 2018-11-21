## Change Log

### bear_export_sync.py

#### Version 1.7.6 - 2018-11-21 at 11:00 IST - Updates:
- Fix: removing empty elements in CSV in '-t=' and '-x=' values.
- `bear_import_sync.sh` updated to reflect changes

#### Version 1.7.5 - 2018-11-21 at 07:48 IST - Updates:
- Fix on issue #12: hardcoded temp vs temp_path.
- '~/BearTemp' remamed to '~/BearProc', so '~/BearTemp' and '~/temp' are now obsolete

#### Version 1.7.4 - 2018-11-20 at 21:46 IST - Updates:
- Fix on issue #18: emtpy arguments confuses rsync! in 'def rsync_files_from_temp()'

#### Version 1.7.2 - 2018-11-18 at 17:15 IST - Updates:
- Added and tidied up comments sections and reordered some code lines, but no real code changes.

#### Version 1.7.1 - 2018-11-17 at 22:06 IST - Updates:
- Refactored code: Now using the 'argparse' library instead of clunky, home-made CLI function.  
Thanks to @motin for that pull-request and code suggestion :)
- Updates shell script sample for easy run with various choices and multiple outputs.
- Command line argument for sync-back to Bear is now default off for security reasons. 
  It's also not a toggle, but have to be turned on explicitly with: "-s=1" or "--do_sync=true"

#### Updates 2018-11-16:
- Fixed: tags getting HTML comment in code-blocks
- Fixed: tags or tag-like code, in codeblocks no longer exported in folders
- Simplified code in function: 'sub_path_from_tag()' used above

### Warning

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

#### Updates 2018-11-15:
- Cleaning up code
- Bug fixes
- Added argument: '-l' do not write to Log-file.
- Added function and argument: '-w' export Without tags: All tags are stripped from text.

#### Updates 2018-11-14:
- Added command line arguments: -R for 'RAW' markdown export, and -s for no Sync.
- Included some other improvements from pull requests.

#### Updates 2018-11-13:
- Added command line argument help and switches.

#### Updates 2018-11-12:
- Now with export of file attachments (only to .textbundle)
- All untagged notes are now exported to '_Untagged' folder if 'make_tag_folders = True'
- Added choice for exporting with or without archived notes, or only archived. 
- Removes escaping of spaces in sync/import back to Bear.
- Fixed multiple copying if same tag is repeated in same note. Case sensitive though!

#### Updates 2018-10-30:
- Use newer rsync from Carbon Copy Cloner to preserve file-creation-time.
- Fixed escaping of spaces in image names from iPhone camera taken directly in Bear.

#### Updates 2018-10-17:
- New Bear DB path: 'Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data'