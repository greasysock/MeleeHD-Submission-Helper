from flask import Flask, abort, request, redirect
from uuid import uuid4
import requests
import requests.auth
import urllib
#This script is used to get access tokens from deviantart, to get this working, you must fill out CLIENT_ID and CLIENT_SECRET with your own via creating a new application at http://deviantart.com/developers
#This is only a temporary solution until I'm finished developing the script, a solution to this would be to run a dedicated server to hand out access tokens.
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = "http://127.0.0.1:5000/da_callback"

app = Flask(__name__)
@app.route('/')


def hompage():
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
			  "scope": "stash basic gallery browse"}
    url = "https://www.deviantart.com/oauth2/authorize?" + urllib.urlencode(params)
    return redirect(url, code=302)

def save_created_state(state):
    pass
def is_valid_state(state):
    return True

@app.route('/da_callback')
def da_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    return access_token

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    response = requests.post("https://www.deviantart.com/oauth2/token",
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]

if __name__ == '__main__':
    app.run(debug=True, port=5000)
