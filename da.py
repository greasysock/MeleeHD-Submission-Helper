import requests
import simplejson as json
import urllib

#deviantart gallary id can be found here http://www.deviantart.com/developers/console/gallery/gallery_folders/
gallery = 'F6004F98-1DAC-7805-065D-0319E61D5E3B'
#this is a deviantArt api interpreter, it is what handles all deviantArt related requests in main.py. Most functions are self explanatory.
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
#t = title, dec = description
def upload(t,dec,img, access_token):
	f = open(img, 'rb')
	s = site + '/stash/submit'
	payload = {'access_token': access_token,'stack': 'test','title': t, 'artist_comments': dec}
	ph = {'img' : f}
	r = requests.post(s, data = payload, files = ph)
	result = r.json()
	stash_id = result.get('itemid')
	return stash_id
def publish(id, access_token):
	s = site + '/stash/publish'
	payload = {'galleryids': gallery, 'catpath': 'resources/textures/other','is_mature': 'no','agree_tos': 'yes','agree_submission':'yes','access_token': access_token, 'itemid': id, 'allow_free_download': 'yes'}
	r = requests.post(s, data = payload)
	result = r.json()
	deviation_id = result.get('deviationid')
	return deviation_id
def glinkget(deviation_id, access_token):
	link = None
	s = site + '/deviation/%s?access_token=%s' % (deviation_id, access_token)
	r = requests.post(s)
	result = r.text
	parsed_json = json.loads(result)
	for keys,values in parsed_json.iteritems():
		if keys == 'content':
			jk = str(values)
			list = jk.split('\'')
			for x in list:
				test = '.deviantart.net/' in x
				if test == True:
					directlink = x
	return directlink
#a combination of all methods above, only returning a direct link.
def uppub(t,dec,img, access_token):
	stash_id = upload(t,dec,img, access_token)
	deviation_id = publish(stash_id, access_token)
	directlink = glinkget(deviation_id, access_token)
	return directlink
