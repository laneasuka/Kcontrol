#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import requests
import json


def load(filename='dat'):
    if filename in os.listdir(os.getcwd()):
        with open(filename) as f:
            return json.loads(f.read())
    return {}


def save(d, filename='dat'):
    args = load(filename)
    args.update(d)
    with open(filename, 'w') as f:
        f.write(json.dumps(args))


P = load()
# print args
s = requests.Session()  # 会话形式访问，保存cookie

data = {
    'username': P['username'],
    'password': P['password'],
    'clientid': P['client_id'],
    'mobilecode': '2ac4OpVXgT0yllHM'
}

# r = s.get(args['url_code'])
# print r.content
r = s.post(P['url_code'], data=data)
# print r.content, '\n', r.url, '\n', r.status_code, '\n', r.history

code = r.url.split("=")[1]
print 'code:          ', code

data = {
    'grant_type': 'authorization_code',
    'client_id': P['client_id'],
    'client_secret': P['client_secret'],
    'code': code,
    'redirect_uri': P['callbackurl']
}

r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/accessToken', data=data)
token = eval(r.text)
print 'access_token:  ', token['access_token']
print 'refresh_token: ', token['refresh_token']

headers = {'Authorization': 'Bearer %s' % token['access_token']}
r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/UserInfo', headers=headers)
userinfo = eval(r.text)
print 'userid:        ', userinfo['userid']

data = {
    'userid': userinfo['userid']
}
r = requests.post('http://kk.bigk2.com:8080/KOAuthDemeter/User/getGeneralRemoteList', headers=headers, data=data)
print r.content.decode('utf-8')
