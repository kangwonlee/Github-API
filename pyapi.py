# https://github.com/msaisushma/Github-API
# Dawson & Straub, Building Tools with GitHub
# Jason McVetta, Password Privacy, Generate a Github OAuth2 Token, https://advanced-python.readthedocs.io/en/latest/rest/authtoken.html#password-privacy

import getpass
import json
import os
import pprint
import sys
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
	resp = parse_req_json(req)

	if isinstance(resp, dict):
		resp = [resp]

	try:
		pd = pandas.DataFrame(resp)
	except BaseException as e:
		pprint.pprint(resp)
		raise e

	return pd


def parse_req_json(req):
    return json.loads(req.content)


def req_to_df_unpack_dict(req):
	"""
	request to DataFrame unpacking nested dictionaries

	req : list of dictionaries (or nested dictionaries)
			[
			   {'a1': 'a1 str', 'b1': {'c1': 'b1.c1 str'}},
			   {'a2': 'a2 str', 'b2': {'c2': 'b2.c2 str'}},
			   {'a3': 'a3 str', 'b3': {'c3': 'b3.c3 str'}},
			   {'a4': 'a4 str', 'b4': {'c4': 'b4.c4 str'}},
			]

	"""

	resp = parse_req_json(req)

	# response check
	if isinstance(resp, dict):
		raise ValueError(f'dict : {resp}')

	# unpack nested dictionaries into simpler dictionaries
	rows = []
	for d in resp:
		row = {}
		for k in d.keys():
			keys = [k]
			if isinstance(d[k], dict):
				for dk in d[k]:
					keys.append(dk)
					# recursion possible?
					row['.'.join(keys)] = d[k][dk]
			else:
				row[k] = d[k]
		rows.append(row)

	try:
		pd = pandas.DataFrame(rows)
	except BaseException as e:
		pprint.pprint(rows)
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


def get_page_49():
	# http://docs.python-requests.org/en/master/user/authentication/
	# https://advanced-python.readthedocs.io/en/latest/rest/authtoken.html#password-privacy

	api_auth_url = up.urljoin(api_url, 'rate_limit')

	note = 'rate check practice' # input('Note (optional): ')
	payload = {}
	if note :
		payload['note'] = note

	df = pandas.DataFrame.from_dict(
			parse_req_json(reg_get_auth(api_auth_url, payload))
		)

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


def get_repo_comments_public(owner, repo, b_verbose=False):
	url = url_repo_comments(owner, repo)
	if b_verbose:
		print(f'get_repos_public() : url = {url}')
	return(get_basic(url))


def url_repo_comments(owner, repo):
	# https://developer.github.com/v3/pulls/comments/#list-comments-in-a-repository
    return up.urljoin(api_url, '/'.join(('repos', owner, repo, 'pulls', 'comments')))


def payload_repo_commit_comment(body_str=False, path_str=False, position_int=False):
	"""
	Prepare the payload for a comment
	ref : https://developer.github.com/v3/repos/comments/#input
	"""

	assert body_str

	result = {'body':body_str,}

	if path_str:
		result['path'] = str(path_str)

	if position_int:
		result['position'] = int(position_int)

	return result


def main(argv):
	if argv:
		pprint.pprint(get_repo_comments_public(argv[0], argv[1], b_verbose=True))
	else:
		print(f"usage : python {os.path.split(__file__)[-1]} <github id>")


def get_comments():
	usrname = input("Enter the username:")
	url = api_url+usrname+"/events"
	req = requests.get(url)
	resp = parse_req_json(req)

	pprint.pprint(resp)

	pload = [li['payload']for li in resp]
	payload = pload[3]
	# print payload

	for _, v in payload.items():
		print(v['html_url'])


if __name__ == '__main__':
	main(sys.argv[1:])
