import json
conf = 'conf.json'
#configuration parameter checker.
def da_token():
	with open(conf) as data_file:    
		data = json.load(data_file)
		da_token = data['deviantart']['accesstoken']
		da_refresh = data['deviantart']['refreshtoken']
	return da_token,da_refresh
def da_client():
	with open(conf) as data_file:    
		data = json.load(data_file)
		da_client_id = data['getkey.py'][0]['Client Id']
		da_client_secret = data['getkey.py'][1]['Client Secret']
	return da_client_id,da_client_secret