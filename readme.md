#Disclaimer:

#####**This script is not an official melee hd script. It has not been reviewed by any major member of the project. Even though I personally have no intentions of compromising your personal information, I am still very new to python, so I cannot ensure your privacy. You as the user are resposible for looking over the code to ensure your own privacy.**

###What it does:

MeleeHD Submission Helper script *greatly* reduces the time and effort required to submit texture posts to melee hd while at the same time ensuring each post you make is formatted correctly.
It takes a provided texture vector, *.pdf* *.ai* *.svg*, and converts it into a *.png* and *.svg* if necessary via inkscape, optionally uploads everything to dropbox, uploads an sd and hd version of the texture to deviantart and then finally creates a bbcode template to paste into a new meleehd post.

###Requirements:

- Firefox - Only required if testing autosubmit feature (which is currently broken)

- Inkscape

- Python 3+ or 2.7 and Modules: splinter, requests, flask, simplejson, dropbox
  - how to install missing modules: ```pip install splinter```

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
  2. In *OAuth2 Redirect URI Whitelist* enter: ```http://127.0.0.1:5000/da_callback```
  3. Copy and paste client id into **conf.json** getkey.py/Client Id = "client id here"
  4. Copy and paste client secret into **conf.json** getkey.py/Client Secret = "client secret here"

* Dropbox access token (only required if you want to use dropbox.) 
  1. Create a new application here: https://www.dropbox.com/developers/apps
  2. Cick on your new app and select 'Generate access token'
  3. Copy that token into **conf.json** dropbox, accesstoken = "access token here"
  4. Enable dropbox in **conf.json** dropbox, enabled = "true"

###How to use it: 

1. Generate a new devaintArt access token by starting getkey.py ```python getkey.py``` and opening up [127.0.0.1:5000](http://127.0.0.1:5000) in your browser, go through the steps of autheticating the application through deviantArt. The access token will save to conf.json, along with it's refresh token. Exit getkey.py
  - To exit getkey.py press ```ctr + c```
2. Start main.py ```python main.py```, the script will create folders: **upload**,**submitted**, and **packedtextures**
3. Now that everything is setup, you can place any number of*.pdf*,*.svg*, or *.ai* textures in the **submit** folder with the apropriate name, and start main.py ```python main.py```. All submited textures will be moved to **submitted**, the processed textures will be moved to **packedtextures**.
  * Example: 'tex1_32x36_11ad122fc65442bc_2.ai' would be the correct name to be processed
  * Note: putting a *.png* in **submit** along with an *.ai*/*.pdf*/*.svg* will override inkscape and submit that texture instead of creating a new *.png*.
5. After it's done processing, copy the contents of */packedtextures/texturename/texturename_bbctemp.txt* into a texture post on Melee HD

####Post example:

![alt text](http://orig01.deviantart.net/507d/f/2015/274/4/d/examplepost_by_ui_ssbm-d9blcmg.png "post example")
