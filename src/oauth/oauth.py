import time
import requests
from config import connection_info

def get_app_token(app_id, secret):
	request_data = {
		"client_id": app_id,
		"client_secret": secret,
		"scope": "chat_login",
		"grant_type": "client_credentials"
	}
	r = requests.post("https://api.twitch.tv/kraken/oauth2/token", data=request_data)
	json = r.json()
	request_time = time.time()
	return AccessToken(json['access_token'], request_time + json['expires_in'])


class AccessToken(object):
	def __init__(self, access_token, expires_at):
		self.access_token = access_token
		self.expires_at = expires_at

	def is_valid(self):
		return time.time() < self.expires_at

	def has_expired(self):
		return not self.is_valid()
