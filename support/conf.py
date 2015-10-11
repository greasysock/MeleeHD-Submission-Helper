import json
import os.path
conf = 'conf.json'
if os.path.isfile(conf) == True:
    pass
else:
    configprep = dict()
    configprep['deviantart'] = {'accesstoken':'put da access token here', 'refreshtoken':'getkey.py generates refresh token'}
    configprep['dropbox'] = {'enabled':'false','accesstoken':'put db access token here'}
    configprep['experimental'] = {'autosubmit':'false'}
    configprep['getkey.py'] = {'Client Id':'Put da app id here','Client Secret':'Put da app secret here'}
    configprep['inkscape'] = {'winexe':'\"C:\\Program Files\\Inkscape\\inkscape.exe\"','linux':'inkscape'}
    configprep['bbcode'] = {'Notify':'meleehd uncleiroh el linkmain111 gameonion'}
    with open(conf, 'w') as f:
        json.dump(configprep, f, sort_keys = True, indent = 4,ensure_ascii=False)
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
def db_client():
    with open(conf) as data_file:
        data = json.load(data_file)
        db_status = data['dropbox'][0]['enabled']
    if db_status == 'true':
        status = True
    else:
        status = False
    return status
def bbcode_notify():
    with open(conf) as data_file:
        data = json.load(data_file)
        notifylist = data['bbcode']['Notify']
        notifylist = notifylist.split(' ')
        atnotifylist = []
        for x in notifylist:
            atnotifylist.append('@'+x)
        atnotifylist = ' '.join(atnotifylist)
    return atnotifylist