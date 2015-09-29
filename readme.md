Currently Under Development. Not in a working state.

For more information, please visit http://meleehd.boards.net/thread/89/wip-meleehd-auto-submission-script

Things completed so far:


deviantArt api implemintation.

Dropbox api implemintation.

Inkscape implementation.

Linux and Windows support.


Things that need to be completed:


Auto Forum Submission (WIP) - It's working about 75% of the time at the moment, due to unpredictable element changes in the page caused by advertisments, it can sometimes fill ad space rather than the forum.

deviantArt access code creation and refreshing. - All access codes used in deviantArt must be renewed every 30 minutes.

FileOptimizer Implementation.

Error handling.

Save built post as bbcode.


How it'll work: 

You'd put either either an ,.ai, .pdf, or .svg in a folder name 'submit' named as the texture you want to submit, you can put as many textures you want in the folder. Once you start the script, it'll create an .svg from the .ai or .pdf if you provided one, and from the .svg. it'll render a .png, and then it'll go through a folder named 'sdtextures' which has a very large dump of sd textures in it provided by iwishiwassleeping and it grabs the sd version of the texture, puts all the files in a folder named 'packeddirectory/texture_name' uploads the sd/hd version to deviantArt, bulds the post based on it's bbcode, and saves the post to a file in the packed texture directory, makes a post for injecting it into the forum page via javascript, logs into meleehd/load submit page, fills the page, and finally submits the texture. You also optionally will be able to upload to dropbox and provide a project files link, but this will not be a requirement or necessary in most cases.

Requirements:

Firefox

Inkscape

Python 2.7 and Modules: splinter, requests, flask, simplejson, dropbox

Note: You must create an 'sdtextures' directory and fill it with textures from a dump, this one has the vast majority of sd textures: https://mega.nz/#F!TYsjHBQC!R8cxMQ68yseVBf5Luf2gCA
'packedtextures', 'submitted', and 'upload' will also need to be created in the root directory of the script in order for this script to work.
You also must provide your own api keys from deviantart/dropbox.
