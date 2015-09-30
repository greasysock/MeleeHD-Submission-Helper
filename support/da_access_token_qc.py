from support import conf
import requests
import requests.auth
import json
access_token, refresh_token = conf.da_token()
site = 'https://www.deviantart.com/api/v1/oauth2'
def test():
	s = site + '/placebo'
	payload = {'access_token': access_token}
	r = requests.post(s, data = payload)
	result = r.json()
	access_token_status = result.get('status')
	return access_token_status
#Refreshes da access token
def keyrefresh():
	accesstoken, refreshtoken = conf.da_token()
	CLIENT_ID, CLIENT_SECRET = conf.da_client()
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	post_data = {"grant_type": "refresh_token", "refresh_token": refreshtoken}
	response = requests.post("https://www.deviantart.com/oauth2/token", auth=client_auth, data=post_data)
	parsed_json = response.json()
	if parsed_json['status'] == 'success':
		configuration = 'conf.json'
		with open(configuration) as data_file:    
			data = json.load(data_file)
		data['deviantart']['accesstoken'] = parsed_json['access_token']
		data['deviantart']['refreshtoken'] = parsed_json['refresh_token']
		with open(configuration, 'w') as f:
			json.dump(data, f, sort_keys = True, indent = 4,ensure_ascii=False)
		global access_token
		access_token,refresh_token = conf.da_token()
	return parsed_json['status']
#Finds a gallary id from a gallary name.
def main():
	testresult = test()
	if testresult == 'success':
		pass
	else:
		print('DA: Token invalid, attempting refresh.')
		keyrefresh()
		refreshtest = test()
		if refreshtest == 'success':
			print('DA: Token refresh successful.')
		else:
			print('DA: Token refresh failed, try using getkey.py to generate a new one.')
			exit()
	global access_token
	return access_token