# https://github.com/msaisushma/Github-API
# Dawson & Straub, Building Tools with GitHub
# Jason McVetta, Password Privacy, Generate a Github OAuth2 Token, https://advanced-python.readthedocs.io/en/latest/rest/authtoken.html#password-privacy

import getpass
import json
import pprint
import urllib.parse as up

import pandas
import requests

api_url = "https://api.github.com/"
api_user_url = "https://api.github.com/users"


def get_basic(url=api_url):
	req = requests.get(url)
	pd = req_to_df(req)

	return pd


def req_to_df(req):
	res = req.content

	resp = json.loads(res)

	if isinstance(resp, dict):
		resp = [resp]

	try:
		pd = pandas.DataFrame(resp)
	except BaseException as e:
		pprint.pprint(resp)
		raise e

	return pd


def get_page_030():
	pd = get_basic()
	print(pd['current_user_url'])


def get_page_033():
	repos_url = '/'.join((api_user_url, 'xrd', 'repos'))

	pd = get_basic(repos_url)

	pprint.pprint(pd['owner'][0]['id'])


def get_page_039():
	# http://docs.python-requests.org/en/master/user/authentication/
	# https://advanced-python.readthedocs.io/en/latest/rest/authtoken.html#password-privacy

	api_auth_url = up.urljoin(api_url, 'authorizations')

	note = 'OAuth practice' # input('Note (optional): ')
	payload = {}
	if note :
		payload['note'] = note

	df = req_to_df(reg_get_auth(api_auth_url, payload))

	pprint.pprint(df)


def reg_get_auth(auth_url, payload):
    req = requests.get(
                    auth_url, 
                    auth=requests.auth.HTTPBasicAuth(
                                    input('Github username: '), 
                                    getpass.getpass('Github password: ')
                            ),
                    data=json.dumps(payload)
            )
    return req


def get_comments():
	usrname = input("Enter the username:")
	url = api_url+usrname+"/events"
	req = requests.get(url)
	res = req.content
	# print res
	resp = json.loads(res)

	pprint.pprint(resp)

	pload = [li['payload']for li in resp]
	payload = pload[3]
	# print payload

	for _, v in payload.items():
		print(v['html_url'])


if __name__ == '__main__':
	get_page_039()
