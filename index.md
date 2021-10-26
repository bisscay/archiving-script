## Welcome to the Archiving Script Wiki

Python script for lossless compression of processed files into archives using Gzip

## Description
Create a script which will be run **weekly**.

Script should:

Find all files created during previous month in **source location**, compress them into single file named YYYY_MM.gz and place it in **output location**.

Source files should then be deleted

Those directories have some files already there for testing.

## Note:
Script runs on Python 2.6.6 and above.

Gzip implements the DEFLATE algorithm (ZIP_DEFLATED).

Runtime error results if zlib module is absent.

POSIX does [not mandate][1] Birth time, modification time(mtime) is used.

If we are certain permission and ownership of the file remains thesame, C-Time will be a good option.

M-Time is currently used, C-Time will be adopted to improve security.

Copying of files should be done with the **p**(*--preserve*) flag to retain timestamps. `cp -a` for recursive copying.

## Usage:
Place script in directory of choice, then run:

`./compressionScript.py -s <source-location> -o <output-location> -m <start-month> -y <start-year> --endMonth <end-month> --endYear <end-year>`

Source location is mandatory

Compression destination defaults to an archive folder in the source directory

By default compression starts from April, 2021

Months and years are one-base indexed; i.e January == 1

End-year if specified must be greater or equal to start-year, else current-year is used

If end-year is equal, end-month must be equal or greater than start-month, else current-month is used

Negative month(s) or year(s) are seen as invalid options

Month(s) over 12-th will default value(s) 

### Knowledge Base:
A **volume** is gotten from formating a filesystem on a partition.

Ideally;

Windows Filesystem (NTFS) has a max of  **2e32 - 1** i.e [4,294,967,295][2] files per folder or volume

Linux Filesystem (ext4) has a max of [2,796,202][2] files per **folder** or [4,294,967,285][2] files per **volume**

[There’s really no limit of the aggregate size of the files in a folder, though there are limits on the number of files in a folder.][2]

### *Partition Table Schemes:*

(Consideration is based on primary and not logical disks) *bAe's deduction*

MBR - Master Boot Record has a max volume size of [2TB][3]

GPT - GUID Partition Table volume size is >= [2TB][3]

## *Timestamps in Unix:*

You can stat a file `stat my_file_name` to see each time or use the corresponding commands for individual views.

Access time - atime: `ls -lu`

When a file or directory is read from or written to.

Change time - ctime: `ls -lc`

Metadata changes - file's ownership (username and/or group), access permissions and file content changes.

Modify time - mtime: `ls -l`

When a file is written to(content changes).

[Source](https://www.unixtutorial.org/atime-ctime-mtime-in-unix-filesystems/)

### *Shabang:*
Script was created on a Windows machine with an editor's end-of-line set for MSDOS/Windows. 

A **dos2unix** tool was used to curb all trailing ^ M tags that result in a windows environment. 

This way, a shabang can be used to manipulate execution of script on linux environments.

Ensure the script has the right execution permissions and the shabang matches your python location.

`ls -l` to verify permission, `chmod +x compressionScript.py` to change permission and `which python` to verify location.

## *File Copy:*

`-p` same as `--preserve=mode,ownership,timestamps`

--preserve[=attr_list] preserves the specified attributes, separated by a comma 

(Default: mode,ownership,timestamps).

Additional options: links, context, xattr, all.

For recursive copy: `cp -a` same as `cp --archive` or `cp -dR --preserve=ALL` which additionally preserves symbolic links.

[Source](https://www.computerhope.com/unix/ucp.htm)

[1]: https://askubuntu.com/questions/918300/when-is-birth-date-for-a-file-actually-used#:~:text=Birth%20time%20is%20the%20time%20when%20the%20file,inode%20change%20time%20%28ctime%29%20are%20mandated%20by%20POSIX.

[2]: https://askleo.com/is-there-a-limit-to-what-a-single-folder-or-directory-can-hold/

[3]: https://www.coursera.org/professional-certificates/google-it-support?utm_source=bg&utm_medium=sem&utm_campaign=15-GoogleCareerCert-HubPage-ROW&utm_content=15-GoogleCareerCert-HubPage-ROW&campaignid=415061745&adgroupid=1211662279754676&device=c&keyword=google%20certification%20courses&matchtype=b&network=o&devicemodel=&adpostion=&creativeid=&msclkid=dac9854696f9154950dee5d5200105e4&utm_term=google%20certification%20courses
