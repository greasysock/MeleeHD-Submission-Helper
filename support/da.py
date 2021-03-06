import requests
import json
import urllib
from support import conf, da_access_token_qc
###This is a deviantArt api interpreter, it is what handles all deviantArt related requests in main.py. Most functions are self explanatory.
#deviantart gallery id can be found here http://www.deviantart.com/developers/console/gallery/gallery_folders/
site = 'https://www.deviantart.com/api/v1/oauth2'
result = None

#ensures quality of access token.
access_token = None
refresh_token = None
#manages access token for da.py session. Ensures a working access_token before continuing.
access_token = da_access_token_qc.main()
#tests an access token for its validity.
def test():
	s = site + '/placebo'
	payload = {'access_token': access_token}
	r = requests.post(s, data = payload)
	result = r.json()
	access_token_status = result.get('status')
	return access_token_status
def galleryfind(gallery_name):
	s = site + '/gallery/folders?access_token=%s' % access_token
	r = requests.post(s)
	result = r.json()
	x = 0
	while True:
		humanname = result['results'][x]['name']
		x = x + 1
		if humanname == gallery_name:
			folderid = result['results'][x-1]['folderid']
			break
	return folderid
#Uploads image to sta.sh, devaintart's image host, and returns the image's id for publishing to deviantArt later.
def upload(title,description,img):
	loadedimg = open(img, 'rb')
	s = site + '/stash/submit'
	payload = {'access_token': access_token,'stack': 'MeleeHD','title': title, 'artist_comments': description}
	imagepayload = {'img' : loadedimg}
	r = requests.post(s, data = payload, files = imagepayload)
	result = r.json()
	stash_id = result.get('itemid')
	return stash_id
#Publishes refrenced stash image id to deviantArt and returns it's deviation id.
def publish(stash_id):
	gallery = galleryfind('Melee HD Project')
	s = site + '/stash/publish'
	payload = {'galleryids': gallery, 'catpath': 'resources/textures/other','is_mature': 'no','agree_tos': 'yes','agree_submission':'yes','access_token': access_token, 'itemid': stash_id, 'allow_free_download': 'yes'}
	r = requests.post(s, data = payload)
	result = r.json()
	deviation_id = result.get('deviationid')
	deviation_link = result.get('url')
	return deviation_id, deviation_link
#Finds a user's profile name and creates a link to their profile
def profile():
	s = site + '/user/whoami?access_token=%s' % access_token
	r = requests.post(s)
	result = r.json()
	username = result.get('username')
	profile_url = 'http://%s.deviantart.com/'%username
	return profile_url, username
#Uses deviation id to retreive image link.
def glinkget(deviation_id):
	link = None
	s = site + '/deviation/%s?access_token=%s' % (deviation_id, access_token)
	r = requests.post(s)
	result = r.text
	parsed_json = json.loads(result)
	#parses response for direct link. This is only done this way because I didn't know how to properly naviate .json files at the time:|
	for keys,values in parsed_json.iteritems():
		if keys == 'content':
			jk = str(values)
			list = jk.split('\'')
			for x in list:
				test = '.deviantart.net/' in x
				if test == True:
					directlink = x
	return directlink
def stashlink(stash_id):
	s = site + '/stash/item/{}?'.format(stash_id)
	payload = {'access_token': access_token}
	r = requests.post(s, data = payload)
	result = r.json()
	direct_url = []
	for x in result['files']:
		direct_url.append(x['src'])
	return direct_url[-1]
#Combination of all methods above, returning a direct link.
def uppub(t,dec,img):
	stash_id = upload(t,dec,img)
	deviation_id, deviation_link = publish(stash_id)
	directlink = glinkget(deviation_id)
	return directlink, deviation_link
