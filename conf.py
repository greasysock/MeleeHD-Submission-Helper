import json
conf = 'conf.json'
#configuration parameter checker.
def da_token():
	with open(conf) as data_file:    
		data = json.load(data_file)
		da_token = data['deviantart']['accesstoken']
	return da_token