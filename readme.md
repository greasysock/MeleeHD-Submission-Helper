

###Requirements:

- Firefox - Only requred if testing autosubmit feature (which is currently broken)

- Inkscape

- Python 2.7 and Modules: splinter, requests, flask, simplejson, dropbox

For more information, please visit http://meleehd.boards.net/thread/89/wip-meleehd-auto-submission-script

###Things completed so far:


deviantArt api implemintation.

Dropbox api implemintation.

Inkscape implementation.

Linux and Windows support.


###Things that need to be completed:

FileOptimizer Implementation.

Error handling.

###What you need to have before you start:

* deviantArt client id and client secret.
  1. Create a new application here: https://www.deviantart.com/developers/apps by selecting register application.
  2. In *OAuth2 Redirect URI Whitelist* enter: *http://127.0.0.1:5000/da_callback*
  3. Copy and paste client id into **conf.json** getkey.py/Client Id = "client id here"
  4. Copy and paste client secret into **conf.json** getkey.py/Client Secret = "client secret here"

* Dropbox access token (only required if you want to use dropbox.) 
  1. Create a new application here: https://www.dropbox.com/developers/apps
  2. Cick on your new app and select 'Generate access token'
  3. Copy that token into **conf.json** dropbox, accesstoken = "access token here"
  4. Enable dropbox in **conf.json** dropbox, enabled = "true"

###How it works: 

1. Generate a new devaintArt access token by starting getkey.py ```python getkey.py``` and opening up 127.0.0.1:5000 in your browser and go through the steps of autheticating the application through deviantArt, the access token will save to **conf.json** automatically.
2. Start main.py ```python main.py```, the script will create folders: **upload**,**submitted**, **packedtextures**, and **sdtextures**
3. After the script is finished setting up, all that needs to be done now is to fill **sdtextures** with a texture dump.
 * Go here and download texture source https://mega.nz/#F!TYsjHBQC!R8cxMQ68yseVBf5Luf2gCA
4. Now that everything is setup, you can place either a **.pdf**,**.svg**,**.ai** in the **submit** folder with the apropriate name, and start main.py **python main.py** will start processing the textures.
 * Note: putting a .png in **submit** with the same texture name as an .ai/.pdf/.svg will override inkscape and submit that texture instead.
 * All textures process will be moved to **complete**
5. After it's done process, copy the **/packedtextures/texturename/texturename_bbctemp.txt** into a texture post on Melee HD
