import requests
import simplejson as json
import urllib

###This is a deviantArt api interpreter, it is what handles all deviantArt related requests in main.py. Most functions are self explanatory.

#deviantart gallary id can be found here http://www.deviantart.com/developers/console/gallery/gallery_folders/
#I will implement a gallary id retreiver in the future, this is just temporary solution.
gallery = 'F6004F98-1DAC-7805-065D-0319E61D5E3B'
site = 'https://www.deviantart.com/api/v1/oauth2'
result = None
#tests an access token for its validity.
def test(access_token):
	s = site + '/placebo'
	payload = {'access_token': access_token}
	r = requests.post(s, data = payload)
	result = r.json()
	access_token_status = result.get('status')
	return access_token_status
#Uploads image to sta.sh, devaintart's image host, and returns the image's id for publishing to deviantArt later.
def upload(title,description,img, access_token):
	loadedimg = open(img, 'rb')
	s = site + '/stash/submit'
	payload = {'access_token': access_token,'stack': 'MeleeHD','title': title, 'artist_comments': description}
	imagepayload = {'img' : loadedimg}
	r = requests.post(s, data = payload, files = imagepayload)
	result = r.json()
	stash_id = result.get('itemid')
	return stash_id
#Publishes refrenced stash image id to deviantArt and returns it's deviation id.
def publish(stash_id, access_token):
	s = site + '/stash/publish'
	payload = {'galleryids': gallery, 'catpath': 'resources/textures/other','is_mature': 'no','agree_tos': 'yes','agree_submission':'yes','access_token': access_token, 'itemid': stash_id, 'allow_free_download': 'yes'}
	r = requests.post(s, data = payload)
	result = r.json()
	deviation_id = result.get('deviationid')
	return deviation_id
#Uses deviation id to retreive image link.
def glinkget(deviation_id, access_token):
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
#Combination of all methods above, returning a direct link.
def uppub(t,dec,img, access_token):
	stash_id = upload(t,dec,img, access_token)
	deviation_id = publish(stash_id, access_token)
	directlink = glinkget(deviation_id, access_token)
	return directlink
