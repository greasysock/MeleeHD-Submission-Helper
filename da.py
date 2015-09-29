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
	b = result.get('status')
	return b
def upload(t,dec,img, access_token):
	f = open(img, 'rb')
	s = site + '/stash/submit'
	payload = {'access_token': access_token,'stack': 'test','title': t, 'artist_comments': dec}
	ph = {'img' : f}
	r = requests.post(s, data = payload, files = ph)
	result = r.json()
	itemid = result.get('itemid')
	return itemid
def publish(id, access_token):
	s = site + '/stash/publish'
	payload = {'galleryids': gallery, 'catpath': 'resources/textures/other','is_mature': 'no','agree_tos': 'yes','agree_submission':'yes','access_token': access_token, 'itemid': id, 'allow_free_download': 'yes'}
	r = requests.post(s, data = payload)
	result = r.json()
	devid = result.get('deviationid')
	return devid
def glinkget(devid, access_token):
	link = None
	s = site + '/deviation/%s?access_token=%s' % (devid, access_token)
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
					link = x
	return link
def uppub(t,dec,img, access_token):
	itemid = upload(t,dec,img, access_token)
	devid = publish(itemid, access_token)
	imlink = glinkget(devid, access_token)
	return imlink
