# https://github.com/msaisushma/Github-API
# Dawson & Straub, Building Tools with GitHub

import json
import pprint

import pandas
import requests

api_url = "https://api.github.com/users"


def get_basic():
	url = api_url
	req = requests.get(url)
	res = req.content

	resp = json.loads(res)

	pd = pandas.DataFrame(resp)

	pprint.pprint(pd)


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
	get_basic()
